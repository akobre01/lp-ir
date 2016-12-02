#!/bin/bash
DATASET="data/train/kou_et_al/kou_score_mat_dm08.npy"
INC=0.01
OUTDIR="test_results"

# Run the baseline, bb with makespan and ir.
python -m src.exps.SeqIncreaseMake 3 $DATASET $INC bb $OUTDIR -i 0.0 -s
python -m src.exps.SeqIncreaseMake 3 $DATASET $INC bb $OUTDIR -i 1.2
python -m src.exps.SeqIncreaseMake 3 $DATASET $INC ir $OUTDIR -i 1.2