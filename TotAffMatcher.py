import uuid
import numpy as np
from gurobipy import *

class TotAffMatcher(object):
    """An iterative paper matching problem instance that tries to maximize
    the sum total affinity of all reviewer paper matches

    Attributes:
      n_Rev - the number of reviewers
      n_Pap - the number of papers
      alpha - the maximum number of papers any reviewer can be assigned
      beta - the (minimum) number of reviewers any paper can be assigned
      weights - the compatibility between each reviewer and each paper.
                This should be a numpy matrix of dimension  n_rev x n_pap.
    """

    def __init__(self, n_rev, n_pap, alpha, beta, weights):
        self.n_rev = n_rev
        self.n_pap = n_pap
        self.alpha = alpha
        self.beta = beta
        self.weights = weights
        self.id = uuid.uuid4()
        self.m = Model(str(self.id) + ": iterative b-matching")
        self.prev_sols = []
        self.prev_affs = []
        self.m.setParam('OutputFlag',0)

        # primal variables
        self.lp_vars = []
        for i in range(self.n_rev):
            self.lp_vars.append([])
            for j in range(self.n_pap):
                self.lp_vars[i].append(self.m.addVar(vtype=GRB.BINARY, name=self.var_name(i,j)))

        self.m.update()

        # set the objective (this could be sped up if need be by incorporating it into the previous loop)
        obj = LinExpr()
        for i in range(self.n_rev):
            for j in range(self.n_pap):
                obj += self.weights[i][j] * self.lp_vars[i][j]
        self.m.setObjective(obj, GRB.MAXIMIZE)

        # reviewer constraints
        for r in range(self.n_rev):
            self.m.addConstr(sum(self.lp_vars[r]) <= alpha, "r" + str(r))

        # paper constraints
        for p in range(self.n_pap):
            self.m.addConstr(sum([ self.lp_vars[i][p] for i in range(self.n_rev) ]) == self.beta, "p" + str(p))

    def var_name(self,i,j):
        return "x_" + str(i) + "," + str(j)

    def sol_dict(self):
        _sol = {}
        for v in self.m.getVars():
            _sol[v.varName] = v.x
        return _sol

    def add_hard_const(self, i, j):
        solution = self.sol_dict()
        prevVal = solution[self.var_name(i,j)]

        self.m.addConstr(self.lp_vars[i][j] == abs(prevVal - 1), "h" + str(i) + ", " + str(j))

    def num_diffs(self, sol1, sol2):
        count = 0
        for (variable, val) in sol1.iteritems():
            if sol2[variable] != val:
                count += 1
        return count

    def solve(self):
        self.m.optimize()
        sol = {}
        for v in self.m.getVars():
            sol[v.varName] = v.x
        self.prev_sols.append(sol)
        self.save_reviewer_affinity()

    def status(self):
        return m.status

    def turn_on_verbosity(self):
        self.m.setParam('OutputFlag', 1)

    def save_reviewer_affinity(self):
        per_rev_aff = np.zeros((self.n_rev, 1))
        sol = self.sol_dict()
        for i in range(self.n_rev):
            for j in range(self.n_pap):
                per_rev_aff[i] += sol[self.var_name(i,j)] * self.weights[i][j]
        self.prev_affs.append(per_rev_aff)

    def objective_val(self):
        return self.m.ObjVal
