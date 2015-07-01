import numpy as np

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
