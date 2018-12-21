from ortools.graph import pywrapgraph

import numpy as np
import uuid


class ResidFlow(object):
    """Improves the makespan value of the matching using maxflow.

    This class tries to improve the makespan of a matching based on the
    algorithm introduced in Gairing et. al 2004 and Gairing et. al. 2007.  Our
    adaptation works as follows.  After we have a matching, construct three
    groups of papers.  The first group are all papers papers whos paper scores
    are greater than the makespan value, the second group are all papers whose
    papers scores are between the makespan and the makespan - maxaffinity, the
    final group are the papers whose paper scores are less than makespan -
    maxaffinity.  For each paper in the last group, we're going to unassign the
    reviewer with the lowest score. Then, we'll construct a new flow network
    from the papers in the first group as sources through the appropriate
    reviewers and papers in the second group and ending at the papers in the
    third group as sinks. Each sink will accept a single new assignment.  Once
    this assignment is made.  We'll construct another flow network of all
    available reviewers to the papers that do not have enough reviewers and
    solve the flow problem again.  Then we'll have a feasible solution. We can
    continue to iterate this process until either: there are no papers in the
    third group or there are no papers in the first group.
    """
    def __init__(self, loads, coverages, weights, makespan, solution):
        """Initialize a makespan matcher

        Args:
            loads - a list of integers specifying the maximum number of papers
                  for each reviewer.
            coverages - a list of integers specifying the number of reviews per
                 paper.
            weights - the affinity matrix (np.array) of papers to reviewers.
                   Rows correspond to reviewers and columns correspond to
                   papers.
            makespan - makespan value.
            solution - a matrix of assignments (same shape as weights).

        Returns:
            initialized makespan matcher.
        """
        self.n_rev = np.size(weights, axis=0)
        self.n_pap = np.size(weights, axis=1)
        self.loads = loads
        self.coverages = coverages
        self.weights = weights
        self.id = uuid.uuid4()
        self.makespan = makespan     # the minimum allowable paper score.
        self.solution = solution
        assert(self.weights.shape == self.solution.shape)
        self.maxaff = np.max(self.weights)
        self.valid = True

        self.min_cost_flow = pywrapgraph.SimpleMinCostFlow()

        self.start_inds = []
        self.end_inds = []
        self.caps = []
        self.costs = []
        self.source = self.n_rev + self.n_pap
        self.sink = self.n_rev + self.n_pap + 1

    def _refresh_internal_vars(self):
        """Set start, end, caps, costs to be empty."""
        self.min_cost_flow = pywrapgraph.SimpleMinCostFlow()
        self.start_inds = []
        self.end_inds = []
        self.caps = []
        self.costs = []

    def _grp_paps_by_ms(self):
        """Group papers by makespan.

        Divide papers into 3 groups based on their paper scores. A paper score
        is the sum affinities among all reviewers assigned to review that paper.
        The first group will contain papers with paper scores greater than or
        equal to the makespan.  The second group will contain papers with paper
        scores less than the makespan but greater than makespan - maxaffinity.
        The third group will contain papers with papers scores less than
        makespan - maxaffinity.

        Args:
            None

        Returns:
            A 3-tuple of paper ids.
        """
        paper_scores = np.sum(self.solution * self.weights, axis=0)
        g1 = np.where(paper_scores >= self.makespan)[0]
        g2 = np.intersect1d(
            np.where(self.makespan > paper_scores),
            np.where(paper_scores >= self.makespan - self.maxaff))
        g3 = np.where(self.makespan - self.maxaff > paper_scores)[0]
        assert(np.size(g1) + np.size(g2) + np.size(g3) == self.n_pap)
        return g1, g2, g3

    def _grp_paps_by_cov(self):
        """Group papers by coverage.

        Divide papers into 3 groups based on coverage. The first group will
        contain papers with 1 too few reviewers.  The second group will contain
        papers with 1 too many reviewers. The third group will contain papers
        with 1 too many reviewers.

        Args:
            None

        Returns:
            A 3-tuple of paper ids.
        """
        covs = np.sum(self.solution, axis=0)
        g1 = np.where(covs == self.coverages - 1)[0]
        g2 = np.where(covs == self.coverages)[0]
        g3 = np.where(covs == self.coverages + 1)[0]
        assert(np.size(g1) + np.size(g2) + np.size(g3) == self.n_pap)
        return g1, g2, g3

    def _worst_reviewer(self, papers):
        """Get the worst reviewer from each paper in the input.

        Args:
            papers - numpy array of paper indices.

        Returns:
            A tuple of rows and columns of the
        """
        mask = (self.solution - 1.0) * -10000
        tmp = (mask + self.weights).astype('float')
        worst_revs = np.argmin(tmp, axis=0)
        return worst_revs[papers], papers

    def _construct_sol_validifier_network(self, g1):
        """Construct a network to make an invalid solution valid.

        Args:
            g1 - numpy array of paper ids in group 1 (-1 reviewer).


        Returns:
            None -- modifies the internal min_cost_flow network.
        """
        # Must convert to python ints first.
        g1 = [int(x) for x in g1]
        print("NUM TO ASSIGN %s" % len(g1))
        # First construct edges between the source and each available reviewer.
        rev_caps = self.loads - np.sum(self.solution, axis=1)
        assert(np.size(rev_caps) == self.n_rev)
        for i in range(self.n_rev):
            self.start_inds.append(self.source)
            self.end_inds.append(i)
            self.caps.append(int(rev_caps[i]))
            self.costs.append(0)

        # Next construct the sink node and edges to each paper in g1.
        for i in range(np.size(g1)):
            self.start_inds.append(self.n_rev + g1[i])
            self.end_inds.append(self.sink)
            self.caps.append(1)
            self.costs.append(0)

        # For each reviewer not assigned to a paper in g1, create an edge.
        revs, paps1 = np.nonzero((self.solution - 1.0)[:, g1])
        for i in range(np.size(revs)):
            rev = int(revs[i])
            pap = g1[paps1[i]]
            assert(self.solution[rev, pap] == 0.0)
            self.start_inds.append(rev)
            self.end_inds.append(self.n_rev + pap)
            self.caps.append(1)
            self.costs.append(int(-1.0 - 10000 * self.weights[rev, pap]))

        self.supplies = np.zeros(self.n_rev + self.n_pap + 2)
        self.supplies[self.source] = int(np.size(g1))
        self.supplies[self.sink] = -int(np.size(g1))

        for i in range(len(self.start_inds)):
            self.min_cost_flow.AddArcWithCapacityAndUnitCost(
                self.start_inds[i], self.end_inds[i], self.caps[i],
                self.costs[i])
        for i in range(len(self.supplies)):
            self.min_cost_flow.SetNodeSupply(i, int(self.supplies[i]))

    def _construct_ms_improvement_network(self, g1, g2, g3):
        """Construct the network the reassigns reviewers to improve makespan.

        Args:
            g1 - numpy array of paper ids in group 1 (best).
            g2 - numpy array of paper ids in group 2.
            g3 - numpy array of paper ids in group 3 (worst).

        Returns:
            None -- modifies the internal min_cost_flow network.
        """
        # Must convert to python ints first.
        g1 = [int(x) for x in g1]
        g2 = [int(x) for x in g2]
        g3 = [int(x) for x in g3]
        assert(len(g1) + len(g2) + len(g3) == self.n_pap)
        assert(not set(g1).intersection(set(g2)) and
               not set(g1).intersection(set(g3)) and
               not set(g2).intersection(set(g3)))
        print(len(g1), len(g2), len(g3))
        # First construct edges between the source and each pap in g1.
        for i in range(np.size(g1)):
            self.start_inds.append(self.source)
            self.end_inds.append(self.n_rev + g1[i])
            self.caps.append(1)
            self.costs.append(0)

        # Next construct the sink node and edges to each paper in g3.
        for i in range(np.size(g3)):
            self.start_inds.append(self.n_rev + g3[i])
            self.end_inds.append(self.sink)
            self.caps.append(1)
            self.costs.append(0)

        # Now, for each assignment in the g1 group, reverse the flow.
        revs, paps1 = np.nonzero(self.solution[:, g1])
        for i in range(np.size(revs)):
            rev = int(revs[i])
            pap = g1[paps1[i]]
            self.start_inds.append(self.n_rev + pap)
            self.end_inds.append(rev)
            self.caps.append(1)
            # self.costs.append(int(1.0 + 10000 * self.weights[rev, pap]))
            self.costs.append(1)

            # and now connect this reviewer to each paper in g2 if that
            # reviewer has not already been assigned to that paper.
            for pap2 in g2:
                if self.solution[rev, pap2] == 0.0:
                    self.start_inds.append(rev)
                    self.end_inds.append(self.n_rev + pap2)
                    self.caps.append(1)
                    self.costs.append(
                        int(-1.0 - 10000 * self.weights[rev, pap2]))

        # For each paper in g2, reverse the flow to assigned revs.
        revs, paps2 = np.nonzero(self.solution[:, g2])
        for i in range(np.size(revs)):
            if self.solution[rev, pap2] == 1.0:
                rev = int(revs[i])
                pap2 = g2[paps2[i]]
                self.start_inds.append(self.n_rev + pap2)
                self.end_inds.append(rev)
                self.caps.append(1)
                # self.costs.append(int(1.0 + 10000 * self.weights[rev, pap2]))
                self.costs.append(1)

        # For each reviewer, connect them to a paper in g3 if not assigned.
        for rev in range(self.n_rev):
            for pap3 in g3:
                if self.solution[rev, pap3] == 0.0:
                    self.start_inds.append(rev)
                    self.end_inds.append(self.n_rev + pap3)
                    self.caps.append(1)
                    self.costs.append(
                        int(-1.0 - 10000 * self.weights[rev, pap3]))

        self.supplies = np.zeros(self.n_rev + self.n_pap + 2)
        self.supplies[self.source] = int(np.size(g3))
        self.supplies[self.sink] = -int(np.size(g3))

        for i in range(len(self.start_inds)):
            self.min_cost_flow.AddArcWithCapacityAndUnitCost(
                self.start_inds[i], self.end_inds[i], self.caps[i],
                self.costs[i])
        for i in range(len(self.supplies)):
            self.min_cost_flow.SetNodeSupply(i, int(self.supplies[i]))

    def solve_ms_improvement(self):
        """Reassign reviewers to improve the makespan."""
        if self.min_cost_flow.Solve() == self.min_cost_flow.OPTIMAL:
            num_un = 0
            for arc in range(self.min_cost_flow.NumArcs()):
                # Can ignore arcs leading out of source or into sink.
                if self.min_cost_flow.Tail(arc) != self.source and \
                                self.min_cost_flow.Head(arc) != self.sink:
                    if self.min_cost_flow.Flow(arc) > 0:
                        if self.min_cost_flow.UnitCost(arc) > 0:
                            pap = self.min_cost_flow.Tail(arc) - self.n_rev
                            rev = self.min_cost_flow.Head(arc)
                            assert(self.solution[rev, pap] == 1.0)
                            self.solution[rev, pap] = 0.0
                            num_un += 1
                        elif self.min_cost_flow.UnitCost(arc) < 0:
                            rev = self.min_cost_flow.Tail(arc)
                            pap = self.min_cost_flow.Head(arc) - self.n_rev
                            assert(self.solution[rev, pap] == 0.0)
                            self.solution[rev, pap] = 1.0
                        else:
                            assert(False)
            assert (np.sum(self.solution) == np.sum(self.coverages))
            print('NUM UNASSIGNED %d' % num_un)
            self.valid = False
        else:
            raise Exception('There was an issue with the min cost flow input.')

    def solve_validifier(self):
        """Reassign reviewers to make the matching valid."""
        if self.min_cost_flow.Solve() == self.min_cost_flow.OPTIMAL:
            for arc in range(self.min_cost_flow.NumArcs()):
                # Can ignore arcs leading out of source or into sink.
                if self.min_cost_flow.Tail(arc) != self.source and \
                                self.min_cost_flow.Head(arc) != self.sink:
                    if self.min_cost_flow.Flow(arc) > 0:
                        rev = self.min_cost_flow.Tail(arc)
                        pap = self.min_cost_flow.Head(arc) - self.n_rev
                        assert(self.solution[rev, pap] == 0.0)
                        assert(np.sum(self.solution[:, pap], axis=0) ==
                               self.coverages[pap] - 1)
                        self.solution[rev, pap] = 1.0
            assert (np.sum(self.solution) == np.sum(self.coverages))
            self.valid = True
        else:
            raise Exception('There was an issue with the min cost flow input.')

    def sol_as_mat(self):
        if self.valid:
            return self.solution
        else:
            raise Exception(
                'You must have solved the model optimally or suboptimally '
                'before calling this function.')

    def try_improve_ms(self):
        """Try to improve the minimum paper score.

        Construct the refinement network (that routes assignments from the
        group of papers with high paper score to low paper scores) and solve the
        corresponding min cost flow problem. Then, remove the worst reviewer
        from each paper with more than the required number of reviewers.
        Finally, construct the validifier network to route available reviewers
        to papers missing a reviewer.

        Args:
            None

        Returns:
            A boolean representing whether makespan was violated (within the
            allowable approximation factor.
        """
        self._refresh_internal_vars()
        assert (np.sum(self.solution) == np.sum(self.coverages))
        g1, g2, g3 = self._grp_paps_by_ms()
        print(np.size(g1), np.size(g3))
        if np.size(g1) > 0 and np.size(g3) > 0:
            curr_assign = np.sum(self.solution)
            self._construct_ms_improvement_network(g1, g2, g3)
            self.solve_ms_improvement()
            # assert (np.sum(self.solution) == np.sum(self.coverages))
            # assert(np.sum(self.solution) == curr_assign)
            self._refresh_internal_vars()
            w_revs, w_paps = self._worst_reviewer(g3)
            self.solution[w_revs, w_paps] = 0.0
            # for i in range(len(w_revs)):
            #     assert (self.solution[w_revs[i], w_paps[i]] == 1.0)
            #     self.solution[w_revs[i], w_paps[i]] = 0.0
            g1, _, _ = self._grp_paps_by_cov()
            self._construct_sol_validifier_network(g1)
            self.solve_validifier()
            # assert (np.sum(self.solution) == np.sum(self.coverages))
            return True, np.size(g1), np.size(g3)
        else:
            return False, np.size(g1), np.size(g3)

if __name__ == '__main__':
    costs = np.array([[.1, .9, .3],
                      [.1, .4, .2],
                      [.1, .14, .1],
                      [.7, .1, .7]])
    sol = np.array([[0, 1, 0],
                    [1, 1, 0],
                    [1, 0, 1],
                    [0, 0, 1]])
    m = ResidFlow(np.array([2, 2, 2, 2]), np.array([2, 2, 2]), costs, 1.2, sol)
    g1, g2, g3 = m._grp_paps_by_ms()
    m._construct_ms_improvement_network(g1, g2, g3)
    m.solve_ms_improvement()
    print(m.sol_as_mat())
    m._refresh_internal_vars()
    w_revs, w_paps = m._worst_reviewer(g3)
    m.solution[w_revs, w_paps] = 0.0
    g1, _, _ = m._grp_paps_by_cov()
    m._construct_sol_validifier_network(g1)
    print(m.start_inds)
    print(m.end_inds)
    print(m.caps)
    print(m.costs)
    m.solve_validifier()
    print(m.sol_as_mat())
