import logging
import numpy as np
import time
import uuid

from .MakespanMatcher import MakespanMatcher
from gurobipy import *


class IRMakespanMatcher(MakespanMatcher):
    """A Makespan paper matcher with iterative relaxation.

        A paper matcher that tries to maximize the minimum among all paper
        assignment scores (a paper assignment score is the sum of affinities for
        all reviewers assigned to that paper). "Makespan" refers to the
        constraint on a paper that constrains its assignment score to be greater
        than T. The makespan formulation of paper matching is NP-Hard; here we
        use iterative relaxation to solve the problem. Specifically, we relax
        the integrality constraints and perform specific rounding that
        guarantees to return a solution in which the makespan constraint at each
        paper is violated by at most w_max which is the maximum affinity between
        any rewviewer and that paper.
        """

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
        self.m = Model("%s : IRMakespan" % str(self.id))
        self.makespan = makespan
        self.solution = None

        self.m.setParam('OutputFlag', 0)

        self.ms_constr_prefix = "ms"
        self.round_constr_prefix = "round"

        # primal variables
        self.lp_vars = []
        for i in range(self.n_rev):
            self.lp_vars.append([])
            for j in range(self.n_pap):
                self.lp_vars[i].append(self.m.addVar(ub=1.0,
                                                     name=self.var_name(i, j)))
        self.m.update()

        # set the objective
        obj = LinExpr()
        for i in range(self.n_rev):
            for j in range(self.n_pap):
                obj += self.weights[i][j] * self.lp_vars[i][j]
        self.m.setObjective(obj, GRB.MAXIMIZE)

        # Reviewer constraints.
        for r, load in enumerate(self.loads):
            self.m.addConstr(sum(self.lp_vars[r]) <= load, "r" + str(r))

        # Paper constraints.
        for p, cov in enumerate(self.coverages):
            self.m.addConstr(sum([self.lp_vars[i][p]
                                  for i in range(self.n_rev)]) == cov,
                             "p" + str(p))

        # Makespan constraints.
        for p in range(self.n_pap):
            self.m.addConstr(sum([self.lp_vars[i][p] * self.weights[i][p]
                                  for i in range(self.n_rev)]) >= self.makespan,
                             self.ms_constr_prefix + str(p))
        self.m.update()

    def makespan_constr_name(self, p):
        """Get the name of the makespan constraint for paper p."""
        return self.ms_constr_prefix + str(p)

    def integral_sol_found(self):
        """Return true if all lp variables are integral."""
        sol = self.sol_as_dict()
        return all(sol[self.var_name(i, j)] == 1.0 or
                   sol[self.var_name(i, j)] == 0.0
                   for i in range(self.n_rev) for j in range(self.n_pap))

    def add_round_const(self, i, j, val, log_file=None):
        """Round the variable x_ij to val."""
        if log_file:
            logging.info("\tROUNDING (REVIEWER, PAPER) %s TO VAL: %s" % (
                 str((i, j)), str(val)))
        self.lp_vars[i][j].ub = val
        self.lp_vars[i][j].lb = val

    # find an appropriate makespan using binary search and solve
    def solve(self, mn=0, mx=-1, itr=10, log_file=None):
        """Find a makespan and solve the ILP.

        Run a binary search to find an appropriate makespan and then solve the
        ILP. If solved optimally or suboptimally then save the solution.

        Args:
            mn - the minimum feasible makespan (optional).
            mx - the maximum possible makespan( optional).
            itr - the number of iterations of binary search for the makespan.
            log_file - the string path to the log file.

        Returns:
            The solution as a matrix.
        """
        # TODO(AK)): Does this even do anything?
        for c in self.m.getConstrs():
            if c.ConstrName.startswith(self.round_constr_prefix):
                print("SURPRISE! REMOVING A CONSTRAINT: %s" % str(c))
                self.m.remove(c)

        if mx <= 0:
            mx = np.max(self.loads) * np.max(self.weights)

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

    def round_fractional(self, integral_assignments=None, log_file=None,
                         count=0):
        """Round a fractional solution.

        This is the meat of the iterative relaxation approach.  First, if the
        solution to the relaxed LP is integral, then we're done--return the
        solution. Otherwise, here's what we do:
        1. if a variable is integral, lock it's value to that integer.
        2. find one paper with exactly 2 fractionally assigned reviewers and
           drop the makespan constraint on that reviewer.

        Args:
            integral_assignments - np.array of revs x paps (initially None).
            log_file - the log file if exists.
            count - (int) to keep track of the number of calls to this function.

        Returns:
            Nothing--has the side effect or storing an assignment matrix in this
            class.
        """
        if integral_assignments is None:
            integral_assignments = np.ones((self.n_rev, self.n_pap)) * -1

        self.m.optimize()

        if self.m.status != GRB.OPTIMAL and self.m.status != GRB.SUBOPTIMAL:
            assert False, self.m.status

        if self.integral_sol_found():
            if log_file:
                logging.info('[#ITERATIONS]: %d' % count)
            return
        else:
            if log_file:
                logging.info('[BEGIN ROUNDING ITERATION]: %d' % count)
            fractional_assignments = {}
            #r_fractional = {}
            sol = self.sol_as_dict()
            fractional_vars = []

            for i in range(self.n_rev):
                for j in range(self.n_pap):
                    if j not in fractional_assignments:
                        fractional_assignments[j] = []
                    #if i not in r_fractional:
                    #    r_fractional[i] = []

                    if sol[self.var_name(i, j)] == 0.0 and \
                                    integral_assignments[i][j] != 0.0:
                        self.add_round_const(i, j, 0.0, log_file)
                        integral_assignments[i][j] = 0.0

                    elif sol[self.var_name(i, j)] == 1.0 and \
                                    integral_assignments[i][j] != 1.0:
                        self.add_round_const(i, j, 1.0, log_file)
                        integral_assignments[i][j] = 1.0

                    elif sol[self.var_name(i, j)] != 1.0 and \
                                    sol[self.var_name(i, j)] != 0.0:
                        fractional_assignments[j].append(
                            (i, j, sol[self.var_name(i, j)]))
                        fractional_vars.append((i, j, sol[self.var_name(i, j)]))

                     #   r_fractional[i].append((i, j, sol[self.var_name(i, j)]))
                        integral_assignments[i][j] = sol[self.var_name(i, j)]

            for (paper, frac_vars) in fractional_assignments.items():
                if len(frac_vars) == 2:
                    for c in self.m.getConstrs():
                        if c.ConstrName == self.makespan_constr_name(paper):
                            if log_file:
                                logging.info('[REMOVED CONSTR NAME]: %s' %
                                             str(c.ConstrName))
                                logging.info(
                                    '[REMOVED CONSTR PAPER]: %d' % paper)
                                logging.info(
                                    '[REMOVED ON ITERATION]: %d' % count)
                            self.m.remove(c)
                            return self.round_fractional(integral_assignments,
                                                         log_file, count + 1)

    # THIS METHOD IS BROKEN NOW
    def count_tight_rev_constr(self, sol):
        """Return the number of tight reviewer load constraints."""
        tight = 0
        for i in range(self.n_rev):
            assignment_count = 0
            for j in range(self.n_pap):
                assignment_count += sol[self.var_name(i,j)]
            if assignment_count == self.alpha:
                tight += 1
        return tight

    def count_revs_with_zero_assigned(self, sol):
        """Return the number of reviewers without any assignments."""
        zero = 0
        for i in range(self.n_rev):
            assignment_count = 0
            for j in range(self.n_pap):
                assignment_count += sol[self.var_name(i,j)]
            if assignment_count == 0:
                zero += 1
        return zero

if __name__ == "__main__":
    ws = np.genfromtxt(
        'data/train/200-200-2.0-5.0-skill_based/weights.txt')
    a = [3] * np.size(ws, axis=0)
    b = [3] * np.size(ws, axis=1)

    init_makespan = 0.0

    x = IRMakespanMatcher(a, b, ws, init_makespan)
    s = time.time()
    x.round_fractional()

    print(time.time() - s)
    print("[done.]")
