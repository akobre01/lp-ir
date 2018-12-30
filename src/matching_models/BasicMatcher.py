import numpy as np
import time
import uuid

from gurobipy import *


class BasicMatcher(object):
    """The basic paper matching formulation"""
    # TODO(AK): We should add reviewer lower bounds to this.
    def __init__(self, loads, coverages, weights, loads_lb=None):
        """Initialize the BasicMatcher

        Args:
            loads - a list of integers specifying the maximum number of papers
                  for each reviewer.
            coverages - a list of integers specifying the number of reviews per
                 paper.
            weights - the affinity matrix (np.array) of papers to reviewers.
                   Rows correspond to reviewers and columns correspond to
                   papers.
            loads_lb - a list of integers specifying the min number of papers
                  for each reviewer (optional).

        Returns:
            initialized matcher.
        """
        self.n_rev = np.size(weights, axis=0)
        self.n_pap = np.size(weights, axis=1)
        self.loads = loads
        self.loads_lb = loads_lb
        self.coverages = coverages

        assert(np.sum(coverages) <= np.sum(loads))
        if loads_lb is not None:
            assert(np.sum(coverages) >= np.sum(loads_lb))

        self.weights = weights
        self.id = uuid.uuid4()
        self.m = Model("%s: basic matcher" % str(self.id))
        # TODO(AK): can we make a makespan constraint per paper?
        self.solution = None

        self.m.setParam('OutputFlag', 0)

        # Primal vars.
        start = time.time()
        self.lp_vars = self.m.addVars(self.n_rev, self.n_pap, vtype=GRB.BINARY,
                                      name='x')
        self.m.update()
        print('Time to add vars %s' % (time.time() - start))

        # Objective.
        start = time.time()
        coeff = list(self.weights.flatten())
        print('flatten %s' % (time.time() - start))

        start = time.time()
        coeff = dict(zip(self.lp_vars.keys(), coeff))
        print('zip %s' % (time.time() - start))

        start = time.time()
        obj = self.lp_vars.prod(coeff)
        print('prod %s' % (time.time() - start))

        start = time.time()
        self.m.setObjective(obj, GRB.MAXIMIZE)
        print('Time to set objective %s' % (time.time() - start))

        # Constraints.
        start = time.time()
        self.m.addConstrs((self.lp_vars.sum(r, '*') <= l
                           for r, l in enumerate(self.loads)))
        self.m.addConstrs((self.lp_vars.sum('*', p) == c
                           for p, c in enumerate(self.coverages)))
        if self.loads_lb is not None:
            self.m.addConstrs((self.lp_vars.sum(r, '*') >= l
                               for r, l in enumerate(self.loads_lb)))

        self.m.update()
        print('Time to add constraints %s' % (time.time() - start))

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
            # solution = np.zeros((self.n_rev, self.n_pap))
            # for v in self.m.getVars():
            #     i, j = self.indices_of_var(v)
            #     solution[i, j] = v.x
            if self.solution is None:
                self.solution = np.zeros((self.n_rev, self.n_pap))
            for key, var in self.lp_vars.items():
                self.solution[key[0], key[1]] = var.x
            return self.solution
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

    x = BasicMatcher(a, b, ws, init_makespan)
    s = time.time()
    x.solve()
    print(time.time() - s)
    print("[done.]")
