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
