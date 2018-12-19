"""Run the basic matcher using a max flow min cost implementation."""
import argparse
import datetime
import numpy as np
import os
import random
import time

from matching_models.MaxFlow import MaxFlowMinCost
from matching_models.ResidFlow import ResidFlow

from utils.Config import Config
from utils.IO import mkdir_p, copy_source_to_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run the min cost flow matcher with makespan.')
    parser.add_argument('config', type=str, help='config file.')

    args = parser.parse_args()
    config = Config(args.config)

    loads = np.load(config.load_f)
    covs = np.load(config.cov_f)
    scores = np.load(config.score_f)
    ms = config.makespan

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

    n_rev = np.size(scores, axis=0)
    n_pap = np.size(scores, axis=1)

    mkdir_p(output_dir)

    # Output files.
    assignment_file = os.path.join(output_dir, 'assignment')
    time_file = os.path.join(output_dir, 'time.tsv')

    bm = MaxFlowMinCost(loads, covs, scores)
    s = time.time()
    bm.solve()
    rf = ResidFlow(loads, covs, scores, ms, bm.sol_as_mat())
    can_improve = rf.try_improve_ms()
    print('can improve')
    print(can_improve)
    num_itrs = 0
    while can_improve:
        can_improve = rf.try_improve_ms()
        num_itrs += 1

    t = time.time() - s
    f = open(time_file, 'w')
    f.write(str(t))
    f.close()
    np.save(assignment_file, rf.sol_as_mat())
