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
#SBATCH --time=0-01:00         # Runtime in D-HH:MM
#SBATCH --mem=2048    # Memory in MB per cpu allocated

#source `pwd`/swarm/setup.sh
set -exu

DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
OUTDIR="results/cvpr"
COVERAGE=3

# Create output director
mkdir -p $OUTDIR

# Run the baseline, bb with makespan and ir.
python -m src.exps.run_basic $COVERAGE $DATASET $OUTDIR

echo "[done.]"