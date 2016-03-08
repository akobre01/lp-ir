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
    parser.add_argument('-i','--input_dirs', nargs='+', help='<Required> Set flag', required=True)

    args = parser.parse_args()

    means = []
    std = []
    for d in args.input_dirs:
        data = read_files_in_dir(d)
        means.append(np.mean(np.array(data), 0))
        std.append(np.std(np.array(data), 0))

    plt.figure(1)
    plt.subplot(111)

    for i in range(len(means)):
        plt.errorbar(range(len(means[i])), means[i], yerr=std[i])

    plt.title(args.title)
    plt.xlabel(args.xlabel)
    plt.ylabel(args.ylabel)
    plt.show()
