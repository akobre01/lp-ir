import matplotlib as mlp
mlp.use('Agg')
import matplotlib.pyplot as plt

import argparse
import glob
import numpy as np
import os

from matplotlib import pyplot as plt
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

    fig, ax = plt.subplots(1, 1)
    max_score = args.max_score or 3
    x_vals = np.linspace(0, max_score, num=100)
    for f in filelist:
        assignments = np.load(f)
        scores = np.sum(assignments * weights, axis=0)
        survivors = []
        file_parts = f.split('/')
        model = '%s-%s' % (file_parts[-3], file_parts[-2])
        for score_threshold in x_vals:
            survivors.append(len([x for x in scores if x >= score_threshold]) /
                             np.size(scores))
        ax.plot(x_vals, survivors, label=model, color=MODEL_TO_COLOR[model])
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

    # assignment_files = read_files_with_prefix(args.input, 'assignment')
    # models = list(set([f.split('-')[1] for f in assignment_files]))
    #
    # # The next line is gross. We want to get a dictionary of model to assignment
    # # file but for each model we might have multiple assignment files so we have
    # # to find the best one. Based on the way we know that files are named, we
    # # can figure this out py parsing the beginning and end of the file names.
    # model_to_assignment = {
    #     model: sorted([f for f in assignment_files
    #                    if f.startswith('assignment-%s' % model)],
    #                   key=lambda x: float(x.split('-')[-1].split('.')[0]))[-1]
    #     for model in models
    #     }
    #
    # weights = np.load(args.weights)
    #
    # fig, ax = plt.subplots(1, 1)
    # max_score = args.max_score
    # x_vals = np.linspace(0, max_score, num=100)
    # for model, assignment_f in model_to_assignment.items():
    #     assert np.all(weights <= 1.0)
    #     assignments = np.load('%s/%s' % (args.input, assignment_f))
    #     scores = np.sum(assignments * weights, axis=0)
    #     survivors = []
    #     for score_threshold in x_vals:
    #         survivors.append(len([x for x in scores if x >= score_threshold]) /
    #                          np.size(scores))
    #     ax.plot(x_vals, survivors, label=model, color=MODEL_TO_COLOR[model])
    # ax.set_ylabel('Fraction Survivors')
    # ax.set_xlabel('Paper Assignment Score')
    # ax.set_title('Survival')
    # leg = ax.legend(loc='upper right', frameon=False)
    # ax.set_xlim(0, max_score)
    # ax.set_ylim(0, 1.2)
    #
    # # Change borders, tick colors, etc.
    # ax.spines['bottom'].set_color(BORDER_COLOR)
    # ax.spines['left'].set_color(BORDER_COLOR)
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # ax.tick_params(axis='x', which='both', bottom='on', top='off',
    #                color=BORDER_COLOR)
    # ax.tick_params(axis='y', which='both', left='on', right='off',
    #                color=BORDER_COLOR)
    # ax.xaxis.label.set_color(LABEL_COLOR)
    # ax.yaxis.label.set_color(LABEL_COLOR)
    # for l in ax.xaxis.get_ticklabels():
    #     l.set_color(LABEL_COLOR)
    # for l in ax.yaxis.get_ticklabels():
    #     l.set_color(LABEL_COLOR)
    # for l in leg.get_texts():
    #     l.set_color(LABEL_COLOR)
    # fig.savefig('%s/survival.png' % args.input)
