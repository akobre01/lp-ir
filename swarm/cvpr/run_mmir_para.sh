#!/bin/bash

source `pwd`/swarm/setup.sh

DATA_NAME="cvpr17acs-0.9-pow-0.9"
DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
COVERAGE=5
ALG="ir"

for ms in `seq 0 0.25 ${COVERAGE}`
do
    OUTDIR="results/${DATA_NAME}-cov=${COVERAGE}/${ALG}-ms=${ms}/"

    # Create output director
    mkdir -p $OUTDIR

    # Run the basic lp formulation of paper matching.
    sbatch $PM_ROOT/swarm/cvpr/run_mmir_single.sh $COVERAGE $ms
done
exit
