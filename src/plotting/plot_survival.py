import argparse
import numpy as np
import os

from matplotlib import pyplot as plt


def read_files_with_prefix(d, pre):
    """Read the files in directory d with prefix pre."""
    return [f for f in os.listdir(d) if f.startswith(pre)]


if __name__ == "__main__":
    """A script that reads from a results dir and generates a survival plot.

    The survival plot looks at the paper assignment score for each method and
    computes the fraction of papers with score greater than x for x in the range
    [0, max_score].
    """
    parser = argparse.ArgumentParser(description='Plot survival of models.')
    parser.add_argument('-i', '--input', type=str,
                        help='The path to the directory that contains results.')
    parser.add_argument('-w', '--weights', type=str,
                        help='The path to the weights matrix used for results.')
    parser.add_argument('-m', '--max_score', type=float,
                        help='The maximum paper assignment score.')
    args = parser.parse_args()

    assignment_files = read_files_with_prefix(args.input, 'assignment')
    models = list(set([f.split('-')[1] for f in assignment_files]))

    # The next line is gross. We want to get a dictionary of model to assignment
    # file but for each model we might have multiple assignment files so we have
    # to find the best one. Based on the way we know that files are named, we
    # can figure this out py parsing the beginning and end of the file names.
    model_to_assignment = {
        model: sorted([f for f in assignment_files
                       if f.startswith('assignment-%s' % model)],
                      key=lambda x: float(x.split('-')[-1].split('.')[0]))[-1]
        for model in models
        }

    weights = np.load(args.weights)

    fig, ax = plt.subplots(1, 1)
    max_score = args.max_score
    x_vals = np.linspace(0, max_score, num=100)
    for model, assignment_f in model_to_assignment.items():
        assert np.all(weights <= 1.0)
        assignments = np.load('%s/%s' % (args.input, assignment_f))
        scores = np.sum(assignments * weights, axis=0)
        survivors = []
        for score_threshold in x_vals:
            survivors.append(len([x for x in scores if x >= score_threshold]) /
                             np.size(scores))
        ax.plot(x_vals, survivors, label=model)
    ax.set_ylabel('Fraction Survivors')
    ax.set_xlabel('Paper Assignment Score')
    ax.set_title('Survival')
    leg = ax.legend(loc='upper right', frameon=False)
    ax.set_xlim(0, max_score)
    ax.set_ylim(0, 1.2)

    # Change borders, tick colors, etc.
    border_color = 'lightgrey'
    label_color = 'k'
    ax.spines['bottom'].set_color(border_color)
    ax.spines['left'].set_color(border_color)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom='on', top='off',
                   color=border_color)
    ax.tick_params(axis='y', which='both', left='on', right='off',
                   color=border_color)
    ax.xaxis.label.set_color(label_color)
    ax.yaxis.label.set_color(label_color)
    for l in ax.xaxis.get_ticklabels():
        l.set_color(label_color)
    for l in ax.yaxis.get_ticklabels():
        l.set_color(label_color)
    for l in leg.get_texts():
        l.set_color(label_color)
    fig.savefig('%s/survival.png' % args.input)
