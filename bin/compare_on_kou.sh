#!/bin/bash
DATASET="data/train/kou_et_al/kou_score_mat_dm08.npy"
INC=0.01
OUTDIR="results/test"
MAXSCORE=3.0

# Run the baseline, bb with makespan and ir.
#python -m src.exps.SeqIncreaseMake 3 $DATASET $INC bb $OUTDIR -i 0.0 -s
#python -m src.exps.SeqIncreaseMake 3 $DATASET $INC bb $OUTDIR -i 1.27
#python -m src.exps.SeqIncreaseMake 3 $DATASET $INC ir $OUTDIR -i 1.27

# Plot survival of the models.
python -m src.plotting.plot_survival -i $OUTDIR -w $DATASET -m $MAXSCORE
python -m src.plotting.plot_aff_hists -i $OUTDIR -w $DATASET -m $MAXSCORE

# Create a latex table of statistics.
python -m src.plotting.create_latex_table -i $OUTDIR -w $DATASET -m $MAXSCORE

echo "[done.]"