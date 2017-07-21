#!/bin/bash

source `pwd`/blake/setup.sh

# This dataset has 1373 reviewers and 2623 papers.
# if coverage is 3
#   2623 * 3 / 1373 ~= 5.73
# if coverage is 5
#   2623 * 5 / 1373 ~= 9.55

DATA_NAME="cvpr17acs-0.9-pow-0.9"
DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"

LOAD=8
COVERAGE=3

for gap in `seq 0 0.05 0.3`
do
    for ms in `seq 0 0.25 ${COVERAGE}`
    do
        LOGDIR=$PM_ROOT/logs/${DATA_NAME}-load=${LOAD}-cov=${COVERAGE}/mmbb/ms=$ms-gap=$gap/
        mkdir -p $LOGDIR
        LOGFILE=${LOGDIR}/run_mmbb_single.log

        # Run the basic lp formulation of paper matching.
        echo "$PM_ROOT/bin/cvpr/run_mmbb.sh $DATA_NAME $DATASET $LOAD $COVERAGE $ms $gap" | qsub -v PATH -cwd  -j y  -o $LOGFILE -m e -M akobren@cs.umass.edu -l mem_token=18G -N run_basic -S /bin/sh
    done
done
exit


