#!/bin/bash

TIME=`(date +%Y%m%d%H%M%S)`

BASE_LOG_DIR="/home/akobren/akobren-on-canvas/software/repos/git/lp-ir/logs/"
EXPERIMENT_FILE="/home/akobren/akobren-on-canvas/software/repos/git/lp-ir/src/utils/subsample_weights.py"
OUTDIR="${BASE_LOG_DIR}/${TIME}"

mkdir -p $OUTDIR

# experimental parameters

EXPERIMENTS=()
EXP_NAMES=()
"""
usage: subsample_weights.py [-h] [--plot] weight_file nrev npap

Subsample an affinity matrix.

positional arguments:
  weight_file  the file containing the affinity matrix
  nrev         # of reviewers (rows)
  npap         # of papers (cols)
"""

#############################
# CREATE WEIGHT FILES
# nrev npap bp1 bp2 structure
#############################

EXPERIMENTS+=("../../data/train/300-300-1.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/300-300-2.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/300-300-3.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/300-300-4.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/300-300-5.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/300-300-6.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/300-300-7.0-7.0-skill_based 50 50")

EXPERIMENTS+=("../../data/train/300-300-1.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/300-300-2.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/300-300-3.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/300-300-4.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/300-300-5.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/300-300-6.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/300-300-7.0-7.0-skill_based 100 100")

EXPERIMENTS+=("../../data/train/300-300-1.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/300-300-2.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/300-300-3.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/300-300-4.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/300-300-5.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/300-300-6.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/300-300-7.0-7.0-skill_based 150 150")

EXPERIMENTS+=("../../data/train/300-300-1.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/300-300-2.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/300-300-3.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/300-300-4.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/300-300-5.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/300-300-6.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/300-300-7.0-7.0-skill_based 200 200")

EXPERIMENTS+=("../../data/train/400-400-1.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/400-400-2.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/400-400-3.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/400-400-4.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/400-400-5.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/400-400-6.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/400-400-7.0-7.0-skill_based 50 50")

EXPERIMENTS+=("../../data/train/400-400-1.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/400-400-2.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/400-400-3.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/400-400-4.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/400-400-5.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/400-400-6.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/400-400-7.0-7.0-skill_based 100 100")

EXPERIMENTS+=("../../data/train/400-400-1.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/400-400-2.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/400-400-3.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/400-400-4.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/400-400-5.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/400-400-6.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/400-400-7.0-7.0-skill_based 150 150")

EXPERIMENTS+=("../../data/train/400-400-1.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/400-400-2.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/400-400-3.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/400-400-4.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/400-400-5.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/400-400-6.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/400-400-7.0-7.0-skill_based 200 200")

EXPERIMENTS+=("../../data/train/500-500-1.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/500-500-2.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/500-500-3.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/500-500-4.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/500-500-5.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/500-500-6.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/500-500-7.0-7.0-skill_based 50 50")

EXPERIMENTS+=("../../data/train/500-500-1.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/500-500-2.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/500-500-3.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/500-500-4.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/500-500-5.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/500-500-6.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/500-500-7.0-7.0-skill_based 100 100")

EXPERIMENTS+=("../../data/train/500-500-1.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/500-500-2.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/500-500-3.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/500-500-4.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/500-500-5.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/500-500-6.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/500-500-7.0-7.0-skill_based 150 150")

EXPERIMENTS+=("../../data/train/500-500-1.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/500-500-2.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/500-500-3.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/500-500-4.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/500-500-5.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/500-500-6.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/500-500-7.0-7.0-skill_based 200 200")

EXPERIMENTS+=("../../data/train/600-600-1.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/600-600-2.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/600-600-3.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/600-600-4.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/600-600-5.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/600-600-6.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/600-600-7.0-7.0-skill_based 50 50")

EXPERIMENTS+=("../../data/train/600-600-1.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/600-600-2.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/600-600-3.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/600-600-4.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/600-600-5.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/600-600-6.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/600-600-7.0-7.0-skill_based 100 100")

EXPERIMENTS+=("../../data/train/600-600-1.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/600-600-2.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/600-600-3.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/600-600-4.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/600-600-5.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/600-600-6.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/600-600-7.0-7.0-skill_based 150 150")

EXPERIMENTS+=("../../data/train/600-600-1.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/600-600-2.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/600-600-3.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/600-600-4.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/600-600-5.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/600-600-6.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/600-600-7.0-7.0-skill_based 200 200")

EXPERIMENTS+=("../../data/train/700-700-1.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/700-700-2.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/700-700-3.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/700-700-4.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/700-700-5.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/700-700-6.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/700-700-7.0-7.0-skill_based 50 50")

EXPERIMENTS+=("../../data/train/700-700-1.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/700-700-2.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/700-700-3.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/700-700-4.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/700-700-5.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/700-700-6.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/700-700-7.0-7.0-skill_based 100 100")

EXPERIMENTS+=("../../data/train/700-700-1.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/700-700-2.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/700-700-3.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/700-700-4.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/700-700-5.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/700-700-6.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/700-700-7.0-7.0-skill_based 150 150")

EXPERIMENTS+=("../../data/train/700-700-1.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/700-700-2.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/700-700-3.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/700-700-4.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/700-700-5.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/700-700-6.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/700-700-7.0-7.0-skill_based 200 200")

EXPERIMENTS+=("../../data/train/800-800-1.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/800-800-2.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/800-800-3.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/800-800-4.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/800-800-5.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/800-800-6.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/800-800-7.0-7.0-skill_based 50 50")

EXPERIMENTS+=("../../data/train/800-800-1.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/800-800-2.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/800-800-3.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/800-800-4.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/800-800-5.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/800-800-6.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/800-800-7.0-7.0-skill_based 100 100")

EXPERIMENTS+=("../../data/train/800-800-1.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/800-800-2.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/800-800-3.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/800-800-4.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/800-800-5.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/800-800-6.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/800-800-7.0-7.0-skill_based 150 150")

EXPERIMENTS+=("../../data/train/800-800-1.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/800-800-2.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/800-800-3.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/800-800-4.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/800-800-5.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/800-800-6.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/800-800-7.0-7.0-skill_based 200 200")

EXPERIMENTS+=("../../data/train/900-900-1.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/900-900-2.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/900-900-3.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/900-900-4.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/900-900-5.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/900-900-6.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/900-900-7.0-7.0-skill_based 50 50")

EXPERIMENTS+=("../../data/train/900-900-1.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/900-900-2.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/900-900-3.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/900-900-4.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/900-900-5.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/900-900-6.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/900-900-7.0-7.0-skill_based 100 100")

EXPERIMENTS+=("../../data/train/900-900-1.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/900-900-2.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/900-900-3.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/900-900-4.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/900-900-5.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/900-900-6.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/900-900-7.0-7.0-skill_based 150 150")

EXPERIMENTS+=("../../data/train/900-900-1.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/900-900-2.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/900-900-3.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/900-900-4.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/900-900-5.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/900-900-6.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/900-900-7.0-7.0-skill_based 200 200")

EXPERIMENTS+=("../../data/train/1000-1000-1.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/1000-1000-2.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/1000-1000-3.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/1000-1000-4.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/1000-1000-5.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/1000-1000-6.0-7.0-skill_based 50 50")
EXPERIMENTS+=("../../data/train/1000-1000-7.0-7.0-skill_based 50 50")

EXPERIMENTS+=("../../data/train/1000-1000-1.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/1000-1000-2.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/1000-1000-3.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/1000-1000-4.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/1000-1000-5.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/1000-1000-6.0-7.0-skill_based 100 100")
EXPERIMENTS+=("../../data/train/1000-1000-7.0-7.0-skill_based 100 100")

EXPERIMENTS+=("../../data/train/1000-1000-1.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/1000-1000-2.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/1000-1000-3.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/1000-1000-4.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/1000-1000-5.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/1000-1000-6.0-7.0-skill_based 150 150")
EXPERIMENTS+=("../../data/train/1000-1000-7.0-7.0-skill_based 150 150")

EXPERIMENTS+=("../../data/train/1000-1000-1.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/1000-1000-2.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/1000-1000-3.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/1000-1000-4.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/1000-1000-5.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/1000-1000-6.0-7.0-skill_based 200 200")
EXPERIMENTS+=("../../data/train/1000-1000-7.0-7.0-skill_based 200 200")

EXP_NAMES+=("o300-50-50-1-7")
EXP_NAMES+=("o300-50-50-2-7")
EXP_NAMES+=("o300-50-50-3-7")
EXP_NAMES+=("o300-50-50-4-7")
EXP_NAMES+=("o300-50-50-5-7")
EXP_NAMES+=("o300-50-50-6-7")
EXP_NAMES+=("o300-50-50-7-7")

EXP_NAMES+=("o300-100-100-1-7")
EXP_NAMES+=("o300-100-100-2-7")
EXP_NAMES+=("o300-100-100-3-7")
EXP_NAMES+=("o300-100-100-4-7")
EXP_NAMES+=("o300-100-100-5-7")
EXP_NAMES+=("o300-100-100-6-7")
EXP_NAMES+=("o300-100-100-7-7")

EXP_NAMES+=("o300-150-150-1-7")
EXP_NAMES+=("o300-150-150-2-7")
EXP_NAMES+=("o300-150-150-3-7")
EXP_NAMES+=("o300-150-150-4-7")
EXP_NAMES+=("o300-150-150-5-7")
EXP_NAMES+=("o300-150-150-6-7")
EXP_NAMES+=("o300-150-150-7-7")

EXP_NAMES+=("o300-200-200-1-7")
EXP_NAMES+=("o300-200-200-2-7")
EXP_NAMES+=("o300-200-200-3-7")
EXP_NAMES+=("o300-200-200-4-7")
EXP_NAMES+=("o300-200-200-5-7")
EXP_NAMES+=("o300-200-200-6-7")
EXP_NAMES+=("o300-200-200-7-7")

EXP_NAMES+=("o400-50-50-1-7")
EXP_NAMES+=("o400-50-50-2-7")
EXP_NAMES+=("o400-50-50-3-7")
EXP_NAMES+=("o400-50-50-4-7")
EXP_NAMES+=("o400-50-50-5-7")
EXP_NAMES+=("o400-50-50-6-7")
EXP_NAMES+=("o400-50-50-7-7")

EXP_NAMES+=("o400-100-100-1-7")
EXP_NAMES+=("o400-100-100-2-7")
EXP_NAMES+=("o400-100-100-3-7")
EXP_NAMES+=("o400-100-100-4-7")
EXP_NAMES+=("o400-100-100-5-7")
EXP_NAMES+=("o400-100-100-6-7")
EXP_NAMES+=("o400-100-100-7-7")

EXP_NAMES+=("o400-150-150-1-7")
EXP_NAMES+=("o400-150-150-2-7")
EXP_NAMES+=("o400-150-150-3-7")
EXP_NAMES+=("o400-150-150-4-7")
EXP_NAMES+=("o400-150-150-5-7")
EXP_NAMES+=("o400-150-150-6-7")
EXP_NAMES+=("o400-150-150-7-7")

EXP_NAMES+=("o400-200-200-1-7")
EXP_NAMES+=("o400-200-200-2-7")
EXP_NAMES+=("o400-200-200-3-7")
EXP_NAMES+=("o400-200-200-4-7")
EXP_NAMES+=("o400-200-200-5-7")
EXP_NAMES+=("o400-200-200-6-7")
EXP_NAMES+=("o400-200-200-7-7")

EXP_NAMES+=("o500-50-50-1-7")
EXP_NAMES+=("o500-50-50-2-7")
EXP_NAMES+=("o500-50-50-3-7")
EXP_NAMES+=("o500-50-50-4-7")
EXP_NAMES+=("o500-50-50-5-7")
EXP_NAMES+=("o500-50-50-6-7")
EXP_NAMES+=("o500-50-50-7-7")

EXP_NAMES+=("o500-100-100-1-7")
EXP_NAMES+=("o500-100-100-2-7")
EXP_NAMES+=("o500-100-100-3-7")
EXP_NAMES+=("o500-100-100-4-7")
EXP_NAMES+=("o500-100-100-5-7")
EXP_NAMES+=("o500-100-100-6-7")
EXP_NAMES+=("o500-100-100-7-7")

EXP_NAMES+=("o500-150-150-1-7")
EXP_NAMES+=("o500-150-150-2-7")
EXP_NAMES+=("o500-150-150-3-7")
EXP_NAMES+=("o500-150-150-4-7")
EXP_NAMES+=("o500-150-150-5-7")
EXP_NAMES+=("o500-150-150-6-7")
EXP_NAMES+=("o500-150-150-7-7")

EXP_NAMES+=("o500-200-200-1-7")
EXP_NAMES+=("o500-200-200-2-7")
EXP_NAMES+=("o500-200-200-3-7")
EXP_NAMES+=("o500-200-200-4-7")
EXP_NAMES+=("o500-200-200-5-7")
EXP_NAMES+=("o500-200-200-6-7")
EXP_NAMES+=("o500-200-200-7-7")

EXP_NAMES+=("o600-50-50-1-7")
EXP_NAMES+=("o600-50-50-2-7")
EXP_NAMES+=("o600-50-50-3-7")
EXP_NAMES+=("o600-50-50-4-7")
EXP_NAMES+=("o600-50-50-5-7")
EXP_NAMES+=("o600-50-50-6-7")
EXP_NAMES+=("o600-50-50-7-7")

EXP_NAMES+=("o600-100-100-1-7")
EXP_NAMES+=("o600-100-100-2-7")
EXP_NAMES+=("o600-100-100-3-7")
EXP_NAMES+=("o600-100-100-4-7")
EXP_NAMES+=("o600-100-100-5-7")
EXP_NAMES+=("o600-100-100-6-7")
EXP_NAMES+=("o600-100-100-7-7")

EXP_NAMES+=("o600-150-150-1-7")
EXP_NAMES+=("o600-150-150-2-7")
EXP_NAMES+=("o600-150-150-3-7")
EXP_NAMES+=("o600-150-150-4-7")
EXP_NAMES+=("o600-150-150-5-7")
EXP_NAMES+=("o600-150-150-6-7")
EXP_NAMES+=("o600-150-150-7-7")

EXP_NAMES+=("o600-200-200-1-7")
EXP_NAMES+=("o600-200-200-2-7")
EXP_NAMES+=("o600-200-200-3-7")
EXP_NAMES+=("o600-200-200-4-7")
EXP_NAMES+=("o600-200-200-5-7")
EXP_NAMES+=("o600-200-200-6-7")
EXP_NAMES+=("o600-200-200-7-7")

EXP_NAMES+=("o700-50-50-1-7")
EXP_NAMES+=("o700-50-50-2-7")
EXP_NAMES+=("o700-50-50-3-7")
EXP_NAMES+=("o700-50-50-4-7")
EXP_NAMES+=("o700-50-50-5-7")
EXP_NAMES+=("o700-50-50-6-7")
EXP_NAMES+=("o700-50-50-7-7")

EXP_NAMES+=("o700-100-100-1-7")
EXP_NAMES+=("o700-100-100-2-7")
EXP_NAMES+=("o700-100-100-3-7")
EXP_NAMES+=("o700-100-100-4-7")
EXP_NAMES+=("o700-100-100-5-7")
EXP_NAMES+=("o700-100-100-6-7")
EXP_NAMES+=("o700-100-100-7-7")

EXP_NAMES+=("o700-150-150-1-7")
EXP_NAMES+=("o700-150-150-2-7")
EXP_NAMES+=("o700-150-150-3-7")
EXP_NAMES+=("o700-150-150-4-7")
EXP_NAMES+=("o700-150-150-5-7")
EXP_NAMES+=("o700-150-150-6-7")
EXP_NAMES+=("o700-150-150-7-7")

EXP_NAMES+=("o700-200-200-1-7")
EXP_NAMES+=("o700-200-200-2-7")
EXP_NAMES+=("o700-200-200-3-7")
EXP_NAMES+=("o700-200-200-4-7")
EXP_NAMES+=("o700-200-200-5-7")
EXP_NAMES+=("o700-200-200-6-7")
EXP_NAMES+=("o700-200-200-7-7")

EXP_NAMES+=("o800-50-50-1-7")
EXP_NAMES+=("o800-50-50-2-7")
EXP_NAMES+=("o800-50-50-3-7")
EXP_NAMES+=("o800-50-50-4-7")
EXP_NAMES+=("o800-50-50-5-7")
EXP_NAMES+=("o800-50-50-6-7")
EXP_NAMES+=("o800-50-50-7-7")

EXP_NAMES+=("o800-100-100-1-7")
EXP_NAMES+=("o800-100-100-2-7")
EXP_NAMES+=("o800-100-100-3-7")
EXP_NAMES+=("o800-100-100-4-7")
EXP_NAMES+=("o800-100-100-5-7")
EXP_NAMES+=("o800-100-100-6-7")
EXP_NAMES+=("o800-100-100-7-7")

EXP_NAMES+=("o800-150-150-1-7")
EXP_NAMES+=("o800-150-150-2-7")
EXP_NAMES+=("o800-150-150-3-7")
EXP_NAMES+=("o800-150-150-4-7")
EXP_NAMES+=("o800-150-150-5-7")
EXP_NAMES+=("o800-150-150-6-7")
EXP_NAMES+=("o800-150-150-7-7")

EXP_NAMES+=("o800-200-200-1-7")
EXP_NAMES+=("o800-200-200-2-7")
EXP_NAMES+=("o800-200-200-3-7")
EXP_NAMES+=("o800-200-200-4-7")
EXP_NAMES+=("o800-200-200-5-7")
EXP_NAMES+=("o800-200-200-6-7")
EXP_NAMES+=("o800-200-200-7-7")

EXP_NAMES+=("o900-50-50-1-7")
EXP_NAMES+=("o900-50-50-2-7")
EXP_NAMES+=("o900-50-50-3-7")
EXP_NAMES+=("o900-50-50-4-7")
EXP_NAMES+=("o900-50-50-5-7")
EXP_NAMES+=("o900-50-50-6-7")
EXP_NAMES+=("o900-50-50-7-7")

EXP_NAMES+=("o900-100-100-1-7")
EXP_NAMES+=("o900-100-100-2-7")
EXP_NAMES+=("o900-100-100-3-7")
EXP_NAMES+=("o900-100-100-4-7")
EXP_NAMES+=("o900-100-100-5-7")
EXP_NAMES+=("o900-100-100-6-7")
EXP_NAMES+=("o900-100-100-7-7")

EXP_NAMES+=("o900-150-150-1-7")
EXP_NAMES+=("o900-150-150-2-7")
EXP_NAMES+=("o900-150-150-3-7")
EXP_NAMES+=("o900-150-150-4-7")
EXP_NAMES+=("o900-150-150-5-7")
EXP_NAMES+=("o900-150-150-6-7")
EXP_NAMES+=("o900-150-150-7-7")

EXP_NAMES+=("o900-200-200-1-7")
EXP_NAMES+=("o900-200-200-2-7")
EXP_NAMES+=("o900-200-200-3-7")
EXP_NAMES+=("o900-200-200-4-7")
EXP_NAMES+=("o900-200-200-5-7")
EXP_NAMES+=("o900-200-200-6-7")
EXP_NAMES+=("o900-200-200-7-7")

EXP_NAMES+=("o1000-50-50-1-7")
EXP_NAMES+=("o1000-50-50-2-7")
EXP_NAMES+=("o1000-50-50-3-7")
EXP_NAMES+=("o1000-50-50-4-7")
EXP_NAMES+=("o1000-50-50-5-7")
EXP_NAMES+=("o1000-50-50-6-7")
EXP_NAMES+=("o1000-50-50-7-7")

EXP_NAMES+=("o1000-100-100-1-7")
EXP_NAMES+=("o1000-100-100-2-7")
EXP_NAMES+=("o1000-100-100-3-7")
EXP_NAMES+=("o1000-100-100-4-7")
EXP_NAMES+=("o1000-100-100-5-7")
EXP_NAMES+=("o1000-100-100-6-7")
EXP_NAMES+=("o1000-100-100-7-7")

EXP_NAMES+=("o1000-150-150-1-7")
EXP_NAMES+=("o1000-150-150-2-7")
EXP_NAMES+=("o1000-150-150-3-7")
EXP_NAMES+=("o1000-150-150-4-7")
EXP_NAMES+=("o1000-150-150-5-7")
EXP_NAMES+=("o1000-150-150-6-7")
EXP_NAMES+=("o1000-150-150-7-7")

EXP_NAMES+=("o1000-200-200-1-7")
EXP_NAMES+=("o1000-200-200-2-7")
EXP_NAMES+=("o1000-200-200-3-7")
EXP_NAMES+=("o1000-200-200-4-7")
EXP_NAMES+=("o1000-200-200-5-7")
EXP_NAMES+=("o1000-200-200-6-7")
EXP_NAMES+=("o1000-200-200-7-7")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
