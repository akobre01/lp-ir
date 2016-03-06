import argparse
import os

import numpy as np

from matplotlib import pyplot as plt

def fromBeta(n_rev, n_pap, bp1, bp2):
    return np.random.beta(bp1, bp2, (n_rev, n_pap))

def skillBased(n_rev, n_pap, bp1, bp2, reviewer_alpha=2):
    weights = []
    for i in range(n_rev):
        reviewer_skill = np.random.beta(bp1, bp2)
        reviewer_beta = ((1.0 - reviewer_skill) * reviewer_alpha) / reviewer_skill
        weights.append(np.random.beta(reviewer_alpha, reviewer_beta, n_pap))
    return np.array(weights)

def skillAndDifficulty(n_rev, n_pap, bp1, bp2, alpha=2):
    weights = []
    skills = []
    ease = []
    for i in range(n_rev):
        skills.append(np.random.beta(bp1, bp2))
    for j in range(n_pap):
        ease.append(np.random.beta(bp1, bp2))
    for i in range(n_rev):
        weights.append([])
        for j in range(n_pap):
            beta = (2.0 - skills[i] - ease[j]) * alpha / (skills[i] + ease[j])
            weights[i].append(np.random.beta(alpha,beta,1))
    return np.array(weights)

def fromUni(n_rev, n_pap):
    return np.random.rand(n_rev, n_pap)

def showWeights(weights):
    weights = weights.reshape(weights.shape[:2])
    reviewer_order = np.array(sorted(weights, key=lambda row: np.sum(row)))
    paper_order = np.array(sorted(reviewer_order.T, key=lambda row: -np.sum(row))).T
    cMap = plt.get_cmap("Blues")

    plt.subplot(1,1,1)
    reviewer_heatmap = plt.pcolor(paper_order, cmap=cMap)
    plt.colorbar(reviewer_heatmap)
    plt.title("Reviewer-paper Affinities")
    plt.xlabel("Papers")
    plt.ylabel("Reviewers")
    return plt

def integerWeights(n_rev, n_pap, bp1, bp2, reviewer_alpha=2):
    weights = skillAndDifficulty(n_rev, n_pap, bp1, bp2, reviewer_alpha)
    for i in range(np.size(weights, axis=0)):
        for j in range(np.size(weights, axis=1)):
            if weights[i,j] < 0.2:
                weights[i,j] = 0.0
            elif weights[i,j] < 0.4:
                weights[i,j] = 1.0
            elif weights[i,j] < 0.6:
                weights[i,j] = 2.0
            elif weights[i,j] < 0.8:
                weights[i,j] = 3.0
            else:
                weights[i,j] = 4.0
    return weights

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for creating weight files.')
    parser.add_argument('nrev', type=int, help='# of reviewers')
    parser.add_argument('npap', type=int, help='# of papers')
    parser.add_argument('bp1', type=float, help='alpha parameter for the beta distribution')
    parser.add_argument('bp2', type=float, help='beta parameter for the beta distribution')
    parser.add_argument('structure', type=str, help='either uniform, skill_based, skill_and_difficulty or integer')
    parser.add_argument('--plot', action='store_true')

    args = parser.parse_args()

    def createDir(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError, e:
            if e.errno != 17:
                raise # This was not a "directory exist" error..

    outdir = '../../data/train/'
    outdir += "-".join(map(lambda x: str(x), [args.nrev, args.npap, args.bp1, args.bp2, args.structure]))
    out_file = '%s/weights.txt' % outdir
    plot_file = '%s/weights.png' % outdir

    createDir(outdir)
    if args.structure == 'skill_based':
        weights = skillBased(args.nrev, args.npap, args.bp1, args.bp2)
    elif args.structure == 'uniform':
        weights = fromUni(args.nrev, args.npap)
    elif args.structure == 'integer':
        weights = integerWeights(args.nrev, args.npap, args.bp1, args.bp2)
    elif args.structure == 'skill_and_difficulty':
        weights = skillAndDifficulty(args.nrev, args.npap, args.bp1, args.bp2)

    plt = showWeights(weights)
    plt.savefig(plot_file)
    if args.plot:
        plt.show()

    np.savetxt(out_file, weights)
