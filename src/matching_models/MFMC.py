import numpy as np
import uuid


class MFMC(object):
    """Solves makespan paper matching using max flow min cost algorithm."""
    def __init__(self, loads, coverages, weights, makespan=0):
        """Initialize a makespan matcher

        Args:
            loads - a list of integers specifying the maximum number of papers
                  for each reviewer.
            coverages - a list of integers specifying the number of reviews per
                 paper.
            weights - the affinity matrix (np.array) of papers to reviewers.
                   Rows correspond to reviewers and columns correspond to
                   papers.
            makespan - optional initial makespan value.

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
        self.solution = np.zeros((self.n_rev, self.n_pap))
        self.costs = np.floor(np.log2(weights))  # costs are all negative.
        self.r_gain = np.exp2(self.costs)
        self.solved = False

        self.src_fwd_costs = np.zeros(self.n_rev)
        self.src_bwd_costs = np.zeros(self.n_rev)
        self.src_caps = np.array(loads[:])
        self.sink_fwd_costs = np.zeros(self.n_pap)
        self.sink_bwd_costs = np.zeros(self.n_pap)
        self.sink_caps = np.array(coverages[:])
        self.fwd_costs = 1.0 / weights[:]
        self.bwd_costs = np.zeros(np.shape(self.fwd_costs))
        self.assign = np.zeros((self.n_rev, self.n_pap))

    def compute_potentials(self):
        """Compute potentials for each node in the network.

        The potential of a node is the cheapest way to get there.  We compute
        potentials using the Bellman ford algorithm (although it is conceivable
        that there is a faster way to do it).

        Args:
            None

        Returns:
            Two vectors of reviewer and paper potentials and the sink potential.
        """
        rev_pots = np.ones(self.n_rev) * np.inf
        pap_pots = np.ones(self.n_pap) * np.inf
        rev_pots2 = np.ones(self.n_rev) * np.inf
        pap_pots2 = np.ones(self.n_pap) * np.inf
        sink_pot = np.inf
        sink_pot2 = np.inf

        # Precomute values.
        src_fc = np.maximum(0, (1.0 - self.src_caps) * np.inf)
        src_fc[np.isnan(src_fc)] = 0
        fwd_edges = self.assign * np.inf  # returns inf if already assigned.
        fwd_edges[np.isnan(fwd_edges)] = 0
        bwd_edges = (self.assign - 1.0) * -np.inf #  inf is not assigned
        bwd_edges[np.isnan(bwd_edges)] = 0
        aug_fc = self.fwd_costs + fwd_edges
        aug_bc = self.bwd_costs + bwd_edges
        fwd_sink_edges = np.maximum(0, (1.0 - self.sink_caps)) * np.inf
        fwd_sink_edges[np.isnan(fwd_sink_edges)] = 0
        bwd_sink_edges = np.maximum(0, self.sink_caps - np.array(self.coverages) + 1.0) * np.inf
        bwd_sink_edges[np.isnan(bwd_sink_edges)] = 0

        # print(self.assign)
        # print(self.fwd_costs)
        # print(self.bwd_costs)
        # print(src_fc)
        for i in range(self.n_rev + self.n_pap + 3):  # TODO: is it +1 or -1?
            print(i)
            # print(sink_pot, rev_pots, pap_pots)
            # print(sink_pot2, rev_pots2, pap_pots2)
            # Costs from src.
            new_rev_pots = np.minimum(rev_pots2, src_fc)

            # Backward costs from papers.
            new_rev_pots = np.minimum(new_rev_pots,
                                      np.min(pap_pots2 + aug_bc, axis=1))

            # Forward costs from revs.
            new_pap_pots = np.minimum(pap_pots2,
                                      np.min(new_rev_pots[:, np.newaxis] + aug_fc, axis=0))

            # Backwards costs from sink.
            new_pap_pots = np.minimum(new_pap_pots, sink_pot2 + bwd_sink_edges)

            # Costs to sink.
            new_sink_pot = np.minimum(sink_pot2,
                                      np.min(pap_pots2 + fwd_sink_edges))

            if all(new_rev_pots == rev_pots2) and \
                    all(new_pap_pots == pap_pots2) and \
                            new_sink_pot == sink_pot2:
                return new_rev_pots, new_pap_pots, new_sink_pot
            else:
                rev_pots2 = new_rev_pots
                pap_pots2 = new_pap_pots
                sink_pot2 = new_sink_pot

            # for rev in range(self.n_rev):
            #     if self.src_caps[rev] > 0 and \
            #                     rev_pots[rev] > self.src_fwd_costs[rev]:
            #         rev_pots[rev] = self.src_fwd_costs[rev]
            #     for pap in range(self.n_pap):
            #         if self.assign[rev, pap] == 0:
            #             edge_cost = self.fwd_costs[rev, pap]
            #             if pap_pots[pap] > rev_pots[rev] + edge_cost:
            #                 pap_pots[pap] = rev_pots[rev] + edge_cost
            #         else: # assign[rev, pap] == 1
            #             edge_cost = self.bwd_costs[rev, pap]
            #             if rev_pots[rev] > pap_pots[pap] + edge_cost:
            #                 rev_pots[rev] = pap_pots[pap] + edge_cost
            #         if self.sink_caps[pap] > 0 and sink_pot > pap_pots[pap] \
            #                         + self.sink_fwd_costs[pap]:
            #             sink_pot = pap_pots[pap] + self.sink_fwd_costs[pap]
            #         if self.sink_caps[pap] < self.coverages[pap] and \
            #                         pap_pots[pap] > sink_pot \
            #                         + self.sink_bwd_costs[pap]:
            #             pap_pots[pap] = sink_pot + self.sink_bwd_costs[pap]
        #return rev_pots, pap_pots, sink_pot
        return rev_pots2, pap_pots2, sink_pot2

    def reduce_costs(self, rev_pots, pap_pots, sink_pot):
        """Compute the reduced cost of every edge.

        The reduce cost is equal to the cost of the current edge, plus the
        potential of its beginning - the potential at its endpoint. The reduce
        costs can be thought of as the cost of the edge en route to the sink
        relative to the cheapest path to the sink.

        Args:
            rev_pots - an array of reviewer potentials.
            pap_pots - an array of paper potentials.
            sink_pot - the sink potential.

        Returns:
            Nothing - but updates fwd and bwd costs of this class.

        """
        rev_pot_mat = np.tile(rev_pots[:, np.newaxis], (1, self.n_pap))
        pap_pot_mat = np.tile(pap_pots, (self.n_rev, 1))
        self.fwd_costs += (self.assign == 0).astype(int) * (rev_pot_mat - pap_pot_mat)
        self.bwd_costs += (self.assign == 1).astype(int) * (pap_pot_mat - rev_pot_mat)
        self.sink_fwd_costs += (self.sink_caps > 0).astype(int) * (
        pap_pots - sink_pot)
        self.sink_bwd_costs += (self.sink_caps == self.coverages).astype(int) * (pap_pots - sink_pot)

        # for rev in range(self.n_rev):
        #     for pap in range(self.n_pap):
        #         if self.assign[rev, pap] == 0:
        #             self.fwd_costs[rev, pap] += rev_pots[rev] - pap_pots[pap]
        #         else:  #assign[rev, pap] == 1:
        #             self.bwd_costs[rev, pap] += pap_pots[pap] - rev_pots[rev]
        # for pap in range(self.n_pap):
        #     if self.sink_caps[pap] > 0:
        #         self.sink_fwd_costs[pap] += pap_pots[pap] - sink_pot
        #     if self.sink_caps[pap] < self.coverages[pap]:
        #         self.sink_bwd_costs[pap] += sink_pot - pap_pots[pap]

    def augment_assign(self):
        """Augment the set of assignments.

        Once the reduce costs have been computed, we simultaneously compute all
        shortest paths to the sink using the ford-fulkerson algorithm.

        Args:
            None.

        Returns:
            Returns whether any path was augmented. Also updates the self.assign
            variables.
        """
        rev_q = []
        pap_q = []
        rev_pars = [None] * self.n_rev
        pap_pars = [None] * self.n_pap
        for rev in range(self.n_rev):
            if self.src_caps[rev] > 0 and self.src_fwd_costs[rev] == 0:
                rev_q.append(rev)
                rev_pars[rev] = -1    # src val.
        unexplored_rs = np.ones(self.n_rev)
        unexplored_ps = np.ones(self.n_pap)
        while rev_q or pap_q:
            if rev_q:
                rev = rev_q.pop(0)
                unexplored_rs[rev] = 0
                unassigned = (self.assign[rev, :] == 0).astype(int)
                zero_edges = (self.fwd_costs[rev, :] == 0).astype(int)
                zero_and_unassigned = zero_edges * unassigned * unexplored_ps
                for pap in np.argwhere(zero_and_unassigned):
                    pap = pap[0]
                    pap_pars[pap] = rev
                    if self.sink_caps[pap] > 0:
                        self.sink_caps[pap] -= 1

                        # Update everything along the path
                        p = pap
                        r = pap_pars[p]
                        rp = rev_pars[r]
                        if rp == -1:
                            self.src_caps[r] -= 1  # revs par is the src.
                        self.assign[r, p] = 1
                        while rp != -1:   # src val.
                            p = rev_pars[r]
                            self.assign[r, p] = 0
                            r = pap_pars[p]
                            self.assign[r, p] = 1
                            rp = rev_pars[r]
                            print(r, p, rp)
                        return True
                    else:
                        pap_q.append(pap)
            if pap_q:
                pap = pap_q.pop(0)
                unexplored_ps[pap] = 0
                assigned = (self.assign[:, pap] == 1).astype(int)
                zero_b_edges = (self.bwd_costs[:, pap] == 0).astype(int)
                zero_and_assigned = assigned * zero_b_edges * unexplored_rs
                for r in np.argwhere(zero_and_assigned):
                    r = r[0]
                    rev_q.append(r)
                    rev_pars[r] = pap
        return False

    def solve(self):
        """Solve matching."""
        found = True
        total = np.sum(self.coverages)

        while found:
            revp, papp, sp = self.compute_potentials()
            print("POTENTIALS COMPUTED")
            self.reduce_costs(revp, papp, sp)
            print("COSTS REDUCED")
            found = self.augment_assign()
            another_aug_path = True
            while another_aug_path:
                print('%s of %s' % (np.sum(self.assign), total))
                another_aug_path = self.augment_assign()
                print("AUGMENTED")
        self.solved = True

    def sol_as_mat(self):
        if self.solved:
            return self.assign
        else:
            raise Exception(
                'You must have solved the model optimally or suboptimally '
                'before calling this function.')


if __name__ == '__main__':
    costs = np.array([[.1, .9, .3],
                      [.1, .4, .2],
                      [.1, .14, .5],
                      [.7, .1, .7]])
    m = MFMC(np.array([2, 2, 2, 2]), np.array([2, 2, 2]), costs)
    m.solve()
    print(m.assign)
