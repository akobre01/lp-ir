import argparse
import numpy as np
import os

from matplotlib import pyplot as plt

def read_files_in_dir(directory):
    data = []
    count = 0
    for filename in os.listdir(directory):
        if count >= 5:
            continue
        data.append(np.genfromtxt(directory + "/" + filename, delimiter=','))
        count += 1
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input directories.')
    parser.add_argument('title', type=str, help='Title of the plot')
    parser.add_argument('xlabel', type=str, help='label for the x-axis')
    parser.add_argument('ylabel', type=str, help='label for the y-axis')
    parser.add_argument('bins', type=int, help='the number of bins to plot')
    parser.add_argument('-d1','--relaxed_dirs', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('-d2','--bb_dirs', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('-d3','--imma_da_dirs', nargs='+', help='<Required> Set flag', required=True)

    args = parser.parse_args()

    relaxed_affs = []
    bb_affs = []
    imma_da_affs = []
    for d in args.relaxed_dirs:
        data = read_files_in_dir(d)
        relaxed_affs.append(data)
    for d in args.bb_dirs:
        data = read_files_in_dir(d)
        bb_affs.append(data)
    for d in args.imma_da_dirs:
        data = read_files_in_dir(d)
        imma_da_affs.append(data)

    sum_relaxed = np.sum(np.array(relaxed_affs), 0)
    sum_bb = np.sum(np.array(bb_affs), 0)
    sum_imma_da = np.sum(np.array(imma_da_affs), 0)

    relaxed_hist, relaxed_bs = np.histogram(sum_relaxed.reshape(-1), bins=args.bins)
    bb_hist, bb_bs = np.histogram(sum_bb.reshape(-1), relaxed_bs)
    imma_da_hist, imma_da_bs = np.histogram(sum_imma_da.reshape(-1), relaxed_bs)

#    relaxed_cdf = np.cumsum(relaxed_hist) / float(np.sum(relaxed_hist))
#    bb_cdf = np.cumsum(bb_hist) / float(np.sum(bb_hist))

#    relaxed_cdf = np.cumsum(relaxed_hist[::-1]) / float(np.sum(relaxed_hist))
#    bb_cdf = np.cumsum(bb_hist[::-1]) / float(np.sum(bb_hist))

    relaxed_cdf = 1.0 - (np.cumsum(relaxed_hist) / float(np.sum(relaxed_hist)))
    bb_cdf = 1.0 - (np.cumsum(bb_hist) / float(np.sum(bb_hist)))
    imma_da_cdf = 1.0 - (np.cumsum(imma_da_hist) / float(np.sum(imma_da_hist)))

    plt.clf()
    plt.figure(1)
    plt.subplot(111)
    plt.hist(sum_relaxed.reshape(-1), relaxed_bs, alpha=0.4, label='IMMA')
    plt.hist(sum_bb.reshape(-1), bb_bs, alpha=0.4, label='BB')
    plt.hist(sum_imma_da.reshape(-1), bb_bs, alpha=0.4, label='IMMA-DA')
    plt.ylabel(args.ylabel)
    plt.xlabel(args.xlabel)
    plt.title(args.title)
    plt.legend(loc='upper right')
    plt.xlim(0.5,3)
    plt.show()

    plt.clf()
    plt.figure(1)
    plt.subplot(111)
    plt.plot(relaxed_bs[:-1], relaxed_cdf, alpha=0.4, label='IMMA')
    plt.plot(bb_bs[:-1], bb_cdf, alpha=0.4, label='BB')
    plt.plot(imma_da_bs[:-1], imma_da_cdf, alpha=0.4, label='IMMA-DA')
    plt.title('Paper Score Survival')
    plt.xlabel(args.xlabel)
    plt.ylabel("Fraction of Papers")
    plt.legend(loc='upper right')
    plt.xlim(0.5,3)
    plt.show()
