import numpy as np
from TotAffMatcher import TotAffMatcher
from matplotlib import pyplot as plt

# PARAMETERS (inspired by EMNLP)
n_rev = 500
n_pap = 900
alpha = 6    # reviewers cannot review more than alpha papers
beta = 3     # each paper must be reviewed beta times

nConsts = 10  # number of constraints to add (1 per iteration)
n_exps = 3   # number of times to run experiment

def runDistortionExperiment():
    all_diffs = []
    all_objectives = []
    all_affs = []

    for e in range(n_exps):
        # draw a new set of weights
        weights = np.random.rand(n_rev, n_pap)

        # sample new constraints
        pairs = [ (i,j) for i in range(n_rev) for j in range(n_pap) ]
        arbitraryConsts = np.random.choice(len(pairs), nConsts, replace=False)

        # construct new problem instance and solve for initial solution
        prob = TotAffMatcher(n_rev, n_pap, alpha, beta, weights)
        prob.solve()

        n_diffs = []
        objectives = []

        # add in each of the new constraints (1 by 1 for now) and resolve the problem
        for i in range(0, nConsts):
            (next_i, next_j) = pairs[arbitraryConsts[i]]
            prob.add_hard_const(next_i, next_j)
            prob.solve()
            objectives.append(prob.objective_val())

            # calculate the number of variables that changed between the current and previous sols
            n_diffs.append(prob.num_diffs(prob.prev_sols[-1], prob.prev_sols[-2]))

        # bookkeeping
        all_diffs.append(n_diffs)
        all_objectives.append(objectives)
        all_affs.append(prob.prev_affs[-1].reshape(-1))

        #mean_affs = np.mean(np.array(all_affs), 0)
        #std_affs = np.std(np.array(all_affs),0)

        #ind = np.arange(np.size(mean_affs))
        #width = 0.2
        #plt.bar(ind + width, mean_affs, width, yerr=std_affs)
        #plt.xlabel("Iteration")
        #plt.ylabel("Objective Value")
        #plt.show()

    mean_diffs = np.mean(np.array(all_diffs), 0)
    std_diffs = np.std(np.array(all_diffs),0)
    mean_objs = np.mean(np.array(all_objectives), 0)
    std_objs = np.std(np.array(all_objectives), 0)

    print np.array(all_affs).shape
    print np.mean(np.array(all_affs),0)
    print np.mean(np.array(all_affs),1)

    mean_affs = np.mean(np.array(all_affs), 0)
    std_affs = np.std(np.array(all_affs),0)

    plt.figure(1)
    plt.subplot(311)
    plt.errorbar(range(len(mean_diffs)), mean_diffs, yerr=std_diffs)
    plt.title("REVIEWERS: " + str(n_rev) + "; PAPERS: " + str(n_pap) + "; ALPHA: " + str(alpha) + "; BETA: " + str(beta))
    plt.ylabel("Num. Diff. Assignments")

    plt.subplot(312)
    plt.errorbar(range(len(mean_objs)), mean_objs, yerr=std_objs)
    plt.xlabel("Iteration")
    plt.ylabel("Objective Value")

    plt.subplot(313)
    ind = np.arange(len(mean_affs))
    print ind
    width = 0.2
    plt.bar(ind + width, mean_affs, width, yerr=std_affs)
    plt.xlabel("Iteration")
    plt.ylabel("Objective Value")

    plt.show()

runDistortionExperiment()
