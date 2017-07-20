#!/bin/bash

set -exu

DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
OUTDIR="results/cvpr"
COVERAGE=3

# Run the baseline, bb with makespan and ir.
python -m src.exps.run_basic $COVERAGE $DATASET $OUTDIR

echo "[done.]"