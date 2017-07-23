#!/bin/bash

source `pwd`/swarm/setup.sh

# This dataset has 1373 reviewers and 2623 papers.
# if coverage is 3
#   2623 * 3 / 1373 ~= 5.73
# if coverage is 5
#   2623 * 5 / 1373 ~= 9.55
# It is different from the other affinity matrices because it only uses
# subject areas.

DATA_NAME="subjects-only"
DATASET="data/cvpr/subjects-only.npy"

LOAD=11
COVERAGE=3

# Run the basic lp formulation of paper matching.
sbatch $PM_ROOT/bin/cvpr/run_basic.sh $DATA_NAME $DATASET $LOAD $COVERAGE $ms $gap

exit
