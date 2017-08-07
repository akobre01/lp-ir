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

        self.src_fwd_costs = np.zeros(self.n_rev)
        self.src_bwd_costs = np.zeros(self.n_rev)
        self.src_caps = loads[:]
        self.sink_fwd_costs = np.zeros(self.n_pap)
        self.sink_bwd_costs = np.zeros(self.n_pap)
        self.sink_caps = coverages[:]
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
        rev_pots = [np.inf] * self.n_rev
        pap_pots = [np.inf] * self.n_pap
        sink_pot = np.inf
        for i in range(self.n_rev + self.n_pap + 3):  # TODO: is it +1 or -1?
            for rev in range(self.n_rev):
                if self.src_caps[rev] > 0 and \
                                rev_pots[rev] > self.src_fwd_costs[rev]:
                    rev_pots[rev] = self.src_fwd_costs[rev]
                for pap in range(self.n_pap):
                    if self.assign[rev, pap] == 0:
                        edge_cost = self.fwd_costs[rev, pap]
                        if pap_pots[pap] > rev_pots[rev] + edge_cost:
                            pap_pots[pap] = rev_pots[rev] + edge_cost
                    else: # assign[rev, pap] == 1
                        edge_cost = self.bwd_costs[rev, pap]
                        if rev_pots[rev] > pap_pots[pap] + edge_cost:
                            rev_pots[rev] = pap_pots[pap] + edge_cost
                    if self.sink_caps[pap] > 0 and sink_pot > pap_pots[pap] \
                                    + self.sink_fwd_costs[pap]:
                        sink_pot = pap_pots[pap] + self.sink_fwd_costs[pap]
                    if self.sink_caps[pap] < self.coverages[pap] and \
                                    pap_pots[pap] > sink_pot \
                                    + self.sink_bwd_costs[pap]:
                        pap_pots[pap] = sink_pot + self.sink_bwd_costs[pap]
        return rev_pots, pap_pots, sink_pot

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
        for rev in range(self.n_rev):
            for pap in range(self.n_pap):
                if self.assign[rev, pap] == 0:
                    self.fwd_costs[rev, pap] += rev_pots[rev] - pap_pots[pap]
                else:  #assign[rev, pap] == 1:
                    self.bwd_costs[rev, pap] += pap_pots[pap] - rev_pots[rev]
        for pap in range(self.n_pap):
            if self.sink_caps[pap] > 0:
                self.sink_fwd_costs[pap] += pap_pots[pap] - sink_pot
            if self.sink_caps[pap] < self.coverages[pap]:
                self.sink_bwd_costs[pap] += sink_pot - pap_pots[pap]

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
        while rev_q or pap_q:
            if rev_q:
                rev = rev_q.pop(0)
                for pap in range(self.n_pap):
                    if self.fwd_costs[rev, pap] == 0 and \
                                    self.assign[rev, pap] == 0:
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
                            return True
                        else:
                            pap_q.append(pap)
            if pap_q:
                pap = pap_q.pop(0)
                for r in range(self.n_rev):
                    if self.assign[r, pap] == 1 and self.bwd_costs[r, pap] == 0:
                        rev_q.append(r)
                        rev_pars[r] = pap
        return False

    def solve(self):
        """Solve matching."""
        found = True
        while found:
            revp, papp, sp = self.compute_potentials()
            self.reduce_costs(revp, papp, sp)
            found = self.augment_assign()


if __name__ == '__main__':
    costs = np.array([[.1, .9, .3],
                      [.1, .4, .2],
                      [.1, .14, .5]])
    m = MFMC(np.array([2, 2, 2]), np.array([2, 2, 2]), costs)
    m.solve()
    print(m.assign)
