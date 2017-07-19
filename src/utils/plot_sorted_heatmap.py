import argparse
import numpy as np
import matplotlib.pyplot as plt
import os


def sorted_heatmap(weights):
    """Create a sorted heatmap.

    Plot a matrix such that the biggest row/col values are in the upper left
    of the heatmap.

    Args:
      weights - a 2d numpy array of floats

    Returns:
      A plot that can be saved to a file via plt.savefig('file')
    """
    weights = weights.reshape(weights.shape[:2])
    row_order = np.array(sorted(weights, key=lambda row: np.sum(row)))
    col_order = np.array(sorted(row_order.T, key=lambda row: -np.sum(row))).T
    cMap = plt.get_cmap("Blues")

    plt.subplot(1,1,1)
    heatmap = plt.pcolor(col_order, cmap=cMap)
    plt.colorbar(heatmap)
    plt.title("Title")
    plt.xlabel("Xlabel")
    plt.ylabel("Ylabel")
    return plt


if __name__ == '__main__':
    """Plot a heatmap of reviewer-paper scores from file."""
    parser = argparse.ArgumentParser(description='Plot heatmap of scores.')
    parser.add_argument('weights', type=str,
                        help='The path to the weights matrix used for results.')
    parser.add_argument('output', type=str,
                        help='Where to save the figure.')
    args = parser.parse_args()

    weights_f = args.weights
    ws = np.load(weights_f)
    plt = sorted_heatmap(ws[:200, :200])
    plt.savefig(os.path.join(args.output, 'cvpr.png'))
