#!/bin/bash

set -exu

#DATA_NAME="cvpr17acs-0.9-pow-0.9"
#DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"

DATA_NAME=acs-0.9-pow-0.9-subjects
DATASET="data/cvpr/${DATA_NAME}.npy"
OUTDIR="results/${DATA_NAME}/heatmaps/"

# Create output director
mkdir -p $OUTDIR

# Produces two heatmaps of best and worst paper/reviewers
python -m src.utils.plot_sorted_heatmap $DATASET $OUTDIR

exit