#!/bin/bash

set -exu

DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
OUTDIR="results/heatmaps/"

# Create output director
mkdir -p $OUTDIR

# Run the baseline, bb with makespan and ir.
python -m src.utils.plot_sorted_heatmap $DATASET $OUTDIR

echo "[done.]"