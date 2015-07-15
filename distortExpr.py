import argparse
import numpy as np
import math

from TotAffMatcher import TotAffMatcher
from matplotlib import pyplot as plt

import weights as wgts

def runDistortionExperiment(n_rev, n_pap, alpha, beta, itrs, n_exps, verbose=False, w_samp=None, constr_per_itr=1, bp1=2, bp2=2):
    all_diffs = []
    all_objectives = []
    all_affs = []

    for e in range(n_exps):
        print "Running Experiment: " + str(e)

        # draw a new set of weights
        if w_samp == 'beta':
            weights = wgts.fromBeta(n_rev, n_pap, bp1, bp2)
        elif w_samp == 'per_rev':
            weights = wgts.skillBased(n_rev, n_pap, bp1, bp2)
        else:
            weights = wgts.fromUni(n_rev, n_pap)

        # print heat map of reviewer weights
#        wgts.showWeights(weights)

        # sample new constraints
        pairs = [ (i,j) for i in range(n_rev) for j in range(n_pap) ]
        arbitraryConsts = np.random.choice(len(pairs), itrs * constr_per_itr, replace=False)

        # construct new problem instance and solve for initial solution
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

    mean_diffs = np.mean(np.array(all_diffs), 0)
    std_diffs = np.std(np.array(all_diffs),0)
    mean_objs = np.mean(np.array(all_objectives), 0)
    std_objs = np.std(np.array(all_objectives), 0)
    mean_affs = np.mean(np.array(all_affs), 0)
    std_affs = np.std(np.array(all_affs),0)

    plt.figure(1)
    plt.subplot(311)
    plt.errorbar(range(len(mean_diffs)), mean_diffs, yerr=std_diffs)
    plt.title("REVIEWERS: " + str(n_rev) + "; PAPERS: " + str(n_pap) + "; ALPHA: " +
              str(alpha) + "; BETA: " + str(beta))
    plt.ylabel("Num. Diff. Assignments")

    plt.subplot(312)
    plt.errorbar(range(len(mean_objs)), mean_objs, yerr=std_objs)
    plt.xlabel("Iteration")
    plt.ylabel("Objective Value")

    plt.subplot(313)
#    ind = np.arange(len(mean_affs))
#    width = 0.2
#    plt.bar(ind + width, mean_affs, width, yerr=std_affs)
    plt.hist(mean_affs, bins=alpha * 20)
    plt.xlabel("Reviewer Affinity")
    plt.ylabel("# of Sols")
    plt.show()

if __name__ == "__main__":
    beta_param1 = 0.5
    beta_param2 = 2

    parser = argparse.ArgumentParser(description='Experiment Parameters.')
    parser.add_argument('reviewers', type=int, help='the number of reviewers')
    parser.add_argument('papers', type=int, help='the number of papers')
    parser.add_argument('reviews_per_paper', type=int, help='the number of reviews per paper')
    parser.add_argument('experiments', type=int, help='the number of experiment repetitions')
    parser.add_argument('itrs', type=int, help='the number of iterations to run')
    parser.add_argument('consts_per_itr', type=int, help='the number of constraints to add each iteration')
    parser.add_argument('-v', '--verbose', help='print gurobi output', action='store_true')
    parser.add_argument('-b', '--beta', help='draw weights from a beta distribution (parameters ' + str(beta_param1) + ',' + str(beta_param2) + ')', action='store_true')
    parser.add_argument('-p', '--per_reviewer', help='draw weights per reviewer', action='store_true')

    args = parser.parse_args()

    # PARAMETERS (inspired by EMNLP)
    n_rev = args.reviewers
    n_pap = args.papers
    beta = args.reviews_per_paper
    alpha = math.ceil((n_pap * beta) / float(n_rev))    # reviwer cannot review > alpha
    itrs = args.itrs
    n_exps = args.experiments
    w_samp = 'beta' if args.beta else None
    w_samp = 'per_rev' if args.per_reviewer else w_samp

    runDistortionExperiment(n_rev, n_pap, alpha, beta, itrs, n_exps, args.verbose, w_samp, args.consts_per_itr, beta_param1, beta_param2)
