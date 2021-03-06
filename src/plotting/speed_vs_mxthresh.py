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
        mx_thresh = filter(lambda x: x.startswith('bb-weights-seqmkspn'), fs)

        mkspns = []
        subsamples = []
        times = []
        if len(mx_thresh) > 0:
            print('%s/%s/%s' % (train_dir, d, mx_thresh[0]))
            full_f = open('%s/%s/%s' % (train_dir, d, mx_thresh[0]), 'r')
            target_line = full_f.readlines()[-2].strip()
            splits = target_line.split('\t')
            mx_mkspn = float(splits[0].strip())
            mx_time = float(splits[-1].strip()[:-1])
            full_f.close()
            mkspns.append(mx_mkspn)
            times.append(mx_time)
            subsamples.append(revs)

        mx_threshs = filter(lambda x: x.startswith('bb-weightsample'), fs)

        # find all of the parameter settings for matrix
        for fname in mx_threshs:
            splits = fname.split('-')
            method,_,nrev,npap,_,alpha,beta = splits[0], splits[1], int(splits[2]), int(splits[3]), splits[4], int(splits[5]), int(splits[6].split('.')[0])
            f = open('%s/%s/%s' % (train_dir, d, fname), 'r')
            print '%s/%s/%s' % (train_dir, d, fname)
            target_line = f.readlines()[-2]
            splits = target_line.split('\t')
            mx_mkspn = float(splits[0].strip())
            mx_time = float(splits[-1].strip()[:-1])
            mkspns.append(mx_mkspn)
            subsamples.append(nrev)
            times.append(mx_time)
            f.close()
            

        plt.clf()
        plt.subplot(1,2,1)
        plt.scatter(subsamples, mkspns)
        plt.xlabel('sample size')
        plt.ylabel('max makespan')
        plt.title('Subsample vs. Max Mkspn')

        plt.subplot(1,2,2)
        plt.scatter(subsamples, times)        
        plt.xlabel('sample size')
        plt.ylabel('time (s)')
        plt.title('Subsample vs. Time to Solve')        
        plt.savefig('subsampled-mkspan-%s-%s-%s-%s-%s.png' % (nrev,revs,paps,bp1,bp2))

    # colors = iter(cm.rainbow(np.linspace(0, 1, len(bp_to_size_and_mkspn.keys()))))
    # scatters = []
    # keys = []
    # plt.clf()
    # plt.subplot(1,1,1)
    # print bp_to_size_and_mkspn
    # for bp, size_mkspn in bp_to_size_and_mkspn.iteritems():
    #     xs = map(lambda (x,y): x, size_mkspn)
    #     ys = map(lambda (x,y): y, size_mkspn)
    #     scatters.append(plt.scatter(xs,ys, color=next(colors), label=size))
    #     keys.append(bp)
    # plt.legend(tuple(scatters), tuple(map(lambda x: str(x), keys)), loc='lower right')
    # plt.xlabel('size')
    # plt.ylabel('mkspn')
    # plt.ylabel('largest feasible makespan')
    # plt.savefig('size_vs_mkspn.png')
