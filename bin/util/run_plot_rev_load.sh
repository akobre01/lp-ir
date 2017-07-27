#!/bin/bash
#
#SBATCH --job-name=revload
#SBATCH --output=logs/cvpr/revload.log
#SBATCH -e logs/cvpr/revload.err
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

# Plot the histogram of reviewer loads.
python -m src.plotting.plot_rev_load $ASSIGNMENT

exit