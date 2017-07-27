#!/bin/bash
#
#SBATCH --job-name=al1elb_single
#SBATCH --output=logs/cvpr/run_al1elb_single.log
#SBATCH -e logs/cvpr/run_al1elb_single.err
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
EXPERT=$6
GAP=$7
ALG="al1elb"
OUTDIR="results/${DATA_NAME}-load=${LOAD}-cov=${COVERAGE}-loadlb=${LOAD_LB}/${ALG}/expert=${EXPERT}-gap=${GAP}/"

# Create output director
mkdir -p $OUTDIR

# Run the basic lp formulation of paper matching.
python -m src.exps.run_al1elb $LOAD $LOAD_LB $COVERAGE $DATASET $OUTDIR -e $EXPERT -g $GAP

exit
