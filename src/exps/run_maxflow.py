"""Run the basic matcher using a max flow min cost implementation."""
import argparse
import numpy as np
import os
import time

from ..matching_models.MaxFlow import MaxFlowMinCost

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run the max flow min cost matcher on dataset.')
    parser.add_argument('load_const', type=int, help='max papers per rev.')
    parser.add_argument('cov_const', type=int, help='# of reviewers per paper')
    parser.add_argument('weight_file', type=str,
                        help='the file from which to read the weights')
    parser.add_argument('output', type=str,
                        help='the directory in which to save the results.')
    args = parser.parse_args()

    coverage = args.cov_const
    weights = np.load(args.weight_file)
    weights_name = args.weight_file[
                   args.weight_file.rfind('/') + 1:args.weight_file.rfind('.')]
    n_rev = np.size(weights, axis=0)
    n_pap = np.size(weights, axis=1)

    max_load = args.load_const
    out_dir = args.output
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # Output files.
    assignment_file = os.path.join(args.output, 'assignment')
    time_file = os.path.join(args.output, 'time.tsv')

    bm = MaxFlowMinCost([max_load] * n_rev, [coverage] * n_pap, weights)
    s = time.time()
    bm.solve()
    t = time.time() - s
    f = open(time_file, 'w')
    f.write(str(t))
    f.close()
    np.save(assignment_file, bm.sol_as_mat())