import argparse
import numpy as np
import os
import sys
import time

class MatFeatExtract:
    def __init__(self, weights, alpha, beta, mx_thresh):
        self.weights = weights
        self.n_rev = np.size(self.weights, axis=0)
        self.n_pap = np.size(self.weights, axis=1)
        self.alpha = alpha
        self.beta = beta
        self.mx_thresh = mx_thresh

    def sum(self):
        return np.sum(self.weights)

    def moment_1(self):
        return np.mean(self.weights)

    def central_moment(self, num):
        mean = np.mean(weights)
        mean_adj = self.weights - mean
        return np.sum(mean_adj ** num) / (self.n_rev * self.n_pap)

    def extract(self):
        return "\t".join(['%f' % self.alpha,
                          '%f' % self.beta,
                          '%f' % self.n_rev,
                          '%f' % self.n_pap,
                          '%f' % self.sum(),
                          '%f' % self.moment_1(),
                          '%f' % self.central_moment(2),
                          '%f' % self.central_moment(3),
                          '%f' % self.central_moment(4),
                          '%f' % self.mx_thresh])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for feature extraction.')
    parser.add_argument('train_dir', type=str, help='location of training files')

    args = parser.parse_args()

    train_dir = args.train_dir
    weights_file = "%s/weights.txt" % args.train_dir
    weights = np.genfromtxt(weights_file)

    fs = os.listdir(train_dir)
    mx_threshs = filter(lambda x: x.startswith('mxthresh-MakespanMatcher'), fs)
    files_and_feats = []

    # find all of the parameter settings for matrix
    for fname in mx_threshs:
        splits = fname.split('-')
        _,_,_,alpha,_,beta = splits[0], splits[1], splits[2], float(splits[3]), splits[4], float(splits[5])
        f = open('%s/%s' % (train_dir, fname), 'r')
        mkspn = float(f.readline().strip())
        f.close()
        files_and_feats.append((fname, alpha, beta, mkspn))

    # write out features for matrix
    for (fname, alpha, beta, mkspn) in files_and_feats:
        mfe = MatFeatExtract(weights, alpha, beta, mkspn)
        f = open('%s/feats-%s' % (train_dir, fname), 'w')
        f.write('%s\n' % mfe.extract())
        f.close()
