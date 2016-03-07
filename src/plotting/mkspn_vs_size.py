import argparse
import numpy as np
import os

from collections import defaultdict
#import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for plotting.')
    parser.add_argument('train_dir', type=str, help='location of training files')

    args = parser.parse_args()

    train_dir = args.train_dir
    ds = os.listdir(train_dir)
    size_to_bp_and_mkspn = defaultdict(list)
    bp_to_size_and_mkspn = defaultdict(list)
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
            size_to_bp_and_mkspn[revs].append((bp1, mkspn))
            bp_to_size_and_mkspn[bp1].append((revs, mkspn))


    mkspn_and_bp = []
    plt.subplot(1,1,1)
    for size, bp_mkspns in size_to_bp_and_mkspn.iteritems():
        xs = map(lambda (x,y): x, bp_mkspns)
        ys = map(lambda (x,y): y, bp_mkspns)
        plt.plot(xs,ys, label=size)
    plt.savefig('test.png')
