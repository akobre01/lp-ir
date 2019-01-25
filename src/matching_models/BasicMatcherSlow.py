import numpy as np
import time
import uuid

from gurobipy import *


class BasicMatcherSlow(object):
    """The basic paper matching formulation"""
    # TODO(AK): We should add reviewer lower bounds to this.
    def __init__(self, loads, coverages, weights):
        """Initialize the BasicMatcher

        Args:
            loads - a list of integers specifying the maximum number of papers
                  for each reviewer.
            coverages - a list of integers specifying the number of reviews per
                 paper.
            weights - the affinity matrix (np.array) of papers to reviewers.
                   Rows correspond to reviewers and columns correspond to
                   papers.

        Returns:
            initialized matcher.
        """
        self.n_rev = np.size(weights, axis=0)
        self.n_pap = np.size(weights, axis=1)
        self.loads = loads
        self.coverages = coverages

        assert(np.sum(coverages) <= np.sum(loads))

        self.weights = weights
        self.id = uuid.uuid4()
        self.m = Model("%s: basic matcher" % str(self.id))
        # TODO(AK): can we make a makespan constraint per paper?
        self.solution = None

        self.m.setParam('OutputFlag', 0)

        # primal variables
        start = time.time()
        self.lp_vars = []
        for i in range(self.n_rev):
            self.lp_vars.append([])
            for j in range(self.n_pap):
                self.lp_vars[i].append(self.m.addVar(vtype=GRB.BINARY,
                                                     name=self.var_name(i, j),
                                                     obj=self.weights[i][j]))
        self.m.update()
        self.m.setObjective(self.m.getObjective(), GRB.MAXIMIZE)
        self.m.update()
        print('Set variables %s' % (time.time() - start))

        # Set the objective.
        # start = time.time()
        # obj = LinExpr()
        # for i in range(self.n_rev):
        #     for j in range(self.n_pap):
        #         obj += self.weights[i][j] * self.lp_vars[i][j]
        # self.m.setObjective(sum(self.lp_vars), GRB.MAXIMIZE)
        # print('Objective %s' % (time.time() - start))

        start = time.time()
        # Reviewer constraints.
        for r, l in enumerate(self.loads):
            self.m.addConstr(sum(self.lp_vars[r]) <= l, "r" + str(r))

        # Paper constraints.
        for p, cov in enumerate(self.coverages):
            self.m.addConstr(sum([self.lp_vars[i][p]
                                  for i in range(self.n_rev)]) == cov,
                             "p" + str(p))
        self.m.update()
        print('Constraints %s' % (time.time() - start))

    @staticmethod
    def var_name(i, j):
        """The name of the variable corresponding to reviewer i and paper j."""
        return "x_" + str(i) + "," + str(j)

    @staticmethod
    def indices_of_var(v):
        """Get the indices associated with a particular var_name (above)."""
        name = v.varName
        indices = name[2:].split(',')
        i, j = int(indices[0]), int(indices[1])
        return i, j

    def sol_as_dict(self):
        """Return the solution to the optimization as a dictionary.

        If the matching has not be solved optimally or suboptimally, then raise
        an exception.

        Args:
            None.

        Returns:
            A dictionary from var_name to value (either 0 or 1)
        """
        if self.m.status == GRB.OPTIMAL or self.m.status == GRB.SUBOPTIMAL:
            _sol = {}
            for v in self.m.getVars():
                _sol[v.varName] = v.x
            return _sol
        else:
            raise Exception(
                'You must have solved the model optimally or suboptimally '
                'before calling this function.')

    def solve(self):
        """Solve the ILP.

        If we were not able to solve the ILP optimally or suboptimally, then
        raise an error.  If we are able to solve the ILP, save the solution.

        Args:
            None.

        Returns:
            An np array corresponding to the solution.
        """
        start = time.time()
        self.m.optimize()
        print('Time to solve %s' % (time.time() - start))
        if self.m.status == GRB.OPTIMAL:
            self.solution = self.sol_as_mat()
        return self.solution

    def sol_as_mat(self):
        if self.m.status == GRB.OPTIMAL or self.m.status == GRB.SUBOPTIMAL:
            solution = np.zeros((self.n_rev, self.n_pap))
            for v in self.m.getVars():
                i, j = self.indices_of_var(v)
                solution[i, j] = v.x
            self.solution = solution
            return solution
        else:
            raise Exception(
                'You must have solved the model optimally or suboptimally '
                'before calling this function.')

    def status(self):
        """Return the status code of the solver."""
        return self.m.status

    def turn_on_verbosity(self):
        """Turn on vurbosity for debugging."""
        self.m.setParam('OutputFlag', 1)

    def objective_val(self):
        """Get the objective value of a solved lp."""
        return self.m.ObjVal


if __name__ == "__main__":
    ws = np.genfromtxt(
        '../../data/train/200-200-2.0-5.0-skill_based/weights.txt')
    init_makespan = 1.5

    a = [3] * np.size(ws, axis=0)
    b = [3] * np.size(ws, axis=1)

    x = BasicMatcherSlow(a, b, ws, init_makespan)
    s = time.time()
    x.solve()
    print(time.time() - s)
    print("[done.]")
