import numpy as np
from MatchingProblem import MatchingProblem
from matplotlib import pyplot as plt

# PARAMETERS
n_rev = 40
n_pap = 60
alpha = 5
beta = 3
weights = np.random.rand(n_rev, n_pap)
nConsts = 20
n_exps = 10

all_diffs = []
all_objectives = []
for e in range(n_exps):
    # Constraints to add
    pairs = [ (i,j) for i in range(n_rev) for j in range(n_pap) ]
    arbitraryConsts = np.random.choice(len(pairs), nConsts, replace=False)

    prob = MatchingProblem(n_rev, n_pap, alpha, beta, weights)
    prob.solve()

    n_diffs = []
    objectives = []
    for i in range(0,nConsts):
        (next_i, next_j) = pairs[arbitraryConsts[i]]
        prob.add_hard_const(next_i, next_j)
        prob.solve()

        objectives.append(prob.objective_val())
        n_diffs.append(prob.num_diffs(prob.prev_sols[-1], prob.prev_sols[-2]))
    all_diffs.append(n_diffs)
    all_objectives.append(objectives)

mean_diffs = np.mean(np.array(all_diffs),0)
std_diffs = np.std(np.array(all_diffs),0)

mean_objs = np.mean(np.array(all_objectives), 0)
std_objs = np.std(np.array(all_objectives), 0)
plt.figure(1)
plt.subplot(211)
plt.errorbar(range(len(mean_diffs)), mean_diffs, yerr=std_diffs)
plt.title("REVIEWERS: " + str(n_rev) + "; PAPERS: " + str(n_pap) + "; ALPHA: " + str(alpha) + "; BETA: " + str(beta))
plt.ylabel("Num. Diff. Assignments")

plt.subplot(212)
plt.errorbar(range(len(mean_objs)), mean_objs, yerr=std_objs)
plt.xlabel("Solution Number")
plt.ylabel("Objective Value")
plt.show()
