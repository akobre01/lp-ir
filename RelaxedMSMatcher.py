import logging
import numpy as np
import uuid

from gurobipy import *

import weights as wgts

class RelaxedMSMatcher(object):
    """An iterative paper matching problem instance that tries to satisfy
    a makespan constraint at each paper using an approximation algorithm based
    on rounding the solution to the relaxed LP solution.

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
        self.m = Model(str(self.id) + ": Relaxed Makespan")
        self.prev_sols = []
        self.prev_rev_affs = []
        self.prev_pap_affs = []
        self.makespan = makespan                    # the minimum allowable sum of affinity for any paper

        self.m.setParam('OutputFlag', 0)
        self.m.setParam('MIPGap', 0.02)
        self.m.setParam('IterationLimit', 200000)

        self.ms_constr_prefix = "ms"
        self.user_ms_constr_prefix = "ums"
        self.round_constr_prefix = "round"

        # primal variables
        self.lp_vars = []
        for i in range(self.n_rev):
            self.lp_vars.append([])
            for j in range(self.n_pap):
                self.lp_vars[i].append(self.m.addVar(ub=1.0, name=self.var_name(i,j)))

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

    def makespan_constr_name(self, p):
        return self.ms_constr_prefix + str(p)

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
            self.m.reset()
            self.m.optimize()
            return self

        prv = self.makespan
        target = (mn + mx) / 2.0
        self.change_makespan(target)

        if log_file:
            logging.info("\tATTEMPTING TO SOLVE WITH MAKESPAN: " + str(self.makespan))
        else:
            print "\tATTEMPTING TO SOLVE WITH MAKESPAN: " + str(self.makespan)

        self.m.optimize()

        if self.m.status == GRB.OPTIMAL:
            if log_file:
                logging.info("\tSTATUS " + str(self.m.status) + "; SEARCHING BETWEEN: " + str(target) + " AND " + str(mx))
            else:
                print "\tSTATUS " + str(self.m.status) + "; SEARCHING BETWEEN: " + str(target) + " AND " + str(mx)
            return self.find_makespan_bin(target, mx, itr -1, log_file)
        else:
            if log_file:
                logging.info("\tSTATUS " + str(self.m.status) + "; SEARCHING BETWEEN: " + str(mn) + " AND " + str(target))
            else:
                print "\tSTATUS " + str(self.m.status) + "; SEARCHING BETWEEN: " + str(mn) + " AND " + str(target)
            self.change_makespan(prv)
            return self.find_makespan_bin(mn, target, itr - 1, log_file)

    def integral_sol_found(self):
        sol = self.sol_dict()
        return all(sol[self.var_name(i,j)] == 1.0 or sol[self.var_name(i,j)] == 0.0 for i in range(self.n_rev) for j in range(self.n_pap))

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

    def add_round_const(self, i, j, val, log_file=None):
        if log_file:
            logging.info("\tROUNDING (REVIEWER, PAPER) " + str((i,j)) + " TO VAL: " + str(val))
        self.lp_vars[i][j].ub = val
        self.lp_vars[i][j].lb = val
        #self.m.addConstr(self.lp_vars[i][j] == val, self.round_constr_prefix + str(i) + ", " + str(j))

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

    # find an appropriate makespan using binary search and solve
    def solve(self, mn=0, mx=-1, itr=10, log_file=None):
        for c in self.m.getConstrs():
            if c.ConstrName.startswith(self.round_constr_prefix):
                self.m.remove(c)
#                self.m.update()

        if mx <= 0:
            mx = self.alpha * np.max(self.weights)

        self.find_makespan_bin(mn, mx, itr, log_file)
        self.round_fractional(np.ones((self.n_rev, self.n_pap)) * -1, log_file)

        sol = {}
#        for v in self.m.getVars():
#            print v.varName
#            sol[v.varName] = v.x

        self.prev_sols.append(sol)
        self.save_reviewer_affinity()
        self.save_paper_affinity()
        if log_file:
            logging.info("OBJECTIVE VALUE: " + str(self.objective_val()))

    def round_fractional(self, integral_assignments, log_file=None):
        self.m.reset()
        self.m.optimize()
        print self.m.status
#        for c in self.m.getConstrs():
#            print c.ConstrName
        if self.integral_sol_found():
            for c in self.m.getConstrs():
                if c.ConstrName.startswith(self.ms_constr_prefix):
                    print c, c.ConstrName, c.RHS
            return
        else:
            fractional_assignments = {}
            fractional_vars = {}
            sol = self.sol_dict()
            fractional_vars = []

            # If you find that any integral assignments, add constraints to keep them
            for i in range(self.n_rev):
                for j in range(self.n_pap):

                    if j not in fractional_assignments:
                        fractional_assignments[j] = []

                    if sol[self.var_name(i,j)] == 0.0 and integral_assignments[i][j] != 0.0:
                        self.add_round_const(i, j, 0.0, log_file)
                        integral_assignments[i][j] = 0.0

                    elif sol[self.var_name(i,j)] == 1.0 and integral_assignments[i][j] != 1.0:
                        self.add_round_const(i, j, 1.0, log_file)
                        integral_assignments[i][j] = 1.0

                    elif sol[self.var_name(i,j)] != 1.0 and sol[self.var_name(i,j)] != 0.0:
                        fractional_assignments[j].append((i,j, sol[self.var_name(i,j)]))
                        fractional_vars.append((i,j,sol[self.var_name(i,j)]))
                        integral_assignments[i][j] = sol[self.var_name(i,j)]

#            self.m.update()

#            print integral_assignments

            # if you find any paper with 1 fractional assignment, round to zero, drop a makespan constraint and resolve
            constrs_to_remove = {}
            for (paper, frac_vars) in fractional_assignments.iteritems():
                if len(frac_vars) == 1:
                    i,j,v = frac_vars[0]
#                    print integral_assignments
                    integral_assignments[i][j] = 0.0
                    self.add_round_constr(i, j, 0.0, log_file)
#                    self.m.update()

                    for c in self.m.getConstrs():
                        if c.ConstrName == self.makespan_constr_name(j):
#                            print c, c.ConstrName, i, j, c.RHS, self.weights[i][j], c.RHS - self.weights[i][j]
#                            print integral_assignments
#                            print
                            self.m.remove(c)
#                            new_RHS = max(c.RHS - self.weights[i][j], 0.0)
#                            self.m.addConstr(sum([ self.lp_vars[i][j] * self.weights[i][j] for i in range(self.n_rev) ]) >= new_RHS,
#                                             c.ConstrName)
#                            self.m.update()
                            print "RECURSING"
                            return self.round_fractional(integral_assignments, log_file)

            for (paper, frac_vars) in fractional_assignments.iteritems():
                if len(frac_vars) == 2:
#                    i1,j,v1 = frac_vars[0]
#                    i2,_,v2 = frac_vars[0]
#                    print integral_assignments
#                    integral_assignments[i][j] = 0.0
#                    self.m.update()

                    for c in self.m.getConstrs():
                        if c.ConstrName == self.makespan_constr_name(j):
#                            print c, c.ConstrName, i, j, c.RHS, self.weights[i][j], c.RHS - self.weights[i][j]
#                            print integral_assignments
#                            print
                            self.m.remove(c)
#                            new_RHS = max(c.RHS - self.weights[i][j], 0.0)
#                            self.m.addConstr(sum([ self.lp_vars[i][j] * self.weights[i][j] for i in range(self.n_rev) ]) >= new_RHS,
#                                             c.ConstrName)
#                            self.m.update()
                            print "RECURSING"
                            return self.round_fractional(integral_assignments, log_file)

            for (paper, frac_vars) in fractional_assignments.iteritems():
                if len(frac_vars) == 3:
#                    i1,j,v1 = frac_vars[0]
#                    i2,_,v2 = frac_vars[1]
#                    i3,_,v3 = frac_vars[2]
#                    print integral_assignments
#                    integral_assignments[i][j] = 0.0
#                    self.add_round_constr(i,j,log_file)
#                    self.m.update()

                    for c in self.m.getConstrs():
                        if c.ConstrName == self.makespan_constr_name(j):
#                            print c, c.ConstrName, i, j, c.RHS, self.weights[i][j], c.RHS - self.weights[i][j]
#                            print integral_assignments
#                            print
                            self.m.remove(c)
#                            new_RHS = max(c.RHS - self.weights[i][j], 0.0)
#                            self.m.addConstr(sum([ self.lp_vars[i][j] * self.weights[i][j] for i in range(self.n_rev) ]) >= new_RHS,
#                                             c.ConstrName)
#                            self.m.update()
                            print "RECURSING"
                            return self.round_fractional(integral_assignments, log_file)

            # if there are two reviewers assigned fractionally to each paper, construct a perfect matching
            # if all(len(x) == 2 for (y,x) in fractional_assignments.iteritems()):
            #    print "WARNING: SOLVING A PERFECT MATCHING UNIMPLEMENTED"

            # print "INFO: finished rounding"

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
        self.prev_rev_affs.append(per_rev_aff)

    def save_paper_affinity(self):
        per_pap_aff = np.zeros((self.n_pap, 1))
        sol = self.sol_dict()
        for i in range(self.n_pap):
            for j in range(self.n_rev):
                per_pap_aff[i] += sol[self.var_name(j,i)] * self.weights[j][i]
        self.prev_pap_affs.append(per_pap_aff)


    def objective_val(self):
        return self.m.ObjVal

if __name__ == "__main__":
    n_rev = 10
    n_pap = 10
    alpha = 1
    beta = 1
    bp1 = 0.5
    bp2 = 5.0
    weights = wgts.skillBased(n_rev, n_pap, bp1, bp2)
    init_makespan = 0

    np.set_printoptions(precision=3)
    print "running"
    x = RelaxedMSMatcher(n_rev, n_pap, alpha, beta, weights, init_makespan)
    x.solve()

    print "[done.]"
