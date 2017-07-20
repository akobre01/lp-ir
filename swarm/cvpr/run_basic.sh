#!/bin/bash
#
#SBATCH --job-name=basic_papermatch
#SBATCH --output=logs/cvpr/run_basic.log
#SBATCH -e logs/cvpr/run_basic.err
#SBATCH --partition=defq    # Partition to submit to
#
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1-00:00         # Runtime in D-HH:MM
#SBATCH --mem=45000    # Memory in MB per cpu allocated

#source `pwd`/swarm/setup.sh
set -exu

DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
OUTDIR="results/test-cvpr"
MAXSCORE=3

# Run the baseline, bb with makespan and ir.
python -m src.exps.run_basic 3 $DATASET $OUTDIR

echo "[done.]"