import matplotlib as mlp
mlp.use('Agg')
import matplotlib.pyplot as plt

import argparse
import numpy as np
import os

from plotting.plotting_style import MODEL_TO_COLOR, BORDER_COLOR, LABEL_COLOR

from utils.Config import Config


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
    parser.add_argument('config_dir', type=str, help='path to exp_out config')
    args = parser.parse_args()

    config = Config(os.path.join(args.config_dir, 'config.json'))
    scores = np.load(config.score_f)

    assignment = np.load(os.path.join(args.config_dir, 'results',
                                      'assignment.npy'))

    # model_to_best = {}
    # for f in filelist:
    #     file_parts = f.split('/')
    #     model = file_parts[-3]
    #     params = file_parts[-2].split('-')
    #     ms = params[0]
    #     ms_val = ms.split('=')[1]
    #     #if model not in model_to_best or model_to_best[model][0] <= ms_val:
    #     model_to_best[ms_val] = (ms_val, f)

    match_scores = np.sum(assignment * scores, axis=0)
    sorted_scores = sorted(match_scores)
    num_papers = np.size(sorted_scores)

    fig, ax = plt.subplots(1, 1)
    ax.boxplot(match_scores)
    ax.set_title('Resid, Makespan=%s' % config.makespan)
    ax.set_ylabel('Paper Assignment Score')
    ax.set_xlabel('Quantile')
    leg = ax.legend(loc='upper right', frameon=False)

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
    fig.savefig('/tmp/box.png')
