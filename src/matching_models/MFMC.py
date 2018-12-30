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
        sink_pot = np.inf

        # Precomute values.
        src_fc = (self.src_caps == 0).astype(int) * np.inf
        src_fc[np.isnan(src_fc)] = 0
        fwd_edges = self.assign * np.inf  # returns inf if already assigned.
        fwd_edges[np.isnan(fwd_edges)] = 0
        bwd_edges = (self.assign == 0).astype(int) * np.inf
        bwd_edges[np.isnan(bwd_edges)] = 0
        aug_fc = 1.0 / self.weights + fwd_edges
        aug_bc = bwd_edges
        # aug_fc = self.fwd_costs + fwd_edges
        # aug_bc = self.bwd_costs + bwd_edges
        fwd_sink_edges = (self.sink_caps == 0).astype(int) * np.inf
        fwd_sink_edges[np.isnan(fwd_sink_edges)] = 0
        bwd_sink_edges = (self.sink_caps == np.array(self.coverages)).astype(
            int) * np.inf
        bwd_sink_edges[np.isnan(bwd_sink_edges)] = 0

        for i in range(self.n_rev + self.n_pap + 3):  # TODO: is it +1 or -1?
            # Costs from src.
            new_rev_pots = np.minimum(rev_pots, src_fc)

            # Backward costs from papers.
            new_rev_pots = np.minimum(new_rev_pots,
                                      np.min(pap_pots + aug_bc, axis=1))

            # Forward costs from revs.
            new_pap_pots = np.minimum(pap_pots,
                                      np.min(new_rev_pots[:, np.newaxis] + \
                                             aug_fc, axis=0))

            # Backwards costs from sink.
            new_pap_pots = np.minimum(new_pap_pots, sink_pot + bwd_sink_edges)

            # Costs to sink.
            new_sink_pot = np.minimum(sink_pot,
                                      np.min(pap_pots + fwd_sink_edges))

            if all(new_rev_pots == rev_pots) and \
                    all(new_pap_pots == pap_pots) and \
                            new_sink_pot == sink_pot:
                return new_rev_pots, new_pap_pots, new_sink_pot
            else:
                rev_pots = new_rev_pots
                pap_pots = new_pap_pots
                sink_pot = new_sink_pot
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
        rev_pot_mat = np.tile(rev_pots[:, np.newaxis], (1, self.n_pap))
        pap_pot_mat = np.tile(pap_pots, (self.n_rev, 1))
        # TODO(AK): note sure which of the reduce costs is correct.
        # self.fwd_costs += (self.assign == 0).astype(int) * (
        #     rev_pot_mat - pap_pot_mat)
        # self.bwd_costs += (self.assign == 1).astype(int) * (
        #     pap_pot_mat - rev_pot_mat)
        # self.sink_fwd_costs += (self.sink_caps > 0).astype(int) * (
        #     pap_pots - sink_pot)
        # self.sink_bwd_costs += (self.sink_caps < self.coverages).astype(int) \
        #                        * (sink_pot - pap_pots)
        fwd_inf = (self.assign == 1).astype(int) * np.inf
        fwd_inf[np.isnan(fwd_inf)] = 0
        bwd_inf = (self.assign == 0).astype(int) * np.inf
        bwd_inf[np.isnan(bwd_inf)] = 0
        sink_fwd_inf = (self.sink_caps == 0).astype(int) * np.inf
        sink_fwd_inf[np.isnan(sink_fwd_inf)] = 0
        sink_bwd_inf = (self.sink_caps == self.coverages).astype(int) * np.inf
        sink_fwd_inf[np.isnan(sink_bwd_inf)] = 0

        self.fwd_costs = (self.assign == 0).astype(int) * (
            rev_pot_mat - pap_pot_mat + 1.0 / self.weights) + fwd_inf
        self.bwd_costs = (self.assign == 1).astype(int) * (
            pap_pot_mat - rev_pot_mat) + bwd_inf
        self.sink_fwd_costs = (self.sink_caps > 0).astype(int) * (
            pap_pots - sink_pot) + sink_fwd_inf
        self.sink_bwd_costs = (self.sink_caps < self.coverages).astype(int) \
                               * (sink_pot - pap_pots) + sink_bwd_inf
        print(sink_pot)
        print(rev_pots)
        print(pap_pots)
        print(sink_pot - pap_pots + sink_bwd_inf)
        print(self.sink_caps)
        assert ((self.fwd_costs >= 0).all())
        assert ((self.bwd_costs >= 0).all())
        assert ((self.sink_fwd_costs >= 0).all())
        assert ((self.sink_bwd_costs >= 0).all())

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
                        # Update everything along the path
                        p = pap
                        r = pap_pars[p]
                        self.assign[r, p] = 1
                        self.sink_caps[pap] -= 1

                        rp = rev_pars[r]
                        while rp != -1:   # src val.
                            p = rev_pars[r]
                            assert(self.assign[r, p] == 1)
                            self.assign[r, p] = 0
                            r = pap_pars[p]
                            assert(self.assign[r, p] == 0)
                            self.assign[r, p] = 1
                            rp = rev_pars[r]
                        assert(rp == -1)
                        self.src_caps[r] -= 1  # revs par is the src.
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
        print(self.src_caps, np.sum(self.src_caps))
        print(self.sink_caps, np.sum(self.sink_caps))
        return False

    def solve(self):
        """Solve matching."""
        found = True
        total = np.sum(self.coverages)

        while found:
            revp, papp, sp = self.compute_potentials()
            self.reduce_costs(revp, papp, sp)
            found = self.augment_assign()
            another_aug_path = True
            while another_aug_path:
                s = np.sum(self.assign)
                if s % 500 == 0:
                    print('Assigned %s of %s' % (s, total))
                another_aug_path = self.augment_assign()
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
