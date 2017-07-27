#!/bin/bash
#
#SBATCH --job-name=mmdalb_single
#SBATCH --output=logs/cvpr/run_mmdalb_single.log
#SBATCH -e logs/cvpr/run_mmdalb_single.err
#SBATCH --partition=defq    # Partition to submit to
#
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=0-02:00         # Runtime in D-HH:MM
#SBATCH --mem=10000    # Memory in MB per cpu allocated

set -exu

DATA_NAME=$1
DATASET=$2
LOAD=$3
LOAD_LB=$4
COVERAGE=$5
MS=$6
ALG="dalb"

OUTDIR="results/${DATA_NAME}-load=${LOAD}-cov=${COVERAGE}-loadlb=${LOAD_LB}/${ALG}/ms=${MS}/"

# Create output director
mkdir -p $OUTDIR

# Run the basic lp formulation of paper matching.
python -m src.exps.run_mmdalb $LOAD $LOAD_LB $COVERAGE $DATASET $OUTDIR -m $MS

exit