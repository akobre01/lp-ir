"""Run makespan formulation with lower bound."""
import argparse
import numpy as np
import os
import time

from ..matching_models.MLLB import MLLB

if __name__ == "__main__":
    """Solve the makespan version of paper matching using gurobi's heuristics.

    If no makespan is passed in, run a binary search over possible makespan
    values to find the best value.  If a makespan is passed in, then only run
    using that makespan.

    This script writes the assignment constructed as well as the total time to
    construct the assignment.
    """
    parser = argparse.ArgumentParser(
        description='Run gurobis ILP solver on dataset.')
    parser.add_argument('load_const', type=int, help='max papers / reviewers.')
    parser.add_argument('load_lb', type=int, help='min papers / reviewers.')
    parser.add_argument('cov_const', type=int, help='# of reviewers per paper')
    parser.add_argument('weight_file', type=str,
                        help='the file from which to read the weights')
    parser.add_argument('output', type=str,
                        help='the directory in which to save the results.')
    parser.add_argument('-m', '--makespan', type=float,
                        help='the value of the makespan to run.')
    parser.add_argument('-g', '--mipgap', type=float,
                        help='the MIP gap to allow.')
    args = parser.parse_args()

    load_lb = args.load_lb
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

    mllb = MLLB([max_load] * n_rev, [load_lb] * n_rev,
                [coverage] * n_pap, weights)
    s = time.time()
    if args.makespan:
        mllb.change_makespan(args.makespan)
        mllb.solve_with_current_makespan()
    else:
        mllb.solve()
    t = time.time() - s
    f = open(time_file, 'w')
    f.write(str(t))
    f.close()
    np.save(assignment_file, mllb.sol_as_mat())
