#!/bin/bash

source `pwd`/swarm/setup.sh

LOAD=11
COV=5
DATA_NAME="subjects-only"
DATASET="data/cvpr/subjects-only.npy"
ASSIGNMENTS="${PM_ROOT}/results/${DATA_NAME}-load=${LOAD}-cov=${COV}"

# Run the basic lp formulation of paper matching.
sbatch $PM_ROOT/bin/util/run_plot_survival.sh $ASSIGNMENTS $DATASET 3

exit
