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
    parser.add_argument('-d2','--uptight_dirs', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('-d3','--complete_relax_dirs', nargs='+', help='<Required> Set flag', required=True)

    args = parser.parse_args()

    relaxed_affs = []
    uptight_affs = []
    complete_relax_affs = []
    for d in args.relaxed_dirs:
        data = read_files_in_dir(d)
        relaxed_affs.append(data)
    for d in args.uptight_dirs:
        data = read_files_in_dir(d)
        uptight_affs.append(data)
    for d in args.complete_relax_dirs:
        data = read_files_in_dir(d)
        complete_relax_affs.append(data)

    sum_relaxed = np.sum(np.array(relaxed_affs), 0)
    sum_uptight = np.sum(np.array(uptight_affs), 0)
    sum_complete_relax = np.sum(np.array(complete_relax_affs), 0)

    relaxed_hist, relaxed_bs = np.histogram(sum_relaxed.reshape(-1), bins=args.bins)
    uptight_hist, uptight_bs = np.histogram(sum_uptight.reshape(-1), relaxed_bs)
    complete_relax_hist, complete_relax_bs = np.histogram(sum_uptight.reshape(-1), relaxed_bs)

#    relaxed_cdf = np.cumsum(relaxed_hist) / float(np.sum(relaxed_hist))
#    uptight_cdf = np.cumsum(uptight_hist) / float(np.sum(uptight_hist))

#    relaxed_cdf = np.cumsum(relaxed_hist[::-1]) / float(np.sum(relaxed_hist))
#    uptight_cdf = np.cumsum(uptight_hist[::-1]) / float(np.sum(uptight_hist))

    relaxed_cdf = 1.0 - (np.cumsum(relaxed_hist) / float(np.sum(relaxed_hist)))
    uptight_cdf = 1.0 - (np.cumsum(uptight_hist) / float(np.sum(uptight_hist)))
    complete_relax_cdf = 1.0 - (np.cumsum(complete_relax_hist) / float(np.sum(complete_relax_hist)))

    plt.clf()
    plt.figure(1)
    plt.subplot(211)
    plt.hist(sum_relaxed.reshape(-1), relaxed_bs, alpha=0.5, label='relaxed')
    plt.hist(sum_uptight.reshape(-1), uptight_bs, alpha=0.5, label='up-tight')
    plt.hist(sum_complete_relax.reshape(-1), uptight_bs, alpha=0.5, label='complete-relax')
    plt.ylabel(args.ylabel)
    plt.title(args.title)
    plt.legend(loc='upper right')
    plt.xlim(0.5,3)

    plt.subplot(212)
    plt.plot(relaxed_bs[:-1], relaxed_cdf, alpha=0.5, label='relaxed')
    plt.plot(uptight_bs[:-1], uptight_cdf, alpha=0.5, label='uptight')
    plt.plot(complete_relax_bs[:-1], complete_relax_cdf, alpha=0.5, label='complete-relax')
    plt.xlabel(args.xlabel)
    plt.ylabel("Fraction of Papers")
    plt.legend(loc='upper right')

    plt.show()
