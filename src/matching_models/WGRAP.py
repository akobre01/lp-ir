from scipy.optimize import linear_sum_assignment
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

        reviewer_tensor = np.tile(np.array(self.rev_mat)[:,np.newaxis,:], (1,len(self.pap_mat),1))
        paper_tensor = np.tile(np.array(self.pap_mat)[np.newaxis,:,:], (len(self.rev_mat),1,1))
        self.score_mat = np.sum(np.minimum(reviewer_tensor, paper_tensor), axis=2)

        self.alpha = alpha
        self.beta = beta
        self.nrevs_per_round = np.ceil(self.alpha / self.beta)
        self.curr_assignment = np.zeros((np.size(self.rev_mat, axis=0),
                                         np.size(self.pap_mat, axis=0)))

    def group_score(self, revs, pap):
        if not any(revs):
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
        if not any(g1):
            g2 = [rev]
        else:
            g2 = []
            g2.extend(g1)
            g2.append(rev)
        return self.marginal_gain(g1, g2, paper)

    def marg_gain_for_rev(self, rev):
        mg = []
        for pap in range(np.size(self.pap_mat, axis=0)):
            if self.curr_assignment[rev, pap] == 1.0:
                mg.append(-1.0)   # should never reassign a reviewer to the same paper
            else:
                mg.append(self.marg_gain_for_rev_pap(rev, pap))
        return mg

    def curr_n_revs(self, rev):
        return np.sum(self.curr_assignment[rev,:])

    def _construct_matching_mat(self, post_refine=False):
        rows = []
        rows_to_revs = {}
        for rev in range(np.size(self.rev_mat, axis=0)):
            if post_refine:
                n_rows = int(self.alpha - self.curr_n_revs(rev))
            else:
                n_rows = int(np.min((self.alpha - self.curr_n_revs(rev), self.nrevs_per_round)))

            if n_rows > 0:
                rev_marg_gain = self.marg_gain_for_rev(rev)

            for row in range(n_rows):
                rows_to_revs[len(rows)] = rev
                rows.append(rev_marg_gain[:])
        return rows, rows_to_revs

    def refine(self, R=0.01, l=0.5, itr=0, show=False):
        """
        Implements 1 iteration of stochastic refinement
        """
        for pap in range(np.size(self.pap_mat, axis=0)):
            assigned_revs = np.nonzero(self.curr_assignment[:,pap])[0]
            assert len(assigned_revs) > 0
            rev_scores = []
            for rev in assigned_revs:
                assert self.curr_assignment[rev,pap] == 1.0
                r_score = np.exp(-l * itr) * \
                          self.score_mat[rev, pap] / np.sum(self.score_mat[rev,:])
                r_score = np.max((r_score, 1.0 / R))
                rev_scores.append(r_score)
            rev_scores = np.array(rev_scores)
            inv_rev_scores = np.sum(rev_scores) - rev_scores
            normed_inv_rev_scores = inv_rev_scores / np.sum(inv_rev_scores)
            sample = np.nonzero(np.random.multinomial(1, normed_inv_rev_scores))[0]
            if show:
                print normed_rev_scores
                print sample
            rev_to_remove = assigned_revs[sample]
            assert self.curr_assignment[rev_to_remove, pap] == 1.0
            self.curr_assignment[rev_to_remove, pap] = 0.0

    def _solve_assignment_and_update(self, rows, rows_to_revs, max_val = 10.0, show=False):
        """
        Implements 1 iteration of stagewise deepening (no stochastic refinement)
        """
        if show:
            print rows
        cost_matrix = self.munkres.make_cost_matrix(rows, lambda v: max_val - v)
        #indexes = self.munkres.compute(cost_matrix)
        row_inds, col_inds = linear_sum_assignment(np.array(cost_matrix))
        if show:
            print cost_matrix
        # for row, col in indexes:
        for row, col in zip(row_inds, col_inds):
            self.curr_assignment[rows_to_revs[row],col] = 1
            if show:
                value = rows[row][col]
                print '(%d, %d) -> %f' % (row, col, value)

    def solve(self):
        for i in range(self.beta):
            print "ITERATION %d" % i
            rows, rows_to_revs = self._construct_matching_mat()
            print "MATRIX CONSTRUCTED"
            self._solve_assignment_and_update(rows, rows_to_revs)
        return self.curr_assignment

    def score_assignment(self):
        total = 0.0
        for pap in range(np.size(self.pap_mat, axis=0)):
            assigned_revs = np.nonzero(self.curr_assignment[:,pap])[0]
            total += self.group_score(assigned_revs, pap)
        return total


if __name__ == "__main__":
    alpha = 2
    beta = 1
    rev_mat = np.array([[0.15, 0.35, 0.5],
                        [0.15, 0.5, 0.35],
                        [0.5, 0.15, 0.35]])
    pap_mat = np.array([[0.15, 0.5, 0.35],
                        [0.5, 0.15, 0.35],
                        [0.15, 0.35, 0.5]])
    wgrap = WGRAP(rev_mat, pap_mat, alpha, beta)

    rows, rows_to_revs = wgrap._construct_matching_mat()
    wgrap._solve_assignment_and_update(rows, rows_to_revs, show=True)
    print wgrap.curr_assignment
    rows, rows_to_revs = wgrap._construct_matching_mat()
    wgrap._solve_assignment_and_update(rows, rows_to_revs, show=True)
    print wgrap.curr_assignment
    wgrap.refine()
    print wgrap.curr_assignment
    rows, rows_to_revs = wgrap._construct_matching_mat(post_refine=True)
    wgrap._solve_assignment_and_update(rows, rows_to_revs, show=True)
    print wgrap.curr_assignment

    print "CORRUPTING THE ASSIGNMENT MATRIX"
    wgrap.curr_assignment[0,0] = 1.0
    wgrap.curr_assignment[1,1] = 1.0
    wgrap.curr_assignment[2,2] = 1.0
    wgrap.curr_assignment[0,2] = 0.0
    wgrap.curr_assignment[1,0] = 0.0
    wgrap.curr_assignment[2,1] = 0.0

    print wgrap.curr_assignment
    for i in range(10):
        wgrap.refine(show=True)
        print wgrap.curr_assignment
        rows, rows_to_revs = wgrap._construct_matching_mat(post_refine=True)
        wgrap._solve_assignment_and_update(rows, rows_to_revs, show=False)
        print wgrap.curr_assignment
