#!/bin/bash

source `pwd`/swarm/setup.sh

DATA_NAME="subjects-only"
DATASET="data/cvpr/subjects-only.npy"
ASSIGNMENTS="${PM_ROOT}/results/${DATA_NAME}-load=${LOAD}-cov=${COVERAGE}"
ASSIGNMENTS_LB="${PM_ROOT}/results/${DATA_NAME}-load=${LOAD}-cov=${COVERAGE}-loadlb=${LOAD_LB}"

# Run the basic lp formulation of paper matching.
sbatch $PM_ROOT/bin/util/run_plot_expert_survival.sh $ASSIGNMENTS $DATASET
sbatch $PM_ROOT/bin/util/run_plot_expert_survival.sh $ASSIGNMENTS_LB $DATASET

exit
