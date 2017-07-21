#!/bin/bash

source `pwd`/swarm/setup.sh

# This dataset has 1373 reviewers and 2623 papers.
# if coverage is 3
#   2623 * 3 / 1373 ~= 5.73
# if coverage is 5
#   2623 * 5 / 1373 ~= 9.55

DATA_NAME="cvpr17acs-0.9-pow-0.9"
DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"

LOAD=8
COVERAGE=3
ALG="bb"

for gap in `seq 0 0.05 0.3`
do
    for ms in `seq 0 0.25 ${COVERAGE}`
    do
        # Run the basic lp formulation of paper matching.
        sbatch $PM_ROOT/swarm/cvpr/run_mmbb_single.sh $LOAD $COVERAGE $ms $gap
    done
done
exit
