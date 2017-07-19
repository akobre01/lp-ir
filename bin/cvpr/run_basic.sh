#!/bin/bash

set -exu

DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
OUTDIR="results/test-cvpr"
MAXSCORE=3

# Run the baseline, bb with makespan and ir.
#python -m src.exps.run_basic 3 $DATASET $OUTDIR

# Plot survival and histogram of results.
python -m src.plotting.plot_survival -i $OUTDIR -w $DATASET -m $MAXSCORE
python -m src.plotting.plot_aff_hists -i $OUTDIR -w $DATASET -m $MAXSCORE

echo "[done.]"