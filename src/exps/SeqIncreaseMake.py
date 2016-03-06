import argparse
import numpy as np
import sys
import time

from gurobipy import *
sys.path.insert(0,'..')
from matching_models.MakespanMatcher import MakespanMatcher

class SeqIncreaseMake:
    def __init__(self, n_rev, n_pap, alpha, beta, weights, mkspns):
        self.n_rev = n_rev
        self.n_pap = n_pap
        self.alpha = alpha
        self.beta = beta
        self.weights = weights
        self.mkspns = mkspns
        self.curr_makespan = 0.0
        self.mkspn_and_sol = []

    def solve_with_curr_makespan(self):
        """
        THIS CODE DOES NOT USE WARM STARTING
        """
        problem = MakespanMatcher(self.n_rev, self.n_pap, self.alpha, self.beta, self.weights, self.curr_makespan)
        problem.solve_with_current_makespan()
        status = problem.status()
        if status == GRB.OPTIMAL:
            self.mkspn_and_sol.append((self.curr_makespan, problem.sol_as_mat()))
        else:
            self.mkspn_and_sol.append((self.curr_makespan, None))
        return (status, problem)

    def num_diffs(self, a1, a2):
        return float(np.sum(np.abs(a1 - a2)))   # this assumes that the

    def report_result(self, assignments, prev_assignments, init_assignment, t):
        if assignments is not None and prev_assignments is not None:
            overall_percent_change = 100.0 * self.num_diffs(assignments, prev_assignments) / np.size(assignments)
            percent_reviews_change = 100.0 * self.num_diffs(assignments, prev_assignments) / (self.n_pap * self.beta * 2.0)   # percet of total reviews that change
            percent_reviews_change_from_init = 100.0 * self.num_diffs(assignments, init_assignment) / (self.n_pap * self.beta * 2.0)   # percet of total reviews that changes
        else:
            overall_percent_change = "----"
            percent_reviews_change = "----"
            percent_reviews_change_from_init = "----"
        return "\t".join(map(lambda x: str(x), ["%.2f" % self.curr_makespan,
                                                self.n_pap,
                                                self.n_rev,
                                                self.alpha,
                                                self.beta,
                                                overall_percent_change,
                                                percent_reviews_change,
                                                percent_reviews_change_from_init,
                                                "%.2fs" % float(t)]))

    def run_exp(self):
        print "\t".join(["MKSPN","#PAP", "#REV", "ALPHA", "BETA", "%X", "%R", "%R0", "TIME"])
        self.curr_makespan = 0
        self.solve_with_curr_makespan()
        init_assignment = self.mkspn_and_sol[-1][1]
        prev_assignment = init_assignment
        for mkspn in self.mkspns:
            self.curr_makespan = mkspn
            s = time.time()
            self.solve_with_curr_makespan()
            t = time.time() - s
            assignment = self.mkspn_and_sol[-1][1]
            print(self.report_result(assignment, prev_assignment, init_assignment, t))
            prev_assignment = assignment


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for creating weight files.')
    parser.add_argument('rev_max', type=int, help='max # of papers per rev')
    parser.add_argument('pap_revs', type=int, help='# of reviewers per paper')
    parser.add_argument('weight_file', type=str, help='the file from which to read the weights')
    parser.add_argument('step', type=float, help='the step value by which we increase the makespan')


    args = parser.parse_args()

    def createDir(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError, e:
            if e.errno != 17:
                raise # This was not a "directory exist" error..

    rev_max = args.rev_max
    pap_revs = args.pap_revs
    weights = np.genfromtxt(args.weight_file)
    n_rev = np.size(weights, axis=0)
    n_pap = np.size(weights, axis=1)
    step = args.step

    sim = SeqIncreaseMake(n_rev, n_pap, rev_max, pap_revs, weights, np.linspace(1.5,3.5, 10))
    sim.run_exp()
