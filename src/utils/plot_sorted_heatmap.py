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

    fig1 = plt.figure(1)
    fig1.add_subplot(1, 1, 1)
    heatmap = plt.pcolor(col_order[:200, :200], cmap=cMap)
    plt.colorbar(heatmap)
    plt.title("Reviewer-Paper Affinities")
    plt.xlabel("Paper")
    plt.ylabel("Reviewer")

    fig2 = plt.figure(2)
    fig2.add_subplot(1, 1, 1)
    heatmap = plt.pcolor(col_order[-200:, -200:], cmap=cMap)
    plt.colorbar(heatmap)
    plt.title("Reviewer-Paper Affinities")
    plt.xlabel("Paper")
    plt.ylabel("Reviewer")
    return fig1, fig2


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
    f1, f2 = sorted_heatmap(ws)
    f1.savefig(os.path.join(args.output, 'cvpr-worst.png'))
    f2.savefig(os.path.join(args.output, 'cvpr-best.png'))
