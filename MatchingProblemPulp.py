import uuid
import numpy as np
from pulp import LpVariable, LpProblem, LpMaximize, LpStatus, value

class MatchingProblem(object):
    """A paper reviewing problem

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
        self.prob = LpProblem(str(self.id) + ": b-Matching", LpMaximize)
        self.prev_sols = []
        self.prev_affs = []

        # primal variables
        self.lp_vars = []
        for i in range(self.n_rev):
            self.lp_vars.append([])
            for j in range(self.n_pap):
                self.lp_vars[i].append(LpVariable(self.var_name(i,j), 0, 1))

        self.prob += sum([ self.weights[i][j] * self.lp_vars[i][j] for i in range(self.n_rev) for j in range(self.n_pap) ]), "total compatibility"

        # reviewer constraints
        for r in range(self.n_rev):
            self.prob += sum(self.lp_vars[r]) <= alpha, "reviewer " + str(r) + " cannot review more than " + str(self.alpha) + " papers"

        # paper constraints
        for p in range(self.n_pap):
            self.prob += sum([ self.lp_vars[i][p] for i in range(self.n_rev) ]) == self.beta, "paper " + str(p) + " must be reviewed at least " + str(self.beta) + " times"

    def var_name(self,i,j):
        return "x_" + str(i) + "," + str(j)

    def sol_dict(self):
        _sol = {}
        for v in self.prob.variables():
            _sol[v.name] = v.varValue
        return _sol

    def add_hard_const(self, i, j):
        solution = self.sol_dict()
        prevVal = solution[self.var_name(i,j)]

        self.prob += self.lp_vars[i][j] == abs(prevVal - 1), "Hard reviewing cosntraint (" + str(i) + ", " + str(j) + ")"

    def num_diffs(self, sol1, sol2):
        count = 0
        for (variable, val) in sol1.iteritems():
            if sol2[variable] != val:
                count += 1
        return count

    def solve(self):
        self.prob.solve()
        sol = {}
        for v in self.prob.variables():
            sol[v.name] = v.varValue
        self.prev_sols.append(sol)
        self.save_reviewer_affinity()

    def status(self):
        return LpStatus[self.prob.status]

    def save_reviewer_affinity(self):
        per_rev_aff = np.zeros((self.n_rev, 1))
        sol = self.sol_dict()
        for i in range(self.n_rev):
            for j in range(self.n_pap):
                per_rev_aff[i] += sol[self.var_name(i,j)] * self.weights[i][j]
        self.prev_affs.append(per_rev_aff)

    def objective_val(self):
        return value(self.prob.objective)
