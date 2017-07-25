#!/bin/bash
#
#SBATCH --job-name=affhist
#SBATCH --output=logs/cvpr/affhist.log
#SBATCH -e logs/cvpr/affhist.err
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
AFFS=$2
COVERAGE=$3

# Plot the histogram of paper scores.
python -m src.plotting.plot_aff_hists $ASSIGNMENT $AFFS $COVERAGE

echo "[done.]"