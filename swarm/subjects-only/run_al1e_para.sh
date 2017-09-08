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
ALG="al1e"

for gap in `seq 0.05 0.05 0.05`
do
    for expert in `seq 0 0.1 1.0`
    do
        # Run the basic lp formulation of paper matching.
        sbatch $PM_ROOT/bin/cvpr/run_al1e_single.sh $DATA_NAME $DATASET $LOAD $COVERAGE $expert $gap
    done
done
exit
