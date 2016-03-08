import argparse
import datetime
import logging
import math
import numpy as np
import time
import os

from TotAffMatcher import TotAffMatcher
from MakespanMatcher import MakespanMatcher
from DistortionMatcher import DistortionMatcher
from RelaxedMSMatcher import RelaxedMSMatcher
from RelaxRevPaPMatcher import RelaxRevPaPMatcher
from CompleteRelaxationMSMatcher import CompleteRelaxationMSMatcher

import weights as wgts

def create_dir(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError, e:
        if e.errno != 17:
            raise # This was not a "directory exist" error..


class MatchingExp:
    """Run a matching experiment
    """

    def __init__(self, matcher, weight_file, alpha, beta, log_file_dir=None, verbose=False):
        # construct new problem instance
        self.weights_file = weight_file
        self.weights = np.genfromtxt(weight_file)
        if matcher.lower() == 'makespan':
            self.matcher = MakespanMatcher(alpha, beta, self.weights)
        elif matcher.lower() == 'distortion':
            self.matcher = DistortionMatcher(alpha, beta, self.weights)
        elif matcher.lower() == 'relaxed':
            self.matcher = RelaxedMSMatcher(alpha, beta, self.weights)
        elif matcher.lower() == 'complete-relax':
            self.matcher = CompleteRelaxationMSMatcher(alpha, beta, self.weights)
        elif matcher.lower() == 'revpap':
            self.matcher = RelaxRevPaPMatcher(alpha, beta, self.weights)
        else:
            self.matcher = TotAffMatcher(alpha, beta, self.weights)

        # Logging and results
        now = datetime.datetime.now()
        exec_time = now.strftime("%Y%m%d_%H%M%S%f")
        param_str = "a-%s_b-%s_r-%s_p-%s" % \
                    (self.matcher.alpha, self.matcher.beta, self.matcher.n_rev, self.matcher.n_pap)

        logging_base = './logs' if log_file_dir == None else log_file_dir
        results_base = './results'

        last_slash = self.weights_file.rfind('/')
        second_to_last_slash = self.weights_file[:last_slash].rfind('/')
        weight_file_name = self.weights_file[second_to_last_slash + 1 : last_slash]

        create_dir(logging_base)
        create_dir("%s/%s" % (logging_base, weight_file_name))
        create_dir("%s/%s" % (results_base, weight_file_name))
        create_dir("%s/%s/%s" % (logging_base, weight_file_name, param_str))
        create_dir("%s/%s/%s" % (results_base, weight_file_name, param_str))

        log_dir = "%s/%s/%s" % (logging_base, weight_file_name, param_str)
        res_dir = "%s/%s/%s" % (results_base, weight_file_name, param_str)

        self.log_file = "%s/%s-%s.log" % (log_dir, exec_time, self.matcher.__class__.__name__)
        self.res_file = "%s/%s-%s" % (res_dir, exec_time, self.matcher.__class__.__name__)

        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)

        print "**************************************************************"
        print "RESULTS WRITTEN TO PREFIX: %s" % self.res_file
        print "LOGS WRITTEN TO: %s" % self.log_file
        print "**************************************************************"

        if verbose:
            self.matcher.turn_on_verbosity()

        logging.info("[MATCHER]: %s" % self.matcher.__class__.__name__)


    def solve(self):
        start = time.time()
        self.matcher.solve(log_file=self.log_file)
        t = time.time() - start
        logging.info("[TOTAL TIME]: %f" % t)

        # construct the matrix of assignments
        solution = self.matcher.prev_sols[-1]
        assn_mat = np.array([
            np.array([ solution[self.matcher.var_name(i,j)]  for j in range(self.matcher.n_pap) ])
            for i in range(self.matcher.n_rev) ])

        # makespan
        if self.matcher.__class__.__name__.lower() in set(['MakespanMatcher']):
            makespan = np.array([self.matcher.makespan])
        else:
            makespan = np.array([0.0])

        # bookkeeping
        all_rev_affs = []
        all_pap_affs = []

        all_rev_affs.append(self.matcher.prev_rev_affs[-1].reshape(-1))
        all_pap_affs.append(self.matcher.prev_pap_affs[-1].reshape(-1))

        np.savetxt('%s-rev_affs.csv' % self.res_file, all_rev_affs, delimiter=',')
        np.savetxt('%s-pap_affs.csv' % self.res_file, all_pap_affs, delimiter=',')
        np.savetxt('%s-assignments.csv' % self.res_file, assn_mat, delimiter=',')
        np.savetxt('%s-makespan.csv' % self.res_file, makespan, delimiter=',')

        assignment_file = "%s-assignments.csv" % self.res_file
        makespan_file = '%s-makespan.csv' % self.res_file

        print "**************************************************************"
        print "OBJECTIVE: %s" % str(self.matcher.objective_val())
        print "WEIGHTS used: %s" % self.weights_file
        print "ASSIGNMENTS written to: %s" % assignment_file
        print "MAKESPAN written to: %s" % makespan_file
        print "to produce stats of the result run:"
        print "python analyzeMatching.py %s %s -m %s" % (self.weights_file, assignment_file, makespan_file)
        print "**************************************************************"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Experiment Parameters.')
    parser.add_argument('max_reviews_per_reviewer',
                        type=int, help='the max number of reviews per reviewer')
    parser.add_argument('reviews_per_paper',
                        type=int, help='the number of reviews per paper')
    parser.add_argument('matcher',
                        type=str, help='either affinity (default), makespan or two-phase')
    parser.add_argument('weights_file',
                        type=str, help='file from which to load weights; required set flag')
    parser.add_argument('-l','--log_file_dir',
                        type=str, help='the base directory into which to write the log of this run')
    parser.add_argument('-v', '--verbose',
                        help='print gurobi output', action='store_true')

    args = parser.parse_args()
    matchingExp = MatchingExp(args.matcher,
                              args.weights_file,
                              args.max_reviews_per_reviewer,
                              args.reviews_per_paper,
                              args.log_file_dir,
                              args.verbose)
    matchingExp.solve()
