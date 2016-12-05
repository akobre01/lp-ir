import argparse
import numpy as np
import os


def read_files_with_prefix(d, pre):
    """Read the files in directory d with prefix pre."""
    return [f for f in os.listdir(d) if f.startswith(pre)]


if __name__ == "__main__":
    """A script that reads from a results dir and generates a latex table.

    For a particular run/experiment (corresponding to some input directory),
    create a latex table of the statistics from that experiment. Specifically,
    write out: model, mean, min, max, AUC survival and time for each run.
    """
    parser = argparse.ArgumentParser(description=
                                     'Create a latex table of results.')
    parser.add_argument('-i', '--input', type=str,
                        help='The path to the directory that contains results.')
    parser.add_argument('-w', '--weights', type=str,
                        help='The path to the weights matrix used for results.')
    parser.add_argument('-m', '--max_score', type=float,
                        help='The maximum paper assignment score.')

    args = parser.parse_args()

    with open('%s/run_stats.tex' % args.input, 'w') as f:
        f.write('\\begin{figure *}[tbh]\n')
        f.write('\\centering\n')
        f.write('\\begin{tabular}{ | c | c | c | c | c | c | c |}\n')
        f.write('\\hline\n')
        f.write('Model & Mean & Min & Max & Std & AUC & Time (s)\\\\\n')
        f.write('\\hline\n')

        assignment_files = read_files_with_prefix(args.input, 'assignment')
        stats_files = read_files_with_prefix(args.input, 'stats')
        maxthresh_files = read_files_with_prefix(args.input, 'mxthresh')
        models = list(set([f.split('-')[1] for f in assignment_files]))

        # The next line is gross. We want to get a dictionary of model to
        # assignment file but for each model we might have multiple assignment
        # files so we have to find the best one. Based on the way we know that
        # files are named, we can figure this out py parsing the beginning and
        # end of the file names.
        model_to_assignment = {
            model: sorted([f for f in assignment_files
                           if f.startswith('assignment-%s' % model)],
                          key=lambda x:
                          float(x.split('-')[-1].split('.')[0]))[-1]
            for model in models
        }

        model_to_stats_f = {
            model: sorted([f for f in stats_files
                           if f.startswith('stats-%s' % model)],
                          key=lambda x: float(x.split('-')[-2][0]))[-1]
            for model in models
            }

        model_to_stats = {}
        for model, stats_f in model_to_stats_f.items():
            last_row = None
            for line in open('%s/%s' % (args.input, stats_f)):
                splits = line.split('\t')
                if splits[-2] != '----':
                    last_row = splits[:]
            model_to_stats[model] = last_row[:]

        weights = np.load(args.weights)

        rows = []
        x_vals = np.linspace(0, args.max_score, num=100)
        for model, assignment_f in model_to_assignment.items():
            assert np.all(weights <= 1.0)
            assignments = np.load('%s/%s' % (args.input, assignment_f))
            scores = np.sum(assignments * weights, axis=0)

            survivors = []
            for score_threshold in x_vals:
                survivors.append(
                    len([x for x in scores if x >= score_threshold]) /
                    np.size(scores))

            sol_time = float(model_to_stats[model][-1][:-2])
            rows.append([])
            rows[-1].append(model)
            rows[-1].append(np.mean(scores))
            rows[-1].append(np.min(scores))
            rows[-1].append(np.max(scores))
            rows[-1].append(np.std(scores))
            rows[-1].append(np.sum(survivors))
            rows[-1].append(sol_time)
        best_mean = max([r[1] for r in rows])
        best_min = max([r[2] for r in rows])
        best_max = max([r[3] for r in rows])
        best_std = min([r[4] for r in rows])
        best_auc = max([r[5] for r in rows])
        best_time = min([r[6] for r in rows])

        for row in rows:
            row_as_strs = [
                row[0],
                '\\textbf{%.2f}' % row[1] if round(row[1], 2) == round(
                    best_mean, 2) else '%.2f' % row[1],
                '\\textbf{%.2f}' % row[2] if round(row[2], 2) == round(
                    best_min, 2) else '%.2f' % row[2],
                '\\textbf{%.2f}' % row[3] if round(row[3], 2) == round(
                    best_max, 2) else '%.2f' % row[3],
                '\\textbf{%.2f}' % row[4] if round(row[4], 2) == round(
                    best_std, 2) else '%.2f' % row[4],
                '\\textbf{%.2f}' % row[5] if round(row[5], 2) == round(
                    best_auc, 2) else '%.2f' % row[5],
                '\\textbf{%.2f}' % row[6] if round(row[6], 2) == round(
                    best_time, 2) else '%.2f' % row[6],
            ]
            f.write(' & '.join(row_as_strs))
            f.write('\\\\\n')

        f.write('\\hline\n')
        f.write('\\end{tabular}\n')
        f.write('\\end{figure*}\n')
