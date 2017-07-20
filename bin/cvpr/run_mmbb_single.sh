#!/bin/bash

set -exu

DATA_NAME="cvpr17acs-0.9-pow-0.9"
DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
COVERAGE=3
ALG="bb"
MS=$1
OUTDIR="results/${DATA_NAME}-cov=${COVERAGE}/${ALG}-ms=${MS}/"

# Create output director
mkdir -p $OUTDIR

# Run the basic lp formulation of paper matching.
python -m src.exps.run_mmbb $COVERAGE $DATASET $OUTDIR -m $MS

echo "[done.]"