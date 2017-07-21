#!/bin/bash

source `pwd`/blake/setup.sh

# This dataset has 1373 reviewers and 2623 papers.
# if coverage is 3
#   2623 * 3 / 1373 ~= 5.73
# if coverage is 5
#   2623 * 5 / 1373 ~= 9.55
# It is different from the other affinity matrices because it only uses
# subject areas.

DATA_NAME="subjects-only"
DATASET="data/cvpr/subjects-only.npy"

LOAD=8
COVERAGE=3
LOGDIR=$PM_ROOT/logs/${DATA_NAME}
LOGFILE=$LOGDIR/run_basic.log

mkdir -p $LOGFILE

# Run the basic lp formulation of paper matching.
echo "$PM_ROOT/bin/cvpr/run_basic.sh $DATA_NAME $DATASET $LOAD $COVERAGE" | qsub -v PATH -cwd  -j y  -o $LOGFILE -m e -M akobren@cs.umass.edu -l mem_token=18G -N run_basic -S /bin/sh

exit
