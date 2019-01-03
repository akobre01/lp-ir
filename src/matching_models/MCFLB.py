from ortools.graph import pywrapgraph

import numpy as np
import uuid


class MCFLB(object):
    """Min cost flow with lower bounds for reviewer assignment problem."""
    def __init__(self, loads, loads_lb, coverages, weights):
        """Initialize a makespan matcher

        Args:
            loads - a list of integers specifying the maximum number of papers
                  for each reviewer.
            loads_lb - a list of integers specifying the min number of papers
                  for each reviewer.
            coverages - a list of integers specifying the number of reviews per
                 paper.
            weights - the affinity matrix (np.array) of papers to reviewers.
                   Rows correspond to reviewers and columns correspond to
                   papers.

        Returns:
            initialized makespan matcher.
        """
        self.n_rev = np.size(weights, axis=0)
        self.n_pap = np.size(weights, axis=1)
        self.loads = loads
        self.loads_lb = loads_lb
        self.coverages = coverages
        self.weights = weights
        self.id = uuid.uuid4()
        self.solution = np.zeros((self.n_rev, self.n_pap))
        self.solved = False

    def solve(self):
        """Solve with lower bounds.

        First construct a flow and solve with capacities equal to the lower
        bounds. Then, construct a graph that routes the residual flow to papers.
        The result should be that each paper is assigned the correct number of
        papers and that each reviewer is assigned to at least its lower bound
        number of papers.
        """
        # First solve flow with lower bounds as caps.
        flow = np.sum(self.loads_lb)
        self._construct_graph_and_solve(self.n_rev, self.n_pap, self.loads_lb,
                                        self.coverages, self.weights, flow)
        # Now compute the residual flow that must be routed so that each paper
        # is sufficiently reviewed. Also compute residual loads and coverages.
        r_loads = [self.loads[i] - self.loads_lb[i] for i in range(self.n_rev)]
        lb_sol = self.sol_as_mat().copy()
        assiged = np.sum(lb_sol, axis=0)
        assert(len(assiged) == self.n_pap)
        r_covs = [self.coverages[i] - assiged[i] for i in range(self.n_pap)]
        flow = sum(r_covs)
        self._construct_graph_and_solve(self.n_rev, self.n_pap, r_loads, r_covs,
                                        self.weights, flow)
        # Finally, combine first sol with new sol
        sol = self.sol_as_mat()
        assert(np.all(np.sum(sol, axis=0) == self.coverages))
        assert (np.all(np.sum(sol, axis=1) <= self.loads))
        assert (np.all(np.sum(sol, axis=1) >= self.loads_lb))
        return sol

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
                        self.solution[rev, pap] = 1.0
            self.solved = True
        else:
            print('There was an issue with the min cost flow input.')

    # def solve(self):
    #     """Solve matching."""
    #     if self.min_cost_flow.Solve() == self.min_cost_flow.OPTIMAL:
    #         for arc in range(self.min_cost_flow.NumArcs()):
    #             # Can ignore arcs leading out of source or into sink.
    #             if self.min_cost_flow.Tail(arc) != self.source and \
    #                             self.min_cost_flow.Head(arc) != self.sink:
    #                 if self.min_cost_flow.Flow(arc) > 0:
    #                     rev = self.min_cost_flow.Tail(arc)
    #                     pap = self.min_cost_flow.Head(arc) - self.n_rev
    #                     self.solution[rev, pap] = 1.0
    #         self.solved = True
    #     else:
    #         print('There was an issue with the min cost flow input.')

    def sol_as_mat(self):
        if self.solved:
            return self.solution
        else:
            raise Exception(
                'You must have solved the model optimally or suboptimally '
                'before calling this function.')
