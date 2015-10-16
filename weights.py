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

def fromUni(n_rev, n_pap):
    return np.random.rand(n_rev, n_pap)

def showWeights(weights):
    reviewer_order = np.array(sorted(weights, key=lambda row: np.sum(row)))
    paper_order = np.array(sorted(weights.T, key=lambda row: np.sum(row))).T
    cMap = plt.get_cmap("Blues")

    plt.subplot(2,1,1)
    reviewer_heatmap = plt.pcolor(reviewer_order, cmap=cMap)
    plt.colorbar(reviewer_heatmap)
    plt.title("Reviewer-paper Affinities")
    plt.xlabel("Papers")
    plt.ylabel("Reviewers")
    plt.subplot(2,1,2)
    paper_heatmap = plt.pcolor(paper_order, cmap=cMap)
    plt.colorbar(paper_heatmap)
    plt.title("Reviewer-paper Affinities")
    plt.xlabel("Papers")
    plt.ylabel("Reviewers")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for creating weight files.')
    parser.add_argument('name', type=str, help='The name of the file')
    parser.add_argument('nrev', type=int, help='# of reviewers')
    parser.add_argument('npap', type=int, help='# of papers')
    parser.add_argument('bp1', type=float, help='alpha parameter for the beta distribution')
    parser.add_argument('bp2', type=float, help='beta parameter for the beta distribution')

    args = parser.parse_args()

    def createDir(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError, e:
            if e.errno != 17:
                raise # This was not a "directory exist" error..

    outdir = './weights/'
    outfile = outdir + "-".join(map(lambda x: str(x), [args.name, args.nrev, args.npap, args.bp1, args.bp2, "skill_based"])) + ".out"

    createDir(outdir)
    weights = skillBased(args.nrev, args.npap, args.bp1, args.bp2)
    np.savetxt(outfile, weights)
