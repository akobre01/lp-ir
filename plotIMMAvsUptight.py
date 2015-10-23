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
    return np.array(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input directories.')
    parser.add_argument('title', type=str, help='Title of the plot')
    parser.add_argument('xlabel', type=str, help='label for the x-axis')
    parser.add_argument('ylabel', type=str, help='label for the y-axis')
    parser.add_argument('bins', type=int, help='the number of bins to plot')
    parser.add_argument('-d1','--relaxed_dirs', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('-d2','--uptight_dirs', nargs='+', help='<Required> Set flag', required=True)

    args = parser.parse_args()

    relaxed_affs = []
    uptight_affs = []
    for d in args.relaxed_dirs:
        data = read_files_in_dir(d)
        relaxed_affs.append(np.array(data))
    for d in args.uptight_dirs:
        data = read_files_in_dir(d)
        uptight_affs.append(np.array(data))


    sum_relaxed = np.sum(np.array(relaxed_affs), 0)
    sum_uptight = np.sum(np.array(uptight_affs), 0)

    plt.clf()
    plt.figure(1)
    plt.subplot(111)
    plt.hist(sum_relaxed.reshape(-1), bins=args.bins, alpha=0.5, label='relaxed')
    plt.hist(sum_uptight.reshape(-1), bins=args.bins, alpha=0.5, label='up-tight')
    plt.xlabel(args.xlabel)
    plt.ylabel(args.ylabel)
    plt.title(args.title)
    plt.legend(loc='upper right')
    plt.xlim(0,5)
    plt.show()
