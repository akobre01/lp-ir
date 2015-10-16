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

import weights as wgts

def createDir(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError, e:
        if e.errno != 17:
            raise # This was not a "directory exist" error..


def runMatching(n_rev, n_pap, alpha, beta, verbose=False, matcher='affinity', ws=None, weights_file=None):
    # Logging and results
    param_str = '_'.join(map(lambda x: str(x), [matcher, n_rev, n_pap, alpha, beta]))
    now = datetime.datetime.now()
    exec_time = now.strftime("%Y%m%d_%H%M%S%f")
    log_file = "./logs/" + exec_time + "_matching_exp_" + param_str + ".log"
    outdir = './results/matching_exp/' + param_str

    logging.basicConfig(filename=log_file, level=logging.DEBUG)

    print "**************************************************************"
    print "RESULTS TO BE WRITTEN TO: " + str(outdir)
    print "LOG FILE: " + log_file
    print "**************************************************************"

    all_objectives = []
    all_rev_affs = []
    all_pap_affs = []

    weights = ws

    # construct new problem instance and solve for initial solution
    if matcher.lower() == 'makespan':
        logging.info("[MATCHER]: makespan")
        prob = MakespanMatcher(n_rev, n_pap, alpha, beta, weights)
    elif matcher.lower() == 'distortion':
        logging.info("[MATCHER]: distortion")
        prob = DistortionMatcher(n_rev, n_pap, alpha, beta, weights)
    elif matcher.lower() == 'relaxed':
        logging.info("[MATCHER]: relaxed makespan")
        prob = RelaxedMSMatcher(n_rev, n_pap, alpha, beta, weights)
    elif matcher.lower() == 'revpap':
        logging.info("[MATCHER]: relax-reviewer and paper  makespan")
        prob = RelaxRevPaPMatcher(n_rev, n_pap, alpha, beta, weights)
    else:
        logging.info("[MATCHER]: sum total affinity")
        prob = TotAffMatcher(n_rev, n_pap, alpha, beta, weights)

    if verbose:
        prob.turn_on_verbosity()

    start = time.time()
    prob.solve(log_file=log_file)
    t = time.time() - start
    logging.info("[TOTAL TIME]: %f" % t)

    # bookkeeping
    all_rev_affs.append(prob.prev_rev_affs[-1].reshape(-1))
    all_pap_affs.append(prob.prev_pap_affs[-1].reshape(-1))

    # save data to csv
    createDir(outdir)
    createDir(outdir + "/weights")
    createDir(outdir + "/rev_affs")
    createDir(outdir + "/pap_affs")

    np.savetxt(outdir + "/weights/" + exec_time + "-weights.csv", weights, delimiter=',')
    np.savetxt(outdir + "/rev_affs/" + exec_time + "-rev_affs.csv", all_rev_affs, delimiter=',')
    np.savetxt(outdir + "/pap_affs/" + exec_time + "-pap_affs.csv", all_pap_affs, delimiter=',')

    print "**************************************************************"
    print "OBJECTIVE: " + str(prob.objective_val())
    print "RESULTS  WRITTEN TO: " + outdir
    print "**************************************************************"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Experiment Parameters.')
    parser.add_argument('reviewers', type=int, help='the number of reviewers')
    parser.add_argument('papers', type=int, help='the number of papers')
    parser.add_argument('reviews_per_paper', type=int, help='the number of reviews per paper')
    parser.add_argument('max_reviews_per_reviewer', type=int, help='the max number of reviews per reviewer')
    parser.add_argument('matcher', type=str, help='either affinity (default), makespan or two-phase')
    parser.add_argument('-f','--weights_file', type=str, help='file from which to load weights; required set flag')

    parser.add_argument('-v', '--verbose', help='print gurobi output', action='store_true')

    args = parser.parse_args()

    n_rev = args.reviewers
    n_pap = args.papers
    beta = args.reviews_per_paper
    alpha = args.max_reviews_per_reviewer
    ws = np.genfromtxt(args.weights_file)

    runMatching(n_rev, n_pap, alpha, beta, args.verbose, args.matcher, ws, args.weights_file)
