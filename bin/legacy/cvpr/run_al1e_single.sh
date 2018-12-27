#!/bin/bash
#
#SBATCH --job-name=al1e_single
#SBATCH --output=logs/cvpr/run_al1e_single.log
#SBATCH -e logs/cvpr/run_al1e_single.err
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
COVERAGE=$4
EXPERT=$5
GAP=$6
ALG="al1e"
OUTDIR="results/${DATA_NAME}-load=${LOAD}-cov=${COVERAGE}/${ALG}/expert=${EXPERT}-gap=${GAP}/"

# Create output director
mkdir -p $OUTDIR

# Run the basic lp formulation of paper matching.
python -m src.exps.run_al1e $LOAD $COVERAGE $DATASET $OUTDIR -e $EXPERT -g $GAP

exit
