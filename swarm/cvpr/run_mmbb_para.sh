#!/bin/bash

source `pwd`/swarm/setup.sh

DATA_NAME="cvpr17acs-0.9-pow-0.9"
DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
COVERAGE=5
ALG="bb"

for gap in `seq 0 0.05 0.3`
do
    for ms in `seq 0 0.25 ${COVERAGE}`
    do
        OUTDIR="results/${DATA_NAME}-cov=${COVERAGE}/${ALG}-ms=${ms}-gp=${gap}/"

        # Create output director
        mkdir -p $OUTDIR

        # Run the basic lp formulation of paper matching.
        sbatch $PM_ROOT/swarm/cvpr/run_mmbb_single.sh $COVERAGE $ms $gap
    done
done
exit
