import sys
import numpy as np
from munkres import Munkres

class WGRAP(object):
    """
    Implements the weighted coverage group base reviewer assignment problem
    inference algorithm in Kou et. al. (2015)

    alpha - the maximum number of papers any reviewer can be assigned
    beta - the number of reviews required per paper
    """

    def __init__(self, rev_mat, pap_mat, alpha, beta):
        self.munkres = Munkres()
        self.rev_mat = rev_mat
        self.pap_mat = pap_mat
        self.alpha = alpha
        self.beta = beta
        self.nrevs_per_round = np.ceil(self.alpha / self.beta)
        self.curr_assignment = np.zeros((np.size(self.rev_mat, axis=0),
                                         np.size(self.pap_mat, axis=0)))

    def group_score(self, revs, pap):
        if not revs:
            return 0.0
        group_max = np.amax(self.rev_mat[revs], axis=0)
        return np.sum(np.minimum(group_max, self.pap_mat[pap])) / float(np.sum(self.pap_mat[pap]))

    def marginal_gain(self, g1, g2, pap):
        return self.group_score(g2, pap) - self.group_score(g1, pap)

    # I need some code that will create the matrix that I want to run
    # munkres algorithm on
    def curr_rev_group(self, paper):
        return np.nonzero(self.curr_assignment[:,paper])[0]

    def marg_gain_for_rev_pap(self, rev, paper):
        g1 = self.curr_rev_group(paper)
        assert rev not in set(g1)
        if not g1:
            g2 = [rev]
        else:
            g2 = g1 + [rev]
        return self.marginal_gain(g1, g2, paper)

    def marg_gain_for_rev(self, rev):
        mg = []
        for pap in range(np.size(self.pap_mat, axis=0)):
            mg.append(self.marg_gain_for_rev_pap(rev, pap))
        return mg

    def curr_n_revs(self, rev):
        return np.sum(self.curr_assignment[rev,:])

    def _construct_matching_mat(self):
        rows = []
        rows_to_revs = {}
        for rev in range(np.size(self.rev_mat, axis=0)):
            n_rows = int(np.min((self.alpha - self.curr_n_revs(rev), self.nrevs_per_round)))
            for row in range(n_rows):
                rows_to_revs[len(rows)] = rev
                rows.append(self.marg_gain_for_rev(rev))
        return rows, rows_to_revs

    def _solve_assignment_and_update(self, rows, rows_to_revs, max_val = 10.0):
        print rows
        cost_matrix = self.munkres.make_cost_matrix(rows, lambda v: max_val - v)
        indexes = self.munkres.compute(cost_matrix)
        print cost_matrix
        for row, col in indexes:
            print row, col
            value = rows[row][col]
            self.curr_assignment[rows_to_revs[row],col] = 1
            print '(%d, %d) -> %f' % (row, col, value)


if __name__ == "__main__":
    rev_mat_file = "/Users/akobren/software/repos/git/lp-ir/data/train/kou_et_al/kou_rev_mat.npy"
    pap_mat_file = "/Users/akobren/software/repos/git/lp-ir/data/train/kou_et_al/kou_rev_mat.npy"
    alpha = 1
    beta = 1
    rev_mat = np.load(rev_mat_file)
    pap_mat = np.load(pap_mat_file)
    rev_mat = np.array([[0.25, 0.25, 0.5],
                        [0.25, 0.5, 0.25],
                        [0.5, 0.25, 0.25]])
    pap_mat = np.array([[0.25, 0.5, 0.25],
                        [0.5, 0.25, 0.25],
                        [0.25, 0.25, 0.5]])
    wgrap = WGRAP(rev_mat, pap_mat, alpha, beta)

    rows, rows_to_revs = wgrap._construct_matching_mat()
    wgrap._solve_assignment_and_update(rows, rows_to_revs)
