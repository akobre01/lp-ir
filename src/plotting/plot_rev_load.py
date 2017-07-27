import matplotlib as mlp
mlp.use('Agg')
import matplotlib.pyplot as plt

import argparse
import numpy as np
import os

from .plotting_style import BORDER_COLOR, LABEL_COLOR


def read_files_with_prefix(d, pre):
    """Read the files in directory d with prefix pre."""
    return [f for f in os.listdir(d) if f.startswith(pre)]


if __name__ == "__main__":
    """A script that reads from a results dir and generates reviewer load hist.

    Make a histogram for the paper assignment score .
    """
    parser = argparse.ArgumentParser(description='Plot reviewer loads.')
    parser.add_argument('input', type=str,
                        help='The path to the directory that contains results.')
    args = parser.parse_args()

    assignments = np.load(os.path.join(args.input, 'assignment.npy'))
    rev_load = np.sum(assignments, axis=1)
    max_revs = np.max(rev_load)
    n, _, _ = plt.hist(rev_load, bins=max_revs + 1)
    y_max = max(n)

    fig, ax = plt.subplots(1, 1)
    _, _, patches = ax.hist(rev_load, bins=max_revs + 1)
    for patch in patches:
        patch.set_edgecolor('white')
        ax.set_ylabel('# of Reviewers')
        ax.set_xlabel('Load (# of Papers)')
        ax.set_title('Reviewer Load')
        ax.set_ylim(0, y_max + 10)

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
    outfile = os.path.join(args.input, 'revload.png')
    fig.savefig(outfile)
