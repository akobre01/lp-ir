"""Run the resid matcher with lower bounds."""
import argparse
import datetime
import numpy as np
import os
import random
import time

from matching_models.MCFLB import MCFLB
from matching_models.MsFlowLB import MsFlowLB

from utils.Config import Config
from utils.IO import mkdir_p, copy_source_to_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run the min cost flow matcher.')
    parser.add_argument('config', type=str, help='config file.')

    args = parser.parse_args()
    config = Config(args.config)

    loads = np.load(config.load_f)
    loads_lb = np.load(config.load_lb_f)
    covs = np.load(config.cov_f)
    scores = np.load(config.score_f)
    ms = config.makespan

    assert(config.match_model == 'flow-lb')

    now = datetime.datetime.now()
    ts = "{:04d}-{:02d}-{:02d}-{:02d}-{:02d}-{:02d}".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    rand = random.Random(config.random_seed)
    config.random = rand
    print('Using random seed %s' % config.random_seed)
    debug = config.debug

    # Set up output dir
    config.experiment_out_dir = os.path.join(
        config.experiment_out_dir, config.dataset_name, config.match_model,
        'ms=%s' % config.makespan, ts)
    output_dir = config.experiment_out_dir

    copy_source_to_dir(output_dir, config)

    output_dir = os.path.join(output_dir, 'results')

    n_rev = np.size(scores, axis=0)
    n_pap = np.size(scores, axis=1)

    mkdir_p(output_dir)

    # Output files.
    assignment_file = os.path.join(output_dir, 'assignment')
    time_file = os.path.join(output_dir, 'time.tsv')
    ms_file = os.path.join(output_dir, 'ms.tsv')

    s = time.time()
    m = MsFlowLB(loads, loads_lb, covs, scores)
    sol = m.solve()
    t = time.time() - s

    f = open(time_file, 'w')
    f.write(str(t))
    f.close()
    np.save(assignment_file, sol)

    f = open(ms_file, 'w')
    f.write(str(m.makespan))
    f.close()
