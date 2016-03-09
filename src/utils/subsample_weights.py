import argparse
import os

import numpy as np

from matplotlib import pyplot as plt
from weights import showWeights

def naive_subsample(mat, nrows, ncols):
    rows = np.random.choice(np.size(mat,axis=0), nrows, False)
    cols = np.random.choice(np.size(mat,axis=1), ncols, False)
    assert np.size(mat[rows,:][:,cols], axis=0) == nrows
    assert np.size(mat[rows,:][:,cols], axis=1) == ncols
    return mat[rows,:][:,cols]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Subsample an affinity matrix.')
    parser.add_argument('weight_file', type=str, help='the file containing the affinity matrix')
    parser.add_argument('nrev', type=int, help='# of reviewers (rows)')
    parser.add_argument('npap', type=int, help='# of papers (cols)')
    parser.add_argument('--plot', action='store_true')

    args = parser.parse_args()

    nrows = args.nrev
    ncols = args.npap
    weight_file = args.weight_file
    weight_file_base = weight_file[:weight_file.rfind('/')]
    sub_sample_file = '%s/weightsample-%s-%s.txt' % (weight_file_base, nrows, ncols)
    plot_file = '%s/weightsample-%s-%s.png' % (weight_file_base, nrows, ncols)

    weight_mat = np.genfromtxt(weight_file)
    sub_sample = naive_subsample(weight_mat, nrows, ncols)

    plt = showWeights(sub_sample)
    plt.savefig(plot_file)
    if args.plot:
        plt.show()

    np.savetxt(sub_sample_file, sub_sample)
