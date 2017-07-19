import argparse
import numpy as np
import time

from gurobipy import *

from ..matching_models.MakespanMatcher import MakespanMatcher
from ..matching_models.IRMakespanMatcher import IRMakespanMatcher
from ..matching_models.IRDAMakespanMatcher import IRDAMakespanMatcher


class SeqIncreaseMake:
    """A class (but should be refactored, this shouldn't be a class...) that
    represents a paper matching experiment. Each experiment takes an affinity
    matrix, matching parameters and the matching to be run and runs the
    matching. In the case of makespan matchings, this code will sequentially try
    to increase the makespan value (using binary search). A run of this code
    will write all results to a specifed output directory.
    """
    def __init__(self, alpha, beta, weights, mkspns, matcher):
        self.n_rev = np.size(weights, axis=0)
        self.n_pap = np.size(weights, axis=1)
        self.alpha = alpha
        self.beta = beta
        self.weights = weights
        self.mkspns = mkspns
        self.curr_makespan = 0.0
        self.mkspn_and_sol = []
        self.matcher = matcher

    def min_pap(self, assignments):
        """Return the smallest paper assignment score."""
        pap_affs = np.sum(self.weights * assignments, axis=0)
        assert(len(pap_affs) == self.n_pap)
        return np.min(pap_affs)

    def max_pap(self, assignments):
        """Return the largest paper assignment score."""
        pap_affs = np.sum(self.weights * assignments, axis=0)
        assert(len(pap_affs) == self.n_pap)
        return np.max(pap_affs)

    def mean_pap(self, assignments):
        """Return the average paper assignment score."""
        pap_affs = np.sum(self.weights * assignments, axis=0)
        assert(len(pap_affs) == self.n_pap)
        return np.mean(pap_affs)

    def std_pap(self, assignments):
        """Return the standard deviation of paper assignment score."""
        pap_affs = np.sum(self.weights * assignments, axis=0)
        assert(len(pap_affs) == self.n_pap)
        return np.std(pap_affs)

    def solve_with_curr_makespan(self):
        """
        THIS CODE DOES NOT USE WARM STARTING
        """
        if self.matcher == 'bb':
            problem = MakespanMatcher(self.alpha, self.beta, self.weights,
                                      self.curr_makespan)
        elif self.matcher == 'ir':
            problem = IRMakespanMatcher(self.alpha, self.beta, self.weights,
                                        self.curr_makespan)
        elif self.matcher == 'da':
            problem = IRDAMakespanMatcher(self.alpha, self.beta, self.weights,
                                          self.curr_makespan)
        else:
            raise Exception("You must specify the matcher to use")
        problem.solve_with_current_makespan()
        status = problem.status()
        if status == GRB.OPTIMAL:
            self.mkspn_and_sol.append((self.curr_makespan, problem.sol_as_mat()))
        else:
            self.mkspn_and_sol.append((self.curr_makespan, None))
        return (status, problem)

    def largest_makespan(self):
        """Return the largest successful makespan from a set of solutions."""
        return sorted([m_and_sol
                       for m_and_sol in self.mkspn_and_sol
                       if m_and_sol[1] is not None],
                      key=lambda m_and_sol: -m_and_sol[0])[0][0]

    def num_diffs(self, a1, a2):
        """Returns the number of different assignments between a1 and a2."""
        return float(np.sum(np.abs(a1 - a2)))   # this assumes that the

    def survival(self, assignments):
        """Compute the area under the survival curve for the assignment."""
        assert (all([b == self.beta[0] for b in self.beta]))
        assert np.all(self.weights <= 1.0)
        scores = np.sum(assignments * self.weights, axis=0)
        survival_score = 0.0
        for score_threshold in np.linspace(0, self.beta[0], num=100):
            survival_score += len([x for x in scores if x >= score_threshold])
        return float(survival_score) / float(self.n_pap)

    def report_result(self, assignments, prev_assignments, init_assignment, t):
        """Return a line in the stats file.

        Specifically, report:
        1) the makespan used
        2) the number of papers
        3) the number of reviewers
        4) the average number of papers per reviewer
        5) the average number of reviewers per paper
        6) the maximum paper assignment score
        7) the minimum paper assignment score
        8) the mean paper assignment score
        9) the standard deviation of paper assignment scores
        10) the percent of the assignments that have changed from the prev sol
        11) the percent of reviewers who have changed assignments from prev sol
        12) the percent of reviewers who changed assignments from the init sol
        13) the integral of the survival curve
        14) the solution time
        """
        if assignments is not None and prev_assignments is not None:
            overall_percent_change = "%.2f%%" % (100.0 * self.num_diffs(
                assignments, prev_assignments) / np.size(assignments))
            # percet of total reviews that change
            percent_reviews_change = "%.2f%%" % (100.0 * self.num_diffs(
                assignments, prev_assignments) / (
                self.n_pap * np.mean(self.beta) * 2.0))
            # percet of total reviews that changes.
            percent_reviews_change_from_init = "%.2f%%" % (
                100.0 * self.num_diffs(assignments, init_assignment) / (
                    self.n_pap * np.mean(self.beta) * 2.0))
            max_pap = "%.2f" % (self.max_pap(assignments))
            min_pap = "%.2f" % (self.min_pap(assignments))
            mean_pap = "%.2f" % (self.mean_pap(assignments))
            std_pap = "%.2f" % (self.std_pap(assignments))
            survival_score = "%.2f" % (self.survival(assignments))
            obj_val = "%.2f" % (np.sum(self.weights * assignments))
        else:
            overall_percent_change = "----"
            percent_reviews_change = "----"
            percent_reviews_change_from_init = "----"
            max_pap = "----"
            min_pap = "----"
            mean_pap = "----"
            std_pap = "____"
            survival_score = "----"
            obj_val = "----"
        return "\t".join([str(x) for x in ["%.2f" % self.curr_makespan,
                                           self.n_pap,
                                           self.n_rev,
                                           np.mean(self.alpha),
                                           np.mean(self.beta),
                                           max_pap,
                                           min_pap,
                                           mean_pap,
                                           std_pap,
                                           overall_percent_change,
                                           percent_reviews_change,
                                           percent_reviews_change_from_init,
                                           obj_val,
                                           survival_score,
                                           "%.2fs" % float(t)]])

    def run_exp(self, out_file=None, out_file_assign=None):
        """ Run an experiment and report results.

        Perform the experiment and print out where the assignment file is. Then
        generate (and print out) statistics of each successive solution.

        :param out_file: where to write statistics of each solution.
        :param out_file_assign: where to write each assignment matrix
        :return: None.
        """
        print('ASSIGNMENT FILE: %s' % out_file_assign)
        header = "\t".join(["#MKSPN", "#PAP", "#REV", "ALPHA", "BETA", "MAX",
                            "MIN", "MEAN", "STD", "%X", "%XR", "%XR_0", "OBJ",
                            "SUR", "TIME"])
        print(header)
        if out_file is not None:
            out_file.write("%s\n" % header)

        self.solve_with_curr_makespan()
        init_assignment = self.mkspn_and_sol[-1][1]
        prev_assignment = init_assignment
        for mkspn in self.mkspns:
            self.curr_makespan = mkspn
            s = time.time()
            self.solve_with_curr_makespan()
            t = time.time() - s
            assignment = self.mkspn_and_sol[-1][1]
            report = self.report_result(assignment, prev_assignment,
                                        init_assignment, t)
            print(report)
            if out_file is not None:
                out_file.write("%s\n" % report)
            if out_file_assign is not None and assignment is not None:
                assign_file_name = "%s-%f" % (out_file_assign, mkspn)
                np.save(assign_file_name, assignment)
            prev_assignment = assignment
            if assignment is None:
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Arguments for creating weight files.')
    # parser.add_argument('max_load', type=int, help='max # of papers per rev')
    parser.add_argument('coverage', type=int, help='# of reviewers per paper')
    parser.add_argument('weight_file', type=str,
                        help='the file from which to read the weights')
    parser.add_argument('step', type=float,
                        help='the step value by which we increase the makespan')
    parser.add_argument('matcher', type=str,
                        help='the matcher to use, either: "bb" or "ir"')
    parser.add_argument('output', type=str,
                        help='the directory in which to save the results.')
    parser.add_argument("-i", "--init", type=float, help="the initial makespan")
    parser.add_argument("-s", "--single", action='store_true',
                        help="if specified, only run this makespan.")
    args = parser.parse_args()

    coverage = args.coverage
    weights = np.load(args.weight_file)
    weights_name = args.weight_file[
                   args.weight_file.rfind('/') + 1:args.weight_file.rfind('.')]
    n_rev = np.size(weights, axis=0)
    n_pap = np.size(weights, axis=1)
    step = args.step
    rev_max = np.ceil(n_pap * float(coverage) / n_rev)
    matcher = args.matcher
    if args.init:
        init_makespan = args.init
    else:
        init_makespan = 0.0

    mn = init_makespan
    mx = n_pap * coverage
    if args.single:
        mkspns = [mn]
    else:
        mkspns = np.linspace(mn, mx, mx / step + 1)
    matcher_name = 'baseline' if len(mkspns) == 1 and mkspns[0] == 0.0 \
        else args.matcher
    out_dir = args.output
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    stats_file_name = "stats-%s-%s-seqmkspn-%s-%s-%f-%f" % (matcher_name,
                                                            weights_name,
                                                            rev_max,
                                                            args.coverage,
                                                            mn, mx)
    assignment_file_name = "assignment-%s-%s-seqmkspn-%s-%s-%s-%s" % (
        matcher_name, weights_name, rev_max, args.coverage, mn, mx)
    full_stats_file = "%s/%s" % (out_dir, stats_file_name)
    full_assignment_file = "%s/%s" % (out_dir, assignment_file_name)
    # Run increasing makespans and write to stats files
    sim = SeqIncreaseMake([rev_max] * n_rev, [coverage] * n_pap, weights,
                          mkspns, matcher)
    f = open(full_stats_file, 'w')
    sim.run_exp(out_file=f, out_file_assign=full_assignment_file)
    f.close()

    # Write the largest threshold found to file
    max_threshold_file = "mxthresh-%s-alpha-%s-beta-%s-%s-%s" % (
        matcher_name, rev_max, args.coverage, mn, mx)
    f = open('%s/%s' % (out_dir, max_threshold_file), 'w')
    f.write("%f\n" % sim.largest_makespan())
    f.close()
