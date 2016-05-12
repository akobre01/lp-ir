import argparse
import os

import numpy as np

import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from weights import showWeights

def naiveTopical(n_rev, n_pap, n_tops, alpha=0.2):
    """
    Returns a tensor of nrev x npap x ntops.  For each reviewer
    There is a normalized vector of topics per paper. One problem
    with this is that each reviewer has a different normalized topic
    vector for every paper (but a reviewer's topical expertise should
    remain somewhat constant)
    """
    return np.random.dirichlet(np.array([alpha] * n_tops), (n_rev, n_pap))

def naiveMinTopical(n_rev, n_pap, n_tops, rev_alpha=0.2, pap_alpha=0.1):
    """
    Draw an affinity tensor yielding a normalized expertise vector for each
    reviewer for each paper. Then draw a topic tensor yielding a topic vector
    for every paper. Produce a third tensor of the same dimension that holds the
    minimum between the reviewers expertise for a topic and the paper's expression
    of that topic (similar to the Kuo et. al. paper). The score of assigning a
    reviewer to a paper is the sum along the topic dimension of the third matrix.
    """
    affinities = np.random.dirichlet(np.array([rev_alpha] * n_tops), n_rev)
    paper_tops = np.random.dirichlet(np.array([pap_alpha] * n_tops), n_pap)
    # convert these matrices to tensors with the dimensions (n_rev, n_pap, n_tops)
    reviewer_tensor = np.tile(affinities[:,np.newaxis,:], (1,n_pap,1))
    paper_tensor = np.tile(paper_tops[np.newaxis,:,:], (n_rev,1,1))
    score_mat = np.sum(np.minimum(reviewer_tensor, paper_tensor), axis=2)
    return score_mat, reviewer_tensor, paper_tensor

def skillTopical(n_rev, n_pap, n_tops, bp1=0.2, bp2=0.1, reviewer_alpha=2.0, paper_alpha=0.5):
    """
    Similar to the naiveMinTopical function above except that instead of drawing
    topical expertise (for reviewers and papers) from the same dirichlet every time,
    first we draw a skill parameters for each reviewer and for each paper and draw
    scores based on that.
    """
    reviewers = []
    for i in range(n_rev):
        reviewer_skill = np.random.beta(bp1, bp2)
        reviewer_beta = ((1.0 - reviewer_skill) * reviewer_alpha) / reviewer_skill
        rev_topics = np.random.beta(reviewer_alpha, reviewer_beta, n_tops)
        rev_topics = rev_topics / np.sum(rev_topics)
        reviewers.append(np.random.dirichlet(rev_topics))

    papers = []
    for i in range(n_pap):
        # paper_skill = np.random.beta(bp1, bp2)
        # paper_beta = ((1.0 - paper_skill) * paper_alpha) / paper_skill
        paper_alpha = 1.0
        paper_beta = 1.0
        paper_topics = np.random.beta(paper_alpha, paper_beta, n_tops)
#        paper_topics = paper_topics / np.sum(paper_topics)
        papers.append(np.random.dirichlet(paper_topics))

    # convert these matrices to tensors with the dimensions (n_rev, n_pap, n_tops)
    reviewer_tensor = np.tile(np.array(reviewers)[:,np.newaxis,:], (1,n_pap,1))
    paper_tensor = np.tile(np.array(papers)[np.newaxis,:,:], (n_rev,1,1))
    score_mat = np.sum(np.minimum(reviewer_tensor, paper_tensor), axis=2)
    return score_mat, reviewer_tensor, paper_tensor


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for creating weight files.')
    parser.add_argument('nrev', type=int, help='# of reviewers')
    parser.add_argument('npap', type=int, help='# of papers')
    parser.add_argument('ntops', type=int, help='# of topics')
    parser.add_argument('bp1', type=float, help='alpha parameter for the beta distribution')
    parser.add_argument('bp2', type=float, help='beta parameter for the beta distribution')
    parser.add_argument('structure', type=str, help='either: topical, skill_topical')
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
    out_affinity = '%s/weights' % outdir
    out_revs = '%s/rev_tensor' % outdir
    out_paps = '%s/pap_tensor' % outdir
    plot_file = '%s/weights.png' % outdir

    createDir(outdir)
    if args.structure == 'topical':
        score_mat, rev_tensor, paper_tensor = naiveMinTopical(args.nrev, args.npap, args.ntops, args.bp1, args.bp2)
    elif args.structure == 'skill_topical':
        score_mat, rev_tensor, paper_tensor = skillTopical(args.nrev, args.npap, args.ntops, args.bp1, args.bp2)

    plt = showWeights(score_mat)
    plt.savefig(plot_file)
    if args.plot:
        plt.show()

    print "OUTFILE: %s" % out_affinity
    np.save(out_affinity, score_mat)
    np.save(out_revs, rev_tensor)
    np.save(out_paps, paper_tensor)
