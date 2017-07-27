import matplotlib as mlp
mlp.use('Agg')
import matplotlib.pyplot as plt

import argparse
import glob
import numpy as np
import os

from .plotting_style import MODEL_TO_COLOR, BORDER_COLOR, LABEL_COLOR


def read_files_with_prefix(d, pre):
    """Read the files in directory d with prefix pre."""
    return [f for f in os.listdir(d) if f.startswith(pre)]


if __name__ == '__main__':
    """A script that reads from a results dir and generates a survival plot.

    The survival plot looks at the paper assignment score for each method and
    computes the fraction of papers with score greater than x for x in the range
    [0, max_score].
    """
    parser = argparse.ArgumentParser(description='Plot survival of models.')
    parser.add_argument('input', type=str,
                        help='The path to the directory that contains results.')
    parser.add_argument('weights', type=str,
                        help='The path to the weights matrix used for results.')
    parser.add_argument('-m', '--max_score', type=float,
                        help='The maximum paper assignment score.')
    args = parser.parse_args()

    weights = np.load(args.weights)
    assert np.all(weights <= 1.0)

    filelist = [f for f in glob.glob(args.input + '/**/assignment.npy',
                                     recursive=True)]

    model_to_best = {}
    for f in filelist:
        file_parts = f.split('/')
        model = file_parts[-3]
        params = file_parts[-2].split('-')
        ms = params[0]
        ms_val = ms.split('=')[1]
        if model not in model_to_best or model_to_best[model][0] <= ms_val:
            model_to_best[model] = (ms_val, f)

    fig, ax = plt.subplots(1, 1)
    max_score = args.max_score or 3
    x_vals = np.linspace(0, max_score, num=100)
    for ms, f in model_to_best.values():
        assignments = np.load(f)
        scores = np.sum(assignments * weights, axis=0)
        survivors = []
        file_parts = f.split('/')
        model = file_parts[-3]
        run_name = '%s-%s' % (file_parts[-3], file_parts[-2])
        for score_threshold in x_vals:
            survivors.append(len([x for x in scores if x >= score_threshold]) /
                             np.size(scores))
        ax.plot(x_vals, survivors, label=run_name, color=MODEL_TO_COLOR[model])
    ax.set_ylabel('Fraction Survivors')
    ax.set_xlabel('Paper Assignment Score')
    ax.set_title('Survival')
    leg = ax.legend(loc='upper right', frameon=False)
    ax.set_xlim(0, max_score)
    ax.set_ylim(0, 1.2)

    # Change borders, tick colors, etc.
    ax.spines['bottom'].set_color(BORDER_COLOR)
    ax.spines['left'].set_color(BORDER_COLOR)
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
    for l in leg.get_texts():
        l.set_color(LABEL_COLOR)
    fig.savefig('%s/survival.png' % args.input)
