import argparse
import json
import numpy as np
import os

from utils.Config import Config


if __name__ == '__main__':
    """A script that computes a series of stats about a matching."""
    parser = argparse.ArgumentParser(description='Generate matching stats.')
    parser.add_argument('config_dir', type=str, help='path to exp_out config')
    args = parser.parse_args()

    config = Config(os.path.join(args.config_dir, 'config.json'))
    scores = np.load(config.score_f)
    loads = np.load(config.load_f)
    if config.load_lb_f:
        loads_lb = np.load(config.load_lb_f)
    else:
        loads_lb = None
    covs = np.load(config.cov_f)

    assignment = np.load(os.path.join(args.config_dir, 'results',
                                      'assignment.npy'))
    time_f = os.path.join(args.config_dir, 'results', 'time.tsv')
    if os.path.exists(time_f):
        with open(time_f, 'r') as f:
            time = float(f.read())
    else:
        time = -1

    makespan_f = os.path.join(args.config_dir, 'results', 'makespan.tsv')

    if os.path.exists(makespan_f):
        with open(makespan_f, 'r') as f:
            makespan = float(f.read())
    else:
        makespan = None
    match_scores = np.sum(assignment * scores, axis=0)
    max_pap_score = np.max(match_scores)
    min_pap_score = np.min(match_scores)
    avg_pap_score = np.mean(match_scores)
    std_pap_score = np.std(match_scores)

    num_quantiles = 5
    sorted_scores = sorted(match_scores)
    num_papers = np.size(sorted_scores)
    scores_per_quant = int(np.floor(num_papers / num_quantiles) + 1)
    quants = []
    for i in range(num_quantiles):
        if i != num_quantiles - 1:
            quants.append(
                sorted_scores[i * scores_per_quant: (i + 1) * scores_per_quant])
        else:
            quants.append(sorted_scores[i * scores_per_quant:])

    if makespan is None:
        makespan = 0.0
    ms_violations = np.sum((match_scores < makespan).astype(int))
    rev_loads = np.sum(assignment, axis=1)
    load_lb_violations = np.sum(rev_loads < loads_lb).astype(int)
    load_violations = np.sum(rev_loads > loads).astype(int)

    output_f = os.path.join(args.config_dir, 'results', 'stats.json')
    with open(output_f, 'w') as f:
        d = {'max_pap_score': float(max_pap_score),
             'min_pap_score': float(min_pap_score),
             'avg_pap_score': float(avg_pap_score),
             'std_pap_score': float(std_pap_score),
             'time': float(time),
             'ms': float(makespan),
             'lb_vio': int(load_lb_violations),
             'ub_vio': int(load_violations),
             'ms_vio': int(ms_violations),
             'q1med': np.median(quants[0]),
             'q2med': np.median(quants[1]),
             'q3med': np.median(quants[2]),
             'q4med': np.median(quants[3]),
             'q5med': np.median(quants[4])}
        json.dump(d, f, sort_keys=True, indent=4)
