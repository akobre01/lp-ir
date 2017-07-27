#!/bin/bash

source `pwd`/swarm/setup.sh

LOAD=7
COV=3
LB=4
DATA_NAME="subjects-only"
DATASET="data/cvpr/subjects-only.npy"
ASSIGNMENTS="${PM_ROOT}/results/${DATA_NAME}-load=${LOAD}-cov=${COV}-loadlb=${LB}"

# Run the basic lp formulation of paper matching.
sbatch $PM_ROOT/bin/util/run_plot_expert_survival.sh $ASSIGNMENTS $DATASET

exit
