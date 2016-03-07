import argparse
import numpy as np
import os

from collections import defaultdict
from matplotlib import pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for plotting.')
    parser.add_argument('train_dir', type=str, help='location of training files')

    args = parser.parse_args()

    train_dir = args.train_dir
    ds = os.listdir(train_dir)
    size_and_bp_to_mkspn = defaultdict(dict)
    for d in ds:
        splits = d.split('-')
        revs,paps,bp1,bp2,_ = float(splits[0]), float(splits[1]), float(splits[2]), float(splits[3]), splits[4]
        fs = os.listdir('%s/%s' % (train_dir, d))
        mx_threshs = filter(lambda x: x.startswith('mxthresh-MakespanMatcher'), fs)

        # find all of the parameter settings for matrix
        for fname in mx_threshs:
            splits = fname.split('-')
            f = open('%s/%s/%s' % (train_dir, d, fname), 'r')
            mkspn = float(f.readline().strip())
            f.close()
            size_and_bp_to_mkspn[revs][bp1] = mkspn


    print size_and_bp_to_mkspn
