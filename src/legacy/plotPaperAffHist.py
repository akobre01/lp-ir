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
    parser.add_argument('-i','--input_dirs', nargs='+', help='<Required> Set flag', required=True)

    args = parser.parse_args()

    affs = []
    for d in args.input_dirs:
        data = read_files_in_dir(d)
        affs.append(np.array(data))
    sum_affs = np.sum(np.array(affs), 0)

    plt.clf()
    plt.figure(1)
    plt.subplot(111)
    plt.hist(sum_affs.reshape(-1), bins=args.bins)
    plt.xlabel(args.xlabel)
    plt.ylabel(args.ylabel)
    plt.title(args.title)
    plt.xlim(0,5)
    plt.show()