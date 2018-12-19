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

CONFIG_DIR=$1

# Create boxplot for assignments
python -m src.plotting.boxplot_quants $CONFIG_DIR

exit