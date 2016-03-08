import logging
import numpy as np
import uuid

from gurobipy import *

class DistortionMatcher(object):
    """A paper matcher that consists of two stages; the first stage tries to
    maximize paper-reviewer affinity (optionally subject to makespan constraints);
    the second stage changes the objective to value keeping variables the same
    between successive iterations (while still statisfying all or most of the
    constraints)

    Attributes:
      n_Rev - the number of reviewers
      n_Pap - the number of papers
      alpha - the maximum number of papers any reviewer can be assigned
      beta - the number of reviews required per paper
      weights - the compatibility between each reviewer and each paper.
                This should be a numpy matrix of dimension  n_rev x n_pap.
    """

    def __init__(self, n_rev, n_pap, alpha, beta, weights, makespan=0):
        self.n_rev = n_rev
        self.n_pap = n_pap
        self.alpha = alpha
        self.beta = beta
        self.weights = weights
        self.id = uuid.uuid4()
        self.m = Model(str(self.id) + ": iterative b-matching")
        self.prev_sols = []
        self.prev_affs = []
        self.makespan = makespan                    # the minimum allowable sum of affinity for any paper
        self.init_sol = False

        self.m.setParam('OutputFlag', 0)
        self.m.setParam('MIPGap', 0.02)
        self.m.setParam('IterationLimit', 200000)

        self.ms_constr_prefix = "ms"
        self.user_ms_constr_prefix = "ums"

        # primal variables
        self.lp_vars = []
        for i in range(self.n_rev):
            self.lp_vars.append([])
            for j in range(self.n_pap):
                self.lp_vars[i].append(self.m.addVar(vtype=GRB.BINARY, name=self.var_name(i,j)))
        self.m.update()

        # set the objective
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

        # (paper) makespan constraints
        for p in range(self.n_pap):
            self.m.addConstr(sum([ self.lp_vars[i][p] * self.weights[i][p] for i in range(self.n_rev) ]) >= self.makespan, self.ms_constr_prefix  + str(p))

        self.m.update()

    def reset_distortion_obj(self):
        prev_solution = self.prev_sols[-1]
        obj = LinExpr()
        for i in range(self.n_rev):
            for j in range(self.n_pap):
                if prev_solution[self.var_name(i,j)] == 1:
                    obj += 1 - self.lp_vars[i][j]          # if the variable was set to 1 previously, try to keep it a 1
                else:
                    obj += self.lp_vars[i][j]              # if the variable was a 0 try to keep it a 0
        self.m.setObjective(obj, GRB.MINIMIZE)             # the new problem is a minimization problem
        self.m.update()

    def change_makespan(self, new_makespan):
        for c in self.m.getConstrs():
            if c.getAttr("ConstrName").startswith(self.ms_constr_prefix):
                self.m.remove(c)
                self.m.update()

        for p in range(self.n_pap):
            self.m.addConstr(sum([ self.lp_vars[i][p] * self.weights[i][p] for i in range(self.n_rev) ]) >= new_makespan, self.ms_constr_prefix + str(p))
        self.makespan = new_makespan
        self.m.update()

    def find_makespan_bin(self, mn=0, mx=-1, itr=10, log_file=None):
        if mx == -1:
            mx = self.alpha
        if itr <= 0 or mn >= mx:
            self.m.optimize()
            return self

        prv = self.makespan
        target = (mn + mx) / 2.0
        self.change_makespan(target)
        if log_file:
            logging.info("\tATTEMPTING TO SOLVE WITH MAKESPAN: " + str(self.makespan))
        self.m.optimize()

        if self.m.status == GRB.OPTIMAL or self.m.status == GRB.SUBOPTIMAL:
            if log_file:
                logging.info("\tSTATUS " + str(self.m.status) + "; SEARCHING BETWEEN: " + str(target) + " AND " + str(mx))
            return self.find_makespan_bin(target, mx, itr -1)
        else:
            if log_file:
                logging.info("\tSTATUS " + str(self.m.status) + "; SEARCHING BETWEEN: " + str(mn) + " AND " + str(target))
            self.change_makespan(prv)
            return self.find_makespan_bin(mn, target, itr - 1)

    def var_name(self,i,j):
        return "x_" + str(i) + "," + str(j)

    def sol_dict(self):
        _sol = {}
        for v in self.m.getVars():
            _sol[v.varName] = v.x
        return _sol

    def add_hard_const(self, i, j, log_file=None):
        solution = self.sol_dict()
        prevVal = solution[self.var_name(i,j)]
        if log_file:
            logging.info("\t(REVIEWER, PAPER) " + str((i,j)) + " CHANGED FROM: " + str(prevVal) + " -> " + str(abs(prevVal - 1)))
        self.m.addConstr(self.lp_vars[i][j] == abs(prevVal - 1), "h" + str(i) + ", " + str(j))

    def add_adeq_const(self, paper):
        solution = self.sol_dict()
        prevVal = solution[self.var_name(i,j)]
        prev_score = sum([ x.m.getVarByName(x.var_name(i,paper)).x * x.weights[i][paper] for i in range(x.n_rev) ])
        max_increase = float(self.beta) - prev_score
        self.m.addConstr(sum([ self.lp_vars[i][paper] * self.weights[i][paper] for i in range(self.n_rev) ]) >=
                         min(float(beta), prev_score + max_increase / 10.0), self.user_ms_constr_prefix + str(p))

    def num_diffs(self, sol1, sol2):
        count = 0
        for (variable, val) in sol1.iteritems():
            if sol2[variable] != val:
                count += 1
        return count

    # if you've already solved the problem and have an initial solution,
    # change to a minimization problem (minimize distortion)
    def solve(self, mn=0, mx=-1, itr=10, log_file=None):
        if self.init_sol == False:
            self.init_sol = True

        else:
            self.reset_distortion_obj()
            logging.info("OBJECTION RESET: minimize distortion")

        if mx <= 0:
            mx = self.alpha * np.max(self.weights)

        self.find_makespan_bin(mn, mx, itr, log_file)
        self.m.optimize()

        sol = {}
        for v in self.m.getVars():
            sol[v.varName] = v.x
        self.prev_sols.append(sol)
        self.save_reviewer_affinity()

    def status(self):
        return self.m.status

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

if __name__ == "__main__":
    n_rev = 100
    n_pap = 250
    alpha = 8
    beta = 3
    weights = np.random.rand(n_rev, n_pap)
    init_makespan = 0

    x = DistortionMatcher(n_rev, n_pap, alpha, beta, weights, init_makespan)
    x.find_makespan_bin(0, alpha, 10)
    print x.makespan
    x.solve()
    print x.objective_val()
    print x.status()
    print "CHAINGING PHASE"
    x.reset_distortion_obj()
    x.solve()
    print x.objective_val()

    for p in range(x.n_pap):
        assert sum([ x.m.getVarByName(x.var_name(i,p)).x * x.weights[i][p] for i in range(x.n_rev) ]) >= x.makespan
