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

    def min_pap(self, assignments):
        pap_affs = np.sum(self.weights * assignments, axis=0)
        assert(len(pap_affs) == self.n_pap)
        return np.min(pap_affs)

    def max_pap(self, assignments):
        pap_affs = np.sum(self.weights * assignments, axis=0)
        assert(len(pap_affs) == self.n_pap)
        return np.max(pap_affs)

    def mean_pap(self, assignments):
        pap_affs = np.sum(self.weights * assignments, axis=0)
        assert(len(pap_affs) == self.n_pap)
        return np.mean(pap_affs)

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

    def largest_makespan(self):
        return sorted(filter(lambda (x,y): y is not None,
                             self.mkspn_and_sol),
                      key=lambda (x,y): -x)[0][0]

    def num_diffs(self, a1, a2):
        return float(np.sum(np.abs(a1 - a2)))   # this assumes that the

    def report_result(self, assignments, prev_assignments, init_assignment, t):
        if assignments is not None and prev_assignments is not None:
            overall_percent_change = "%.2f%%" % (100.0 * self.num_diffs(assignments, prev_assignments) / np.size(assignments))
            percent_reviews_change = "%.2f%%" % (100.0 * self.num_diffs(assignments, prev_assignments) / (self.n_pap * self.beta * 2.0))   # percet of total reviews that change
            percent_reviews_change_from_init = "%.2f%%" % (100.0 * self.num_diffs(assignments, init_assignment) / (self.n_pap * self.beta * 2.0))   # percet of total reviews that changes
            max_pap = "%.2f" % (self.max_pap(assignments))
            min_pap = "%.2f" % (self.min_pap(assignments))
            mean_pap = "%.2f" % (self.mean_pap(assignments))
        else:
            overall_percent_change = "----"
            percent_reviews_change = "----"
            percent_reviews_change_from_init = "----"
            max_pap = "----"
            min_pap = "----"
            mean_pap = "----"
        return "\t".join(map(lambda x: str(x), ["%.2f" % self.curr_makespan,
                                                self.n_pap,
                                                self.n_rev,
                                                self.alpha,
                                                self.beta,
                                                max_pap,
                                                min_pap,
                                                mean_pap,
                                                overall_percent_change,
                                                percent_reviews_change,
                                                percent_reviews_change_from_init,
                                                "%.2fs" % float(t)]))

    def run_exp(self, out_file=None):
        header = "\t".join(["#MKSPN","#PAP", "#REV", "ALPHA", "BETA", "MAX", "MIN", "MEAN", "%X", "%R", "%R0", "TIME"])
        print header
        if out_file is not None:
            out_file.write("%s\n" % header)

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
            report = self.report_result(assignment, prev_assignment, init_assignment, t)
            print report
            if out_file is not None:
                out_file.write("%s\n" % report)
            prev_assignment = assignment
            if assignment is None:
                break


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

    out_dir = args.weight_file[:args.weight_file.rfind('/')]
    stats_file_name = "seqmkspn.stats"
    full_stats_file = "%s/%s" % (out_dir, stats_file_name)
    max_threshold_file = "mxthresh-MakespanMatcher-alpha-%s-beta-%s" % (args.rev_max, args.pap_revs)


    mn = 0
    mx = n_pap * pap_revs
    mkspns = np.linspace(mn, mx, mx / step + 1)

    # Run increasing makespans and write to stats file
    sim = SeqIncreaseMake(n_rev, n_pap, rev_max, pap_revs, weights, mkspns)
    f = open(full_stats_file, 'w')
    sim.run_exp(f)
    f.close()

    # Write the largest threshold found to file
    f = open('%s/%s' % (out_dir, max_threshold_file), 'w')
    f.write("%f\n" % sim.largest_makespan())
    f.close()
