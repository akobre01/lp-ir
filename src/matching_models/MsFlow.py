from collections import defaultdict

from ortools.graph import pywrapgraph

import time
import numpy as np
import uuid


class MsFlow(object):
    """Approximate makespan matching via flow network..

    Approximately solve the reviewer assignment problem with makespan
    constraint. Based on the algorithm introduced in Gairing et. al 2004 and
    Gairing et. al. 2007.  Our adaptation works as follows.  After we have a
    matching, construct three groups of papers.  The first group are all papers
    with scores > makespan value, the second group are all papers whose
    papers scores are between the makespan and the makespan - maxaffinity, the
    final group are the papers whose paper scores are less than makespan -
    maxaffinity.  For each paper in the last group, we'll unassign the
    reviewer with the lowest score. Then, we'll construct a new flow network
    from the papers in the first group as sources through reviewers assigned to
    those paper and terminating in the papers in the last group. Each sink will
    accept a single new assignment.  Once this assignment is made.  We'll
    construct another flow network of all available reviewers to the papers that
    do not have enough reviewers and solve the flow problem again.  Then we'll
    have a feasible solution. We can continue to iterate this process until
    either: there are no papers in the first group, there are no papers in the
    third group, or running the procedure does not change the sum total score of
    the matching.

    OLD TEXT:
    we're going to unassign the
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
    def __init__(self, loads, coverages, affs, sol=None, ms=0.0):
        """Initialize a makespan flow matcher

        Args:
            loads - a list of integers specifying the maximum number of papers
                  for each reviewer.
            coverages - a list of integers specifying the number of reviews per
                 paper.
            weights - the affinity matrix (np.array) of papers to reviewers.
                   Rows correspond to reviewers and columns correspond to
                   papers.
            solution - a matrix of assignments (same shape as weights).
            makespan - makespan value.

        Returns:
            initialized makespan matcher.
        """
        self.n_rev = np.size(affs, axis=0)
        self.n_pap = np.size(affs, axis=1)
        self.loads = loads
        self.coverages = coverages
        # make sure that all weights are positive:
        self.orig_affs = affs.copy()
        self.affs = affs.copy()
        min_aff = np.min(affs)
        if min_aff < 0:
            self.affs -= min_aff
        self.id = uuid.uuid4()
        self.makespan = ms     # the minimum allowable paper score.
        self.solution = sol if sol else np.zeros((self.n_rev, self.n_pap))
        assert(self.affs.shape == self.solution.shape)
        self.maxaff = np.max(self.affs)
        self.valid = True

        self.min_cost_flow = pywrapgraph.SimpleMinCostFlow()

        self.start_inds = []
        self.end_inds = []
        self.caps = []
        self.costs = []
        self.source = self.n_rev + self.n_pap
        self.sink = self.n_rev + self.n_pap + 1

    def objective_val(self):
        """Get the objective value of the RAP."""
        return np.sum(self.sol_as_mat() * self.orig_affs)

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
        paper_scores = np.sum(self.solution * self.affs, axis=0)
        g1 = np.where(paper_scores >= self.makespan)[0]
        # g3 = np.where(self.makespan - self.maxaff > paper_scores)[0]
        # g2 = np.setdiff1d(np.setdiff1d(paper_scores, g1)[0], g3)[0]
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
        papers with correct # of reviewers. The third group will contain papers
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
        tmp = (mask + self.affs).astype('float')
        worst_revs = np.argmin(tmp, axis=0)
        return worst_revs[papers], papers

    def _construct_and_solve_validifier_network(self):
        """Construct a network to make an invalid solution valid.

        To do this we need to ensure that:
            1) each load upper bound is satisfied
            2) each paper coverage constraint is satisfied.

        Returns:
            None -- modifies the internal min_cost_flow network.
        """
        # Construct edges between the source and each reviewer that must review.
        rev_caps = np.maximum(self.loads - np.sum(self.solution, axis=1), 0)
        assert (np.size(rev_caps) == self.n_rev)
        pap_caps = np.maximum(self.coverages - np.sum(self.solution, axis=0), 0)
        flow = np.sum(pap_caps)
        self._construct_graph_and_solve(self.n_rev, self.n_pap, rev_caps,
                                        pap_caps, self.affs, flow)

        # Finally, return.
        assert (np.all(np.sum(self.solution, axis=0) == self.coverages))
        assert (np.all(np.sum(self.solution, axis=1) <= self.loads))
        self.valid = True
        return self.solution

    def _construct_ms_improvement_network_old(self, g1, g2, g3):
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
        self._refresh_internal_vars()
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
        added = set()
        for i in range(np.size(revs)):
            rev = int(revs[i])
            pap = g1[paps1[i]]
            assert(self.solution[rev, pap] == 1.0)
            self.start_inds.append(self.n_rev + pap)
            self.end_inds.append(rev)
            self.caps.append(1)
            self.costs.append(int(1.0 + 10000 * self.affs[rev, pap]))
            # self.costs.append(1)

            # and now connect this reviewer to each paper in g2 if that
            # reviewer has not already been assigned to that paper.
            if rev not in added:
                for pap2 in g2:
                    if self.solution[rev, pap2] == 0.0:
                        assert((rev, pap2) not in added)
                        added.add((rev, pap2))

                        self.start_inds.append(rev)
                        self.end_inds.append(self.n_rev + pap2)
                        self.caps.append(1)
                        self.costs.append(
                            int(-1.0 - 10000 * self.affs[rev, pap2]))
                added.add(rev)
        # For each paper in g2, reverse the flow to assigned revs.
        revs, paps2 = np.nonzero(self.solution[:, g2])
        for i in range(np.size(revs)):
            rev = int(revs[i])
            pap = g2[paps2[i]]
            assert(self.solution[rev, pap] == 1.0)
            self.start_inds.append(self.n_rev + pap)
            self.end_inds.append(rev)
            self.caps.append(1)
            self.costs.append(int(1.0 + 10000 * self.affs[rev, pap]))
            # self.costs.append(1)
            # TODO(AK): below??
            # self.costs.append(0)

        # For each reviewer, connect them to a paper in g3 if not assigned.
        for rev in range(self.n_rev):
            for pap3 in g3:
                if self.solution[rev, pap3] == 0.0:
                    self.start_inds.append(rev)
                    self.end_inds.append(self.n_rev + pap3)
                    self.caps.append(1)
                    self.costs.append(
                        int(-1.0 - 10000 * self.affs[rev, pap3]))

        flow = int(min(np.size(g3), np.size(g1)))
        self.supplies = np.zeros(self.n_rev + self.n_pap + 2)
        self.supplies[self.source] = flow    #int(np.size(g3))
        self.supplies[self.sink] = -flow     #-int(np.size(g3))

        for i in range(len(self.start_inds)):
            self.min_cost_flow.AddArcWithCapacityAndUnitCost(
                self.start_inds[i], self.end_inds[i], self.caps[i],
                self.costs[i])
        for i in range(len(self.supplies)):
            self.min_cost_flow.SetNodeSupply(i, int(self.supplies[i]))

    def _construct_ms_improvement_network(self, g1, g2, g3):
        """Construct the network the reassigns reviewers to improve makespan.

        In v2 we allow for each paper in G1 to have 1 reviewer removed. This
        guarantees that papers in G1 can only fall to G2. Then, we assign each
        unassigned reviewer to the papers in G2 and G3. Papers in G2 have their
        flows reversed **only if their score, s, satisfies
        s- r(g2)_max + r(g1)_min > T - max, so that they remain in G2. Then,
        assign all reviewers who had their flows reversed to the availabe papers
        in G3.

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
        pap_scores = np.sum(self.solution * self.affs, axis=0)
        # First construct edges between the source and each pap in g1.
        self._refresh_internal_vars()
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

        ################################################
        # For each paper in g2, create a dummy node the restricts the flow to
        # that paper to 1.
        for pap2 in g2:
            self.start_inds.append(self.n_rev + self.n_pap + 2 + pap2)
            self.end_inds.append(self.n_rev + pap2)
            self.caps.append(1)
            self.costs.append(0)

        # Now, for each assignment in the g1 group, reverse the flow.
        revs, paps1 = np.nonzero(self.solution[:, g1])
        assignment_to_give = set()
        added = set()
        pg2_to_minaff = defaultdict(lambda: np.inf)
        for i in range(np.size(revs)):
            rev = int(revs[i])
            pap = g1[paps1[i]]
            assert(self.solution[rev, pap] == 1.0)
            self.start_inds.append(self.n_rev + pap)
            self.end_inds.append(rev)
            self.caps.append(1)
            # self.costs.append(int(1.0 + 10000 * self.affs[rev, pap]))
            self.costs.append(0)
            assignment_to_give.add(rev)

            # and now connect this reviewer to each paper in g2 if that
            # reviewer has not already been assigned to that paper.
            if rev not in added:
                for pap2 in g2:
                    if self.solution[rev, pap2] == 0.0:
                        # assert((rev, pap2) not in added)
                        # added.add((rev, pap2))

                        self.start_inds.append(rev)

                        ##############################
                        # Route through another node to choose 1 rev
                        self.end_inds.append(self.n_rev + self.n_pap + 2 + pap2)
                        # self.end_inds.append(self.n_rev + pap2)
                        pg2_to_minaff[pap2] = min(pg2_to_minaff[pap2],
                                                  self.affs[rev, pap2])

                        self.caps.append(1)
                        # self.costs.append(
                        #     int(-1.0 - 10000 * self.affs[rev, pap2]))
                        self.costs.append(0)
                added.add(rev)
        # For each paper in g2, reverse the flow to assigned revs only if the
        # reversal, plus the min edge coming in from G1 wouldn't violate ms.
        revs, paps2 = np.nonzero(self.solution[:, g2])
        for i in range(np.size(revs)):
            rev = int(revs[i])
            pap = g2[paps2[i]]
            pap_score = pap_scores[pap]
            assert(self.solution[rev, pap] == 1.0)
            min_in = pg2_to_minaff[pap]
            rp_aff = self.affs[rev, pap]
            if min_in < np.inf and (self.makespan - self.maxaff) <= (pap_score + min_in - rp_aff):
                # print(self.makespan - self.maxaff, (pap_score + min_in - rp_aff), pap_score, min_in, rp_aff)
                self.start_inds.append(self.n_rev + pap)
                self.end_inds.append(rev)
                self.caps.append(1)
                # self.costs.append(int(1.0 + 10000 * self.affs[rev, pap]))
                # self.costs.append(1)
                # TODO(AK): below??
                self.costs.append(0)
                # print('happened')
                assignment_to_give.add(rev)

        # For each reviewer, connect them to a paper in g3 if not assigned.
        for rev in assignment_to_give:#range(self.n_rev):
            for pap3 in g3:
                # rs = np.nonzero(self.solution[:, pap3])[0]
                # nnz_rs = np.nonzero(self.affs[:, pap3])[0]
                # print(nnz_rs)
                # print(self.affs[nnz_rs, pap3])
                # print(pap3, pap_scores[pap3], self.affs[rs[0], pap3], self.affs[rs[1], pap3])

                if self.solution[rev, pap3] == 0.0:
                    self.start_inds.append(rev)
                    self.end_inds.append(self.n_rev + pap3)
                    self.caps.append(1)
                    lb = self.makespan - self.maxaff
                    pap_score = pap_scores[pap3]
                    if self.affs[rev, pap3] + pap_score >= lb:
                        self.costs.append(-1)
                    else:
                        self.costs.append(
                            int((self.maxaff - self.affs[rev, pap3]) * 10000))

        flow = int(min(np.size(g3), np.size(g1)))
        self.supplies = np.zeros(self.n_rev + self.n_pap + 2)
        self.supplies[self.source] = flow    #int(np.size(g3))
        self.supplies[self.sink] = -flow     #-int(np.size(g3))

        for i in range(len(self.start_inds)):
            self.min_cost_flow.AddArcWithCapacityAndUnitCost(
                self.start_inds[i], self.end_inds[i], self.caps[i],
                self.costs[i])
        for i in range(len(self.supplies)):
            self.min_cost_flow.SetNodeSupply(i, int(self.supplies[i]))

    def _construct_ms_improvement_network_new(self, g1, g2, g3):
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
        self._refresh_internal_vars()
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
        added = set()
        for i in range(np.size(revs)):
            rev = int(revs[i])
            pap = g1[paps1[i]]
            assert(self.solution[rev, pap] == 1.0)
            self.start_inds.append(self.n_rev + pap)
            self.end_inds.append(rev)
            self.caps.append(1)
            # TODO(AK): make this cost something so that we want to unassign
            # relative weak revs
            # self.costs.append(int(1.0 + 10000 * self.weights[rev, pap]))
            self.costs.append(0)
            added.add(rev)

        #     # and now connect this reviewer to each paper in g2 if that
        #     # reviewer has not already been assigned to that paper.
        #     if rev not in added:
        #         for pap2 in g2:
        #             if self.solution[rev, pap2] == 0.0:
        #                 assert((rev, pap2) not in added)
        #                 added.add((rev, pap2))
        #
        #                 self.start_inds.append(rev)
        #                 self.end_inds.append(self.n_rev + pap2)
        #                 self.caps.append(1)
        #                 self.costs.append(
        #                     int(-1.0 - 10000 * self.affs[rev, pap2]))
        #         added.add(rev)
        # # For each paper in g2, reverse the flow to assigned revs.
        # revs, paps2 = np.nonzero(self.solution[:, g2])
        # for i in range(np.size(revs)):
        #     rev = int(revs[i])
        #     pap = g2[paps2[i]]
        #     assert(self.solution[rev, pap] == 1.0)
        #     self.start_inds.append(self.n_rev + pap)
        #     self.end_inds.append(rev)
        #     self.caps.append(1)
        #     # self.costs.append(int(1.0 + 10000 * self.weights[rev, pap]))
        #     self.costs.append(1)
        #     # TODO(AK): below??
        #     # self.costs.append(0)

        # For each rev in added, connect them to a paper in g3 if not assigned.
        for rev in added:
            for pap3 in g3:
                if self.solution[rev, pap3] == 0.0:
                    self.start_inds.append(rev)
                    self.end_inds.append(self.n_rev + pap3)
                    self.caps.append(1)
                    self.costs.append(
                        int(-1.0 - 10000 * self.affs[rev, pap3]))

        flow = int(min(np.size(g3), np.size(g1)))
        # flow = int(np.size(g3))
        self.supplies = np.zeros(self.n_rev + self.n_pap + 2)
        self.supplies[self.source] = flow    #int(np.size(g3))
        self.supplies[self.sink] = -flow     #-int(np.size(g3))
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
                        # flow goes from tail to head
                        head = self.min_cost_flow.Head(arc)
                        tail = self.min_cost_flow.Tail(arc)
                        if head >= self.n_rev + self.n_pap + 2:
                            # this is an edge that restricts flow to a paper
                            pap = head - (self.n_rev + self.n_pap + 2)
                            assert(tail <= self.n_rev)
                            rev = tail
                            assert(self.solution[rev, pap] == 0.0)
                            self.solution[rev, pap] = 1.0
                        elif tail >= self.n_rev + self.n_pap + 2:
                            continue
                        elif head >= self.n_rev:
                            pap = head - self.n_rev
                            rev = tail
                            assert(self.solution[rev, pap] == 0.0)
                            self.solution[rev, pap] = 1.0
                            num_un += 1
                        else:
                            rev = head
                            pap = tail - self.n_rev
                            assert(self.solution[rev, pap] == 1.0)
                            self.solution[rev, pap] = 0.0

                    # if self.min_cost_flow.Flow(arc) > 0:
                    #
                    #     if self.min_cost_flow.UnitCost(arc) > 0:
                    #         pap = self.min_cost_flow.Tail(arc) - self.n_rev
                    #         rev = self.min_cost_flow.Head(arc)
                    #         assert(self.solution[rev, pap] == 1.0)
                    #         self.solution[rev, pap] = 0.0
                    #         num_un += 1
                    #     elif self.min_cost_flow.UnitCost(arc) < 0:
                    #         rev = self.min_cost_flow.Tail(arc)
                    #         pap = self.min_cost_flow.Head(arc) - self.n_rev
                    #         assert(self.solution[rev, pap] == 0.0)
                    #         self.solution[rev, pap] = 1.0
                    #     else:
                    #         assert(False)
            # assert (np.sum(self.solution) == np.sum(self.coverages))
            # print('NUM UNASSIGNED %d' % num_un)
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
            assert np.all(np.sum(self.solution, axis=1) <= self.loads)
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
        print('solving with MS=%s' % self.makespan)
        self._refresh_internal_vars()
        if np.sum(self.solution) != np.sum(self.coverages):
            self._construct_and_solve_validifier_network()
        assert(np.sum(self.solution) == np.sum(self.coverages))
        g1, g2, g3 = self._grp_paps_by_ms()
        old_g1, old_g2, old_g3 = set(g1), set(g2), set(g3)
        print('G1: %s, G3: %s' % (np.size(g1), np.size(g3)))
        if np.size(g1) > 0 and np.size(g3) > 0:
            self._refresh_internal_vars()
            w_revs, w_paps = self._worst_reviewer(g3)
            assert (np.sum(self.solution) == np.sum(self.coverages))
            assert(len(set(w_paps)) == len(w_paps))
            self.solution[w_revs, w_paps] = 0.0

            self._construct_ms_improvement_network(g1, g2, g3)
            self.solve_ms_improvement()
            g1, _, _ = self._grp_paps_by_cov()
            self._construct_and_solve_validifier_network()

            # Checks:
            g1, g2, g3 = self._grp_paps_by_ms()
            print(old_g3.difference(g3))
            for p in g3:
                print(p in old_g2, p in old_g1)
            assert(len(g3) <= len(old_g3))
            return True, np.size(g1), np.size(g3)
        else:
            return False, np.size(g1), np.size(g3)

    def _construct_graph_and_solve(self, n_rev, n_pap, _caps, _covs, ws, flow):
        """Flow graph"""
        start_inds = []
        end_inds = []
        caps = []
        costs = []
        source = n_rev + n_pap
        sink = n_rev + n_pap + 1

        # edges from source to revs.
        for i in range(n_rev):
            start_inds.append(source)
            end_inds.append(i)
            caps.append(int(_caps[i]))
            costs.append(0)

        # edges from rev to pap.
        for i in range(n_rev):
            for j in range(n_pap):
                start_inds.append(i)
                end_inds.append(n_rev + j)
                if self.solution[i, j] == 1:
                    caps.append(0)
                else:
                    caps.append(1)
                # Costs must be integers. Also, we have affinities so make
                # the "costs" negative affinities.
                costs.append(int(-1.0 - 10000 * ws[i, j]))

        # edges from pap to sink.
        for j in range(n_pap):
            start_inds.append(n_rev + j)
            end_inds.append(sink)
            caps.append(int(_covs[j]))
            costs.append(0)

        supplies = np.zeros(n_rev + n_pap + 2)
        supplies[source] = int(flow)
        supplies[sink] = int(-flow)

        # Add arcs.
        mcf = pywrapgraph.SimpleMinCostFlow()
        for i in range(len(start_inds)):
            mcf.AddArcWithCapacityAndUnitCost(
                start_inds[i], end_inds[i], caps[i],
                costs[i])
        for i in range(len(supplies)):
            mcf.SetNodeSupply(i, int(supplies[i]))

        # Solve.
        if mcf.Solve() == mcf.OPTIMAL:
            for arc in range(mcf.NumArcs()):
                # Can ignore arcs leading out of source or into sink.
                if mcf.Tail(arc) != source and mcf.Head(arc) != sink:
                    if mcf.Flow(arc) > 0:
                        rev = mcf.Tail(arc)
                        pap = mcf.Head(arc) - n_rev
                        assert(self.solution[rev, pap] == 0.0)
                        self.solution[rev, pap] = 1.0
            self.solved = True
        else:
            raise Exception('There was an issue with the min cost flow input.')

    def find_ms(self):
        """Find an the highest possible makespan.

        Perform a binary search on the makespan value. Solve the RAP with each
        makespan value and return the solution corresponding to the makespan
        which achieves the largest minimum paper score.

        Args:
            None

        Return:
            Highest feasible makespan value found.
        """
        mn = 0.0
        mx = np.max(self.affs) * np.max(self.coverages)
        # ms = (mx - mn) / 2.0
        best = mx
        best_worst_pap_score = 0.0
        for ms in np.arange(mn, mx + mx/100.0, mx / 100.0):
            print('ITERATION ms %s' % ms)
            self.makespan = ms
            can_improve, s1, s3 = self.try_improve_ms()
            num_itrs = 0
            prev_s1, prev_s3 = -1, -1
            while can_improve and (prev_s1 != s1 or prev_s3 != s3):
                prev_s1, prev_s3 = s1, s3
                can_improve, s1, s3 = self.try_improve_ms()
                num_itrs += 1
            worst_pap_score = np.min(np.sum(self.solution * self.affs,
                                            axis=0))
            print('best worst paper score %s worst score %s' % (best_worst_pap_score, worst_pap_score) )
            if worst_pap_score > best_worst_pap_score:
                best_worst_pap_score = worst_pap_score
                best = ms
        self.makespan = best

        # for i in range(10):
        #     print('ITERATION %s ms %s' % (i, ms))
        #     can_improve, s1, s3 = self.try_improve_ms()
        #     num_itrs = 0
        #     prev_s1, prev_s3 = -1, -1
        #     while can_improve and (prev_s1 != s1 or prev_s3 != s3):
        #         prev_s1, prev_s3 = s1, s3
        #         can_improve, s1, s3 = self.try_improve_ms()
        #         num_itrs += 1
        #
        #     worst_pap_score = np.min(np.sum(self.solution * self.weights,
        #                                     axis=0))
        #     print('best worst paper score %s worst score %s' % (best_worst_pap_score, worst_pap_score) )
        #     if best_worst_pap_score >= worst_pap_score:
        #         mx = ms
        #         ms -= (ms - mn) / 2.0
        #     else:
        #         assert(worst_pap_score > best_worst_pap_score)
        #         best = ms
        #         best_worst_pap_score = worst_pap_score
        #         mn = ms
        #         ms += (mx - ms) / 2.0
        #
        #     self.makespan = ms
        print('Best found %s' % best)
        print('Best Worst Paper Score found %s' % best_worst_pap_score)
        return best

    def solve(self, mn=0, mx=-1, itr=10):
        """Find a makespan and solve flow.

        Run a binary search to find best makespan and return the corresponding
        solution.

        Args:
            mn - the minimum feasible makespan (optional).
            mx - the maximum possible makespan( optional).
            itr - the number of iterations of binary search for the makespan.

        Returns:
            The solution as a matrix.
        """
        ms = self.find_ms()
        self.makespan = ms

        can_improve, s1, s3 = self.try_improve_ms()
        num_itrs = 0
        prev_s1, prev_s3 = -1, -1
        while can_improve and (prev_s1 != s1 or prev_s3 != s3):
            prev_s1, prev_s3 = s1, s3
            can_improve, s1, s3 = self.try_improve_ms()
            num_itrs += 1

        return self.sol_as_mat()
