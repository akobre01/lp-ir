#!/bin/bash

set -exu

DATA_NAME="cvpr17acs-0.9-pow-0.9"
DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
COVERAGE=3
OUTDIR="results/${DATA_NAME}-cov=${COVERAGE}/"

# Create output director
mkdir -p $OUTDIR

# Plot the histogram of paper scores.
python -m src.plotting.plot_aff_hists $OUTDIR $DATASET $COVERAGE

echo "[done.]"