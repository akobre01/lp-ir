import argparse
import numpy as np
import os

from matplotlib import pyplot as plt

def read_files_in_dir(directory):
    data = []
    for filename in os.listdir(directory):
        data.append(np.genfromtxt(directory + "/" + filename, delimiter=','))
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

    mean_affs = np.mean(affs, 0)

    plt.figure(1)
    plt.subplot(111)
    plt.hist(mean_affs, bins=args.bins)
    plt.xlabel(args.xlabel)
    plt.ylabel(args.ylabel)
    plt.title(args.title)
    plt.xlim(0,5)
    plt.show()
