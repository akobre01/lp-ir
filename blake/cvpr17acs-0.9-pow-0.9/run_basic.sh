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

# Run the basic lp formulation of paper matching.
echo "$PM_ROOT/bin/cvpr/run_basic.sh $DATA_NAME $DATASET $LOAD $COVERAGE" | qsub -cwd  -j y  -o results/${DATA_NAME}/run_basic.log" -m e -M akobren@cs.umass.edu -l mem_token=18G -N run_basic -S /bin/sh

exit
