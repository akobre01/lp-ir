#!/bin/bash

source `pwd`/swarm/setup.sh

DATA_NAME="cvpr17acs-0.9-pow-0.9"
DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
ASSIGNMENTS="${PM_ROOT}/results/${DATA_NAME}-load=8-cov=3"

# Run the basic lp formulation of paper matching.
sbatch $PM_ROOT/bin/util/run_plot_survival.sh $ASSIGNMENTS $DATASET 3

exit
