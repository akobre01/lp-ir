#!/bin/bash
#
#SBATCH --job-name=maxflow_ms
#SBATCH --output=logs/cvpr/run_maxflow_ms.log
#SBATCH -e logs/cvpr/run_maxflow_ms.err
#SBATCH --partition=defq    # Partition to submit to
#
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=0-02:00         # Runtime in D-HH:MM
#SBATCH --mem=8000    # Memory in MB per cpu allocated

set -exu

DATA_NAME=$1
DATASET=$2
LOAD=$3
COVERAGE=$4
MS=$5
ALG="mf"
OUTDIR="results/${DATA_NAME}-load=${LOAD}-cov=${COVERAGE}/${ALG}/ms=${MS}/"

# Create output director
mkdir -p $OUTDIR

# Run the basic lp formulation of paper matching.
python -m src.exps.run_maxflow $LOAD $COVERAGE $DATASET $OUTDIR -m $MS

exit