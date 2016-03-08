import logging
import numpy as np
import time
import uuid

from gurobipy import *

class IRMakespanMatcher(object):
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

    def __init__(self, alpha, beta, weights, makespan=0):
        self.n_rev = np.size(weights, axis=0)
        self.n_pap = np.size(weights, axis=1)
        self.alpha = alpha
        self.beta = beta
        self.weights = weights
        self.id = uuid.uuid4()
        self.m = Model(str(self.id) + ": Relaxed Makespan")
        self.makespan = makespan        # the minimum allowable sum of affinity for any paper
        self.solution = None

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

    def indices_of_var(self, v):
        name = v.varName
        indices = name[2:].split(',')
        i, j = int(indices[0]), int(indices[1])
        return i,j

    def sol_as_mat(self):
        if self.m.status == GRB.OPTIMAL or self.m.status == GRB.SUBOPTIMAL:
            solution = np.zeros((self.n_rev, self.n_pap))
            for v in self.m.getVars():
                i,j = self.indices_of_var(v)
                solution[i,j] = v.x
            self.solution = solution
            return solution
        else:
            raise Exception('You must have solved the model optimally or suboptimally before calling this function.')

    # solve optimization with whatever the current makespan is
    def solve_with_current_makespan(self, log_file=None):
        self.round_fractional(np.ones((self.n_rev, self.n_pap)) * -1, log_file)
        if self.m.status == GRB.OPTIMAL or self.m.status == GRB.SUBOPTIMAL:
            self.solution = self.sol_as_mat()
        return self.solution

    def add_round_const(self, i, j, val, log_file=None):
        if log_file:
            logging.info("\tROUNDING (REVIEWER, PAPER) " + str((i,j)) + " TO VAL: " + str(val))
        self.lp_vars[i][j].ub = val
        self.lp_vars[i][j].lb = val

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

        if log_file:
            logging.info("[OBJ]: %f" % self.objective_val())

    def round_fractional(self, integral_assignments=None, log_file=None, count = 0):
        if integral_assignments is None:
            integral_assignments = np.ones((self.n_rev, self.n_pap)) * -1

        self.m.optimize()

        if self.m.status != GRB.OPTIMAL and self.m.status != GRB.SUBOPTIMAL:
            return

        if self.integral_sol_found():
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

    def objective_val(self):
        return self.m.ObjVal

if __name__ == "__main__":
    alpha = 3
    beta = 3
    weights = np.genfromtxt('../../data/train/200-200-2.0-5.0-skill_based/weights.txt')
    init_makespan = 1.5  # took this from the training mx threshold in data/train dir

    x = IRMakespanMatcher(alpha, beta, weights, init_makespan)
    s = time.time()
    x.solve_with_current_makespan()
    print (time.time() - s)
    print "[done.]"
