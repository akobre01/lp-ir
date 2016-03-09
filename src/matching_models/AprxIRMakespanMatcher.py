import logging
import numpy as np
import time
import uuid

from gurobipy import *

import weights as wgts

class CompleteRelaxationMSMatcher(object):
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
        self.m = Model(str(self.id) + ": Complete Relaxation Makespan")
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
            self.m.addConstr(sum([ self.lp_vars[i][p] * self.weights[i][p] for i in range(self.n_rev) ]) >= self.makespan, self.makespan_constr_name(p))

        self.m.update()

    def makespan_constr_name(self, p):
        return self.ms_constr_prefix + str(p)

    def change_makespan(self, new_makespan, log_file=None):
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
            logging.info("[MAKESPAN ATTEMPT]: %f" % self.makespan)
        else:
            print "[MAKESPAN ATTEMPT]: %f" % self.makespan

        self.m.optimize()

        if self.m.status == GRB.OPTIMAL:
            if log_file:
                logging.info("[STATUS]: %d" % self.m.status)
                logging.info("SEARCHING BETWEEN: " + str(target) + " AND " + str(mx))
            else:
                print "\tSTATUS " + str(self.m.status) + "; SEARCHING BETWEEN: " + str(target) + " AND " + str(mx)
            return self.find_makespan_bin(target, mx, itr -1, log_file)
        else:
            if log_file:
                logging.info("[STATUS]: %d" % self.m.status)
                logging.info("SEARCHING BETWEEN: " + str(mn) + " AND " + str(target))
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

        if mx <= 0:
            mx = self.alpha * np.max(self.weights)

        self.find_makespan_bin(mn, mx, itr, log_file)

        begin_opt = time.time()
        self.round_fractional(np.ones((self.n_rev, self.n_pap)) * -1, log_file)
        end_opt = time.time()
        if log_file:
            logging.info("[SOLVER TIME]: %s" % (str(end_opt - begin_opt)))


        sol = {}
        for v in self.m.getVars():
            sol[v.varName] = v.x

        self.prev_sols.append(sol)
        self.save_reviewer_affinity()
        self.save_paper_affinity()
        if log_file:
            logging.info("[OBJ]: %f" % self.objective_val())

    def round_fractional(self, integral_assignments, log_file=None, count = 0):
        self.m.optimize()

        if self.integral_sol_found():
            print "FOUND INTEGRAL SOLUTION"
            if log_file:
                logging.info('[#ITERATIONS]: %d' % count)
            return
        else:
            if log_file:
                logging.info('[BEGIN ROUNDING ITERATION]: %d' % count)
            fractional_assignments = {}
            r_fractional = {}
            fractional_vars = {}
            sol = self.sol_dict()
            fractional_vars = []

            # If you find that any integral assignments, add constraints to keep them
            for i in range(self.n_rev):
                for j in range(self.n_pap):

                    if j not in fractional_assignments:
                        fractional_assignments[j] = []
                    if i not in r_fractional:
                        r_fractional[i] = []

                    if sol[self.var_name(i,j)] == 0.0 and integral_assignments[i][j] != 0.0:
                        self.add_round_const(i, j, 0.0, log_file)
                        integral_assignments[i][j] = 0.0

                    elif sol[self.var_name(i,j)] == 1.0 and integral_assignments[i][j] != 1.0:
                        self.add_round_const(i, j, 1.0, log_file)
                        integral_assignments[i][j] = 1.0

                    elif sol[self.var_name(i,j)] != 1.0 and sol[self.var_name(i,j)] != 0.0:
                        fractional_assignments[j].append((i,j, sol[self.var_name(i,j)]))
                        fractional_vars.append((i,j,sol[self.var_name(i,j)]))

                        r_fractional[i].append((i,j,sol[self.var_name(i,j)]))
                        integral_assignments[i][j] = sol[self.var_name(i,j)]

            # Let's log some features for learning which variables to round
            if log_file:
                logging.info('[FEAT_#PAPS_0_FRAC]: %d' % len(filter(lambda x: len(x) == 0, fractional_assignments.values())))
                logging.info('[FEAT_#PAPS_1_FRAC]: %d' % len(filter(lambda x: len(x) == 1, fractional_assignments.values())))
                logging.info('[FEAT_#PAPS_2_FRAC]: %d' % len(filter(lambda x: len(x) == 2, fractional_assignments.values())))
                logging.info('[FEAT_#PAPS_3_FRAC]: %d' % len(filter(lambda x: len(x) == 3, fractional_assignments.values())))
                logging.info('[FEAT_#PAPS_4+_FRAC]: %d' % len(filter(lambda x: len(x) >= 4, fractional_assignments.values())))

                logging.info('[FEAT_#REVS_0_FRAC]: %d' % len(filter(lambda x: len(x) == 0, r_fractional.values())))
                logging.info('[FEAT_#REVS_1_FRAC]: %d' % len(filter(lambda x: len(x) == 1, r_fractional.values())))
                logging.info('[FEAT_#REVS_2_FRAC]: %d' % len(filter(lambda x: len(x) == 2, r_fractional.values())))
                logging.info('[FEAT_#REVS_3_FRAC]: %d' % len(filter(lambda x: len(x) == 3, r_fractional.values())))
                logging.info('[FEAT_#REVS_4+_FRAC]: %d' % len(filter(lambda x: len(x) >= 4, r_fractional.values())))

                logging.info('[FEAT_#TIGHT_REV_CONSTR]: %d' % self.count_tight_rev_constr(sol))
                logging.info('[FEAT_#REV_0_ASSN]: %d' % self.count_revs_with_zero_assigned(sol))
                logging.info('[FEAT_#FRAC_VAR]: %d' % sum([ len(frac_vars) for frac_vars in fractional_assignments.values()]))


            # Drop makespan constraints on all of the papers that have two fractional assignments
            for (paper, frac_vars) in fractional_assignments.iteritems():
                if len(frac_vars) == 2:
                    for c in self.m.getConstrs():
                        if c.ConstrName == self.makespan_constr_name(paper):
                            if log_file:
                                logging.info('[REMOVED CONSTR NAME]: %s' % str(c.ConstrName))
                                logging.info('[REMOVED CONSTR PAPER]: %d' % paper)
                                logging.info('[REMOVED ON ITERATION]: %d' % count)
                            self.m.remove(c)

            return self.round_fractional(integral_assignments, log_file, count+1)


    def count_tight_rev_constr(self, sol):
        tight = 0
        for i in range(self.n_rev):
            assignment_count = 0
            for j in range(self.n_pap):
                assignment_count += sol[self.var_name(i,j)]
            if assignment_count == self.alpha:
                tight += 1
        return tight

    def count_revs_with_zero_assigned(self, sol):
        zero = 0
        for i in range(self.n_rev):
            assignment_count = 0
            for j in range(self.n_pap):
                assignment_count += sol[self.var_name(i,j)]
            if assignment_count == 0:
                zero += 1
        return zero

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