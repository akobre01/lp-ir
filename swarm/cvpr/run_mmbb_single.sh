#!/bin/bash
#
#SBATCH --job-name=mmbb_single
#SBATCH --output=logs/cvpr/run_mmbb_single.log
#SBATCH -e logs/cvpr/run_mmbb_single.err
#SBATCH --partition=defq    # Partition to submit to
#
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-02:00         # Runtime in D-HH:MM
#SBATCH --mem=8000    # Memory in MB per cpu allocated

source `pwd`/swarm/setup.sh

set -exu

DATA_NAME="cvpr17acs-0.9-pow-0.9"
DATASET="data/cvpr/cvpr17acs-0.9-pow-0.9.npy"
COVERAGE=$1
ALG="bb"
MS=$2
GAP=$3
OUTDIR="results/${DATA_NAME}-cov=${COVERAGE}/${ALG}-ms=${MS}/"

# Create output director
mkdir -p $OUTDIR

# Run the basic lp formulation of paper matching.
python -m src.exps.run_mmbb $COVERAGE $DATASET $OUTDIR -m $MS -g $GAP

exit
