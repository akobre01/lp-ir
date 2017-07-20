#!/bin/bash

set -exu

DATA_NAME="cvpr17acs-0.9-pow-0.9"
DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
COVERAGE=3
OUTDIR="results/${DATA_NAME}-cov=${COVERAGE}/"

# Create output director
mkdir -p $OUTDIR

# Run the baseline, bb with makespan and ir.
python -m src.utils.plot_sorted_heatmap $DATASET $OUTDIR

echo "[done.]"