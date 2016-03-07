import argparse
import numpy as np
import os

from collections import defaultdict
#import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.cm as cm

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

    plt.clf()
    colors = iter(cm.rainbow(np.linspace(0, 1, len(size_to_bp_and_mkspn.keys()))))
    scatters = []
    keys = []
    xs = []
    ys = []
    for size, bp_mkspns in size_to_bp_and_mkspn.iteritems():
        xs = map(lambda (x,y): x, bp_mkspns)
        ys = map(lambda (x,y): y, bp_mkspns)
        scatters.append(plt.scatter(xs,ys, color=next(colors), label=size))
        keys.append(size)
    plt.legend(tuple(scatters), tuple(map(lambda x: str(x), keys)), loc='lower right')
    plt.xlabel('bp1')
    plt.ylabel('mkspn')
    plt.title('largest feasible makespan')
    plt.savefig('bp_vs_mkspn.png')

    colors = iter(cm.rainbow(np.linspace(0, 1, len(bp_to_size_and_mkspn.keys()))))
    scatters = []
    keys = []
    plt.subplot(1,1,1)
    print bp_to_size_and_mkspn
    for bp, size_mkspn in bp_to_size_and_mkspn.iteritems():
        xs = map(lambda (x,y): x, size_mkspn)
        ys = map(lambda (x,y): y, size_mkspn)
        scatters.append(plt.scatter(xs,ys, color=next(colors), label=size))
        keys.append(bp)
    plt.legend(tuple(scatters), tuple(map(lambda x: str(x), keys)), loc='lower right')
    plt.xlabel('size')
    plt.ylabel('mkspn')
    plt.ylabel('largest feasible makespan')
    plt.savefig('size_vs_mkspn.png')

