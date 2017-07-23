#!/bin/bash

source `pwd`/swarm/setup.sh

COVERAGE=3

INPUT=$1

# Run the basic lp formulation of paper matching.
sbatch $PM_ROOT/bin/cvpr/run_plot_aff_hist.sh $INPUT $PM_DATA_ROOT/cvpr/acs-0.9-pow-0.9-subjects $COVERAGE

exit