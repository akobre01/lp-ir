#!/bin/bash

source `pwd`/swarm/setup.sh

# This dataset has 1373 reviewers and 2623 papers.
# if coverage is 3
#   2623 * 3 / 1373 ~= 5.73
# if coverage is 5
#   2623 * 5 / 1373 ~= 9.55
# if coverage is 7
#   2623 * 7 / 1373 ~= 13.37
# It is different from the other affinity matrices because it only uses
# subject areas.

DATA_NAME="subjects-only"
DATASET="data/cvpr/subjects-only.npy"

LOAD=7
LOAD_LB=4
COVERAGE=3

for ms in `seq 0 0.5 ${COVERAGE}`
do
    # Run the basic lp formulation of paper matching.
    sbatch $PM_ROOT/bin/cvpr/run_mmdalb_single.sh $DATA_NAME $DATASET $LOAD $LOAD_LB $COVERAGE $ms
done
exit
