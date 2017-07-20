import argparse
import numpy as np
import os

from matplotlib import pyplot as plt
from .plotting_style import MODEL_TO_COLOR, BORDER_COLOR, LABEL_COLOR


def read_files_with_prefix(d, pre):
    """Read the files in directory d with prefix pre."""
    return [f for f in os.listdir(d) if f.startswith(pre)]


if __name__ == "__main__":
    """A script that reads from a results dir and generates a score histograms.

    Make a histogram for the paper assignment score .
    """
    parser = argparse.ArgumentParser(description='Plot survival of models.')
    parser.add_argument('input', type=str,
                        help='The path to the directory that contains results.')
    parser.add_argument('weights', type=str,
                        help='The path to the weights matrix used for results.')
    parser.add_argument('coverage', type=float,
                        help='The maximum paper assignment score.')
    args = parser.parse_args()

    weights = np.load(args.weights)
    max_score = args.coverage
    bins = np.linspace(0, max_score, num=50)
    y_max = 0

    assignments = np.load(os.path.join(args.input, 'assignment.npy'))
    scores = np.sum(assignments * weights, axis=0)
    n, _, _ = plt.hist(scores, bins=bins)
    max_height = max(n)
    y_max = max(y_max, max_height)

    fig, ax = plt.subplots(1, 1)
    assert np.all(weights <= 1.0)
    _, _, patches = ax.hist(scores, bins=bins)
    for patch in patches:
        patch.set_edgecolor('white')
        ax.set_ylabel('# of Assignments')
        ax.set_xlabel('Paper Assignment Score')
        ax.set_title('Assignment Affinities')
        ax.set_xlim(0, max_score)
        ax.set_ylim(0, max_height + 10)

    # Change borders, tick colors, etc.
    ax.spines['bottom'].set_color(BORDER_COLOR)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom='on', top='off',
                   color=BORDER_COLOR)
    ax.tick_params(axis='y', which='both', left='on', right='off',
                   color=BORDER_COLOR)
    ax.xaxis.label.set_color(LABEL_COLOR)
    ax.yaxis.label.set_color(LABEL_COLOR)
    for l in ax.xaxis.get_ticklabels():
        l.set_color(LABEL_COLOR)
    for l in ax.yaxis.get_ticklabels():
        l.set_color(LABEL_COLOR)
    outfile = os.path.join(args.input, 'affhist.png')
    fig.savefig(outfile)