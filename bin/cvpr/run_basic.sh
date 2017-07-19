#!/bin/bash

set -exu

DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
OUTDIR="results/test-cvpr"
MAXSCORE=3

# Run the baseline, bb with makespan and ir.
python -m src.exps.run_baseline 3 $DATASET $OUTDIR

# Plot survival of the models.
python -m src.plotting.plot_survival -i $OUTDIR -w $DATASET -m $MAXSCORE

echo "[done.]"