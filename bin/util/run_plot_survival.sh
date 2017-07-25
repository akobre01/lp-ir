#!/bin/bash
#
#SBATCH --job-name=survival
#SBATCH --output=logs/util/survival.log
#SBATCH -e logs/util/survival.err
#SBATCH --partition=defq    # Partition to submit to
#
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-02:00         # Runtime in D-HH:MM
#SBATCH --mem=8000    # Memory in MB per cpu allocated

set -exu

ASSIGNMENT=$1
WEIGHTS=$2
MAXSCORE=$3

# Plot the histogram of paper scores.
python -m src.plotting.plot_survival $ASSIGNMENT $WEIGHTS -m $MAXSCORE

echo "[done.]"
