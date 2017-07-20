import logging
import numpy as np
import time
import uuid

from gurobipy import *


class MakespanMatcher(object):
    """A Makespan paper matcher.

    A paper matcher that tries to maximize the minimum among all paper
    assignment scores (a paper assignment score is the sum of affinities for
    all reviewers assigned to that paper). "Makespan" refers to the constraint
    on a paper that constraints its assignment score to be greater than T. The
    makespan formulation of paper matching is NP-Hard; we rely on the solver
    (Gurobi) to do its best to solve the problem for us. In other matching
    models, we will guarantee approximate solutions. Gurobi uses branch and
    bound to solve the ILP (I think???).
    """

    # TODO(AK): We should add reviewer lower bounds to this.
    def __init__(self, alphas, betas, weights, makespan=0):
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
        self.alphas = alphas
        self.betas = betas
        self.weights = weights
        self.id = uuid.uuid4()
        self.m = Model("%s: makespan matcher" % str(self.id))
        self.makespan = makespan     # the minimum allowable paper score.
        # TODO(AK): can we make a makespan constraint per paper?
        self.solution = None

        self.m.setParam('OutputFlag', 0)
        self.m.setParam('MIPGap', 0.02)
        self.m.setParam('IterationLimit', 200000)

        self.ms_constr_prefix = "ms"

        # primal variables
        self.lp_vars = []
        for i in range(self.n_rev):
            self.lp_vars.append([])
            for j in range(self.n_pap):
                self.lp_vars[i].append(self.m.addVar(vtype=GRB.BINARY,
                                                     name=self.var_name(i, j)))
        self.m.update()

        # Set the objective.
        obj = LinExpr()
        for i in range(self.n_rev):
            for j in range(self.n_pap):
                obj += self.weights[i][j] * self.lp_vars[i][j]
        self.m.setObjective(obj, GRB.MAXIMIZE)

        # Reviewer constraints.
        for r, alpha in enumerate(self.alphas):
            self.m.addConstr(sum(self.lp_vars[r]) <= alpha, "r" + str(r))

        # Paper constraints.
        for p, beta in enumerate(self.betas):
            self.m.addConstr(sum([self.lp_vars[i][p]
                                  for i in range(self.n_rev)]) == beta,
                             "p" + str(p))

        # Makespan constraints.
        for p in range(self.n_pap):
            self.m.addConstr(sum([self.lp_vars[i][p] * self.weights[i][p]
                                  for i in range(self.n_rev)]) >= self.makespan,
                             self.ms_constr_prefix  + str(p))
        self.m.update()

    def change_makespan(self, new_makespan):
        """Change the current makespan to a new_makespan value.

        Args:
            new_makespan - the new makespan constraint.

        Returns:
            Nothing.
        """
        for c in self.m.getConstrs():
            if c.getAttr("ConstrName").startswith(self.ms_constr_prefix):
                self.m.remove(c)
                self.m.update()

        for p in range(self.n_pap):
            self.m.addConstr(sum([self.lp_vars[i][p] * self.weights[i][p]
                                  for i in range(self.n_rev) ]) >= new_makespan,
                             self.ms_constr_prefix + str(p))
        self.makespan = new_makespan
        self.m.update()

    def find_makespan_bin(self, mn=0, mx=-1, itr=10, log_file=None):
        """Use a binary search to find a feasible makespan.

        Try to solve the ILP with the current setting of the makespan. If that
        doesn't work, then decrease the makespan halfway to the maximum feasible
        makespan so far (as in a normal binary search). Repeat for 10
        iterations and return the this object (which stores the best makespan).

        Args:
            mn - the minimum feasible makespan so far (optional).
            mx - the maximum feasible makespan so far (optional).
            itr - the maximum number of iterations before we give up (optional).
            log_file - a string path to the log file (optional).
        """
        if mx == -1:
            mx = self.alpha
        if itr <= 0 or mn >= mx:
            self.m.optimize()
            return self

        prv = self.makespan
        target = (mn + mx) / 2.0
        self.change_makespan(target)

        if log_file:
            logging.info(
                "\tATTEMPTING TO SOLVE WITH MAKESPAN: %f" % self.makespan)

        self.m.optimize()

        if self.m.status == GRB.OPTIMAL or self.m.status == GRB.SUBOPTIMAL:
            if log_file:
                logging.info("\tSTATUS %s; SEARCHING BETWEEN: %s AND %s" % (
                    str(self.m.status), str(target), str(mx)))
            return self.find_makespan_bin(target, mx, itr -1, log_file)
        else:
            if log_file:
                logging.info("\tSTATUS %s; SEARCHING BETWEEN: %s AND %s" % (
                    str(self.m.status), str(mn), str(target)))
            self.change_makespan(prv)
            return self.find_makespan_bin(mn, target, itr - 1, log_file)

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

    def solve_with_current_makespan(self):
        """Solve the ILP with the current makespan.

        If we were not able to solve the ILP optimally or suboptimally, then
        raise an error.  If we are able to solve the ILP, save the solution.

        Args:
            None.

        Returns:
            An np array corresponding to the solution.
        """
        self.m.optimize()
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
        if mx <= 0:
            mx = np.max(self.alphas) * np.max(self.weights)

        self.find_makespan_bin(mn, mx, itr, log_file)

        begin_opt = time.time()
        self.m.optimize()
        end_opt = time.time()
        if log_file:
            logging.info("[SOLVER TIME]: %s" % (str(end_opt - begin_opt)))
        return self.sol_as_mat()

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

    x = MakespanMatcher(a, b, ws, init_makespan)
    s = time.time()
    x.solve_with_current_makespan()
    print(time.time() - s)
    print("[done.]")
