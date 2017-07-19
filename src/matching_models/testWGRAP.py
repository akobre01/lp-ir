import sys
import numpy as np
from WGRAP import WGRAP
import time

if __name__ == "__main__":
    rev_mat_file = "/Users/akobren/software/repos/git/lp-ir/data/train/kou_et_al/kou_rev_mat_dm08.npy"
    pap_mat_file = "/Users/akobren/software/repos/git/lp-ir/data/train/kou_et_al/kou_pap_mat_dm08.npy"
    beta = 5
    rev_mat = np.load(rev_mat_file)
    pap_mat = np.load(pap_mat_file)
    num_rev = np.size(rev_mat, axis=0)
    num_pap = np.size(pap_mat, axis=0)
    alpha = np.ceil(num_pap * beta / num_rev)
    out_file = "../../data/train/kou_et_al/wgrap-dm08-%d-%d-assign" % (alpha, beta)

    print "REV MAT SHAPE: %s" % str(rev_mat.shape)
    print "PAP MAT SHAPE: %s" % str(pap_mat.shape)
    wgrap = WGRAP(rev_mat, pap_mat, alpha, beta)

    start = time.time()
    wgrap.solve()
    print "SOLVED IN: %s SECONDS" % (time.time() - start)
    print "SCORE: %f" % wgrap.score_assignment()
    np.save(out_file, wgrap.curr_assignment)

    for i in range(10):
        start = time.time()
        wgrap.refine()
        rows, rows_to_revs = wgrap._construct_matching_mat(post_refine=True)
        wgrap._solve_assignment_and_update(rows, rows_to_revs, show=False)
        print "REFINED IN: %s SECONDS" % (time.time() - start)
        print "SCORE: %f" % wgrap.score_assignment()
        np.save("%s-refine-%d" % (out_file, i), wgrap.curr_assignment)
