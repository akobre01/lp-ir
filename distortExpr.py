import argparse
import datetime
import math
import numpy as np
import os

from TotAffMatcher import TotAffMatcher
from FairMatcher import FairMatcher
from DistortionMatcher import DistortionMatcher

import weights as wgts

def createDir(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError, e:
        if e.errno != 17:
            raise # This was not a "directory exist" error..


def runDistortionExperiment(n_rev, n_pap, alpha, beta, itrs, outdir, verbose=False, w_samp=None, constr_per_itr=1, bp1=2, bp2=2, matcher='affinity'):
    all_diffs = []
    all_objectives = []
    all_affs = []

    # draw a new set of weights
    if w_samp == 'beta':
        weights = wgts.fromBeta(n_rev, n_pap, bp1, bp2)
    elif w_samp == 'per_rev':
        weights = wgts.skillBased(n_rev, n_pap, bp1, bp2)
    elif w_samp == 'uni':
        weights = wgts.fromUni(n_rev, n_pap)
    else:
        pass #weights from file

    # sample new constraints
    pairs = [ (i,j) for i in range(n_rev) for j in range(n_pap) ]
    arbitraryConsts = np.random.choice(len(pairs), itrs * constr_per_itr, replace=False)

    # construct new problem instance and solve for initial solution
    if matcher.lower() == 'makespan':
        print "MAKESPAN"
        prob = FairMatcher(n_rev, n_pap, alpha, beta, weights)
    elif matcher.lower() == 'distortion':
        print "Selected distortion"
        prob = DistortionMatcher(n_rev, n_pap, alpha, beta, weights)
    else:
        prob = TotAffMatcher(n_rev, n_pap, alpha, beta, weights)

    if verbose:
        prob.turn_on_verbosity()

    prob.solve()

    n_diffs = []
    objectives = []

    # add in each of the new constraints (1 by 1 for now) and resolve the problem
    for i in range(0, itrs):
        for j in range(constr_per_itr):
            print "\tAdding constraint: " + str(i * constr_per_itr + j)
            (next_i, next_j) = pairs[arbitraryConsts[i * constr_per_itr + j]]
            prob.add_hard_const(next_i, next_j)
        prob.solve()
        objectives.append(prob.objective_val())

        # calculate the number of variables that changed between the current and previous sols
        n_diffs.append(prob.num_diffs(prob.prev_sols[-1], prob.prev_sols[-2]))

    # bookkeeping
    all_diffs.append(n_diffs)
    all_objectives.append(objectives)
    all_affs.append(prob.prev_affs[-1].reshape(-1))

    # save data to csv
    createDir(outdir + "/diffs")
    createDir(outdir + "/objs")
    createDir(outdir + "/affs")

    now = datetime.datetime.now()
    exec_time = now.strftime("%Y%m%d_%H%M%S%f")
    np.savetxt(outdir + "/diffs/" + exec_time + "-diffs.csv", all_diffs, delimiter=',')
    np.savetxt(outdir + "/affs/" + exec_time + "-affs.csv", all_affs, delimiter=',')
    np.savetxt(outdir + "/objs/" + exec_time + "-objs.csv", all_objectives, delimiter=',')


if __name__ == "__main__":
    beta_param1 = 0.5
    beta_param2 = 2

    parser = argparse.ArgumentParser(description='Experiment Parameters.')
    parser.add_argument('reviewers', type=int, help='the number of reviewers')
    parser.add_argument('papers', type=int, help='the number of papers')
    parser.add_argument('reviews_per_paper', type=int, help='the number of reviews per paper')
    parser.add_argument('outdir', type=str, help='the directory into which to write the results')
    parser.add_argument('itrs', type=int, help='the number of iterations to run')
    parser.add_argument('consts_per_itr', type=int, help='the number of constraints to add each iteration')
    parser.add_argument('matcher', type=str, help='either affinity (default), makespan or two-phase')

    parser.add_argument('-v', '--verbose', help='print gurobi output', action='store_true')
    parser.add_argument('-b', '--beta', help='draw weights from a beta distribution (parameters ' + str(beta_param1) + ',' + str(beta_param2) + ')', action='store_true')
    parser.add_argument('-p', '--per_reviewer', help='draw weights per reviewer', action='store_true')

    args = parser.parse_args()

    # PARAMETERS (inspired by EMNLP 2015)
    n_rev = args.reviewers
    n_pap = args.papers
    beta = args.reviews_per_paper
    alpha = math.ceil((n_pap * beta) / float(n_rev))    # reviwer cannot review > alpha
    itrs = args.itrs
    outdir = args.outdir
    w_samp = 'beta' if args.beta else None
    w_samp = 'per_rev' if args.per_reviewer else w_samp

    runDistortionExperiment(n_rev, n_pap, alpha, beta, itrs, outdir, args.verbose, w_samp, args.consts_per_itr, beta_param1, beta_param2, args.matcher)
