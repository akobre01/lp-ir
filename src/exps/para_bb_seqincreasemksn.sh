#!/bin/bash

TIME=`(date +%Y%m%d%H%M%S)`

BASE_LOG_DIR="/home/akobren/akobren-on-canvas/software/repos/git/lp-ir/logs/"
EXPERIMENT_FILE="/home/akobren/akobren-on-canvas/software/repos/git/lp-ir/src/exps/SeqIncreaseMake.py"
OUTDIR="${BASE_LOG_DIR}/${TIME}"

mkdir -p $OUTDIR

EXPERIMENTS=()
EXP_NAMES=()
"""
usage: SeqIncreaseMake.py [-h] rev_max pap_revs weight_file step matcher

Arguments for creating weight files.

positional arguments:
  rev_max      max # of papers per rev
  pap_revs     # of reviewers per paper
  weight_file  the file from which to read the weights
  step         the step value by which we increase the makespan
  matcher      the matcher to use, either: "bb" or "ir"
"""
# usage: SeqIncreaseMake.py [-h] rev_max pap_revs weight_file step
# python SeqIncreaseMake.py 3 3 ../../data/train/200-200-2.0-5.0-skill_based/weights.txt 0.5
#############################
# SKILL BASED EXPERIMENTS
#############################
# EXPERIMENTS+=("5 5 ../../data/train/100-100-1.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/100-100-2.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/100-100-3.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/100-100-4.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/100-100-5.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/100-100-6.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/100-100-7.0-7.0-skill_based/weights.txt 0.1 bb")

# EXPERIMENTS+=("5 5 ../../data/train/200-200-1.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/200-200-2.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/200-200-3.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/200-200-4.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/200-200-5.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/200-200-6.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/200-200-7.0-7.0-skill_based/weights.txt 0.1 bb")

# EXPERIMENTS+=("5 5 ../../data/train/300-300-1.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/300-300-2.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/300-300-3.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/300-300-4.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/300-300-5.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/300-300-6.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/300-300-7.0-7.0-skill_based/weights.txt 0.1 bb")

# EXPERIMENTS+=("5 5 ../../data/train/400-400-1.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/400-400-2.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/400-400-3.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/400-400-4.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/400-400-5.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/400-400-6.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/400-400-7.0-7.0-skill_based/weights.txt 0.1 bb")

# EXPERIMENTS+=("5 5 ../../data/train/500-500-1.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/500-500-2.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/500-500-3.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/500-500-4.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/500-500-5.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/500-500-6.0-7.0-skill_based/weights.txt 0.1 bb")
# EXPERIMENTS+=("5 5 ../../data/train/500-500-7.0-7.0-skill_based/weights.txt 0.1 bb")

EXPERIMENTS+=("5 5 ../../data/train/600-600-1.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/600-600-2.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/600-600-3.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/600-600-4.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/600-600-5.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/600-600-6.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/600-600-7.0-7.0-skill_based/weights.txt 0.1 bb")

EXPERIMENTS+=("5 5 ../../data/train/700-700-1.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/700-700-2.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/700-700-3.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/700-700-4.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/700-700-5.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/700-700-6.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/700-700-7.0-7.0-skill_based/weights.txt 0.1 bb")

EXPERIMENTS+=("5 5 ../../data/train/800-800-1.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/800-800-2.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/800-800-3.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/800-800-4.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/800-800-5.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/800-800-6.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/800-800-7.0-7.0-skill_based/weights.txt 0.1 bb")

EXPERIMENTS+=("5 5 ../../data/train/900-900-1.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/900-900-2.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/900-900-3.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/900-900-4.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/900-900-5.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/900-900-6.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/900-900-7.0-7.0-skill_based/weights.txt 0.1 bb")

EXPERIMENTS+=("5 5 ../../data/train/1000-1000-1.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/1000-1000-2.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/1000-1000-3.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/1000-1000-4.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/1000-1000-5.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/1000-1000-6.0-7.0-skill_based/weights.txt 0.1 bb")
EXPERIMENTS+=("5 5 ../../data/train/1000-1000-7.0-7.0-skill_based/weights.txt 0.1 bb")

# EXP_NAMES+=("sim100-100-1-7-bb")
# EXP_NAMES+=("sim100-100-2-7-bb")
# EXP_NAMES+=("sim100-100-3-7-bb")
# EXP_NAMES+=("sim100-100-4-7-bb")
# EXP_NAMES+=("sim100-100-5-7-bb")
# EXP_NAMES+=("sim100-100-6-7-bb")
# EXP_NAMES+=("sim100-100-7-7-bb")

# EXP_NAMES+=("sim200-200-1-7-bb")
# EXP_NAMES+=("sim200-200-2-7-bb")
# EXP_NAMES+=("sim200-200-3-7-bb")
# EXP_NAMES+=("sim200-200-4-7-bb")
# EXP_NAMES+=("sim200-200-5-7-bb")
# EXP_NAMES+=("sim200-200-6-7-bb")
# EXP_NAMES+=("sim200-200-7-7-bb")

# EXP_NAMES+=("sim300-300-1-7-bb")
# EXP_NAMES+=("sim300-300-2-7-bb")
# EXP_NAMES+=("sim300-300-3-7-bb")
# EXP_NAMES+=("sim300-300-4-7-bb")
# EXP_NAMES+=("sim300-300-5-7-bb")
# EXP_NAMES+=("sim300-300-6-7-bb")
# EXP_NAMES+=("sim300-300-7-7-bb")

# EXP_NAMES+=("sim400-400-1-7-bb")
# EXP_NAMES+=("sim400-400-2-7-bb")
# EXP_NAMES+=("sim400-400-3-7-bb")
# EXP_NAMES+=("sim400-400-4-7-bb")
# EXP_NAMES+=("sim400-400-5-7-bb")
# EXP_NAMES+=("sim400-400-6-7-bb")
# EXP_NAMES+=("sim400-400-7-7-bb")

# EXP_NAMES+=("sim500-500-1-7-bb")
# EXP_NAMES+=("sim500-500-2-7-bb")
# EXP_NAMES+=("sim500-500-3-7-bb")
# EXP_NAMES+=("sim500-500-4-7-bb")
# EXP_NAMES+=("sim500-500-5-7-bb")
# EXP_NAMES+=("sim500-500-6-7-bb")
# EXP_NAMES+=("sim500-500-7-7-bb")

EXP_NAMES+=("sim600-600-1-7-bb")
EXP_NAMES+=("sim600-600-2-7-bb")
EXP_NAMES+=("sim600-600-3-7-bb")
EXP_NAMES+=("sim600-600-4-7-bb")
EXP_NAMES+=("sim600-600-5-7-bb")
EXP_NAMES+=("sim600-600-6-7-bb")
EXP_NAMES+=("sim600-600-7-7-bb")

EXP_NAMES+=("sim700-700-1-7-bb")
EXP_NAMES+=("sim700-700-2-7-bb")
EXP_NAMES+=("sim700-700-3-7-bb")
EXP_NAMES+=("sim700-700-4-7-bb")
EXP_NAMES+=("sim700-700-5-7-bb")
EXP_NAMES+=("sim700-700-6-7-bb")
EXP_NAMES+=("sim700-700-7-7-bb")

EXP_NAMES+=("sim800-800-1-7-bb")
EXP_NAMES+=("sim800-800-2-7-bb")
EXP_NAMES+=("sim800-800-3-7-bb")
EXP_NAMES+=("sim800-800-4-7-bb")
EXP_NAMES+=("sim800-800-5-7-bb")
EXP_NAMES+=("sim800-800-6-7-bb")
EXP_NAMES+=("sim800-800-7-7-bb")

EXP_NAMES+=("sim900-900-1-7-bb")
EXP_NAMES+=("sim900-900-2-7-bb")
EXP_NAMES+=("sim900-900-3-7-bb")
EXP_NAMES+=("sim900-900-4-7-bb")
EXP_NAMES+=("sim900-900-5-7-bb")
EXP_NAMES+=("sim900-900-6-7-bb")
EXP_NAMES+=("sim900-900-7-7-bb")

EXP_NAMES+=("sim1000-1000-1-7-bb")
EXP_NAMES+=("sim1000-1000-2-7-bb")
EXP_NAMES+=("sim1000-1000-3-7-bb")
EXP_NAMES+=("sim1000-1000-4-7-bb")
EXP_NAMES+=("sim1000-1000-5-7-bb")
EXP_NAMES+=("sim1000-1000-6-7-bb")
EXP_NAMES+=("sim1000-1000-7-7-bb")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
