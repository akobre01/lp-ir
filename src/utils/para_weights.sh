#!/bin/bash

TIME=`(date +%Y%m%d%H%M%S)`

BASE_LOG_DIR="/home/akobren/akobren-on-canvas/software/repos/git/lp-ir/logs/"
EXPERIMENT_FILE="/home/akobren/akobren-on-canvas/software/repos/git/lp-ir/src/utils/weights.py"
OUTDIR="${BASE_LOG_DIR}/${TIME}"

mkdir -p $OUTDIR

# experimental parameters

EXPERIMENTS=()
EXP_NAMES=()
# usage: weights.py [-h] [--plot] nrev npap bp1 bp2 structure

#############################
# CREATE WEIGHT FILES
# nrev npap bp1 bp2 structure
#############################
# EXPERIMENTS+=("100 100 1 7 skill_based")
# EXPERIMENTS+=("100 100 2 7 skill_based")
# EXPERIMENTS+=("100 100 3 7 skill_based")
# EXPERIMENTS+=("100 100 4 7 skill_based")
# EXPERIMENTS+=("100 100 5 7 skill_based")
# EXPERIMENTS+=("100 100 6 7 skill_based")
# EXPERIMENTS+=("100 100 7 7 skill_based")

# EXPERIMENTS+=("200 200 1 7 skill_based")
# EXPERIMENTS+=("200 200 2 7 skill_based")
# EXPERIMENTS+=("200 200 3 7 skill_based")
# EXPERIMENTS+=("200 200 4 7 skill_based")
# EXPERIMENTS+=("200 200 5 7 skill_based")
# EXPERIMENTS+=("200 200 6 7 skill_based")
# EXPERIMENTS+=("200 200 7 7 skill_based")

# EXPERIMENTS+=("300 300 1 7 skill_based")
# EXPERIMENTS+=("300 300 2 7 skill_based")
# EXPERIMENTS+=("300 300 3 7 skill_based")
# EXPERIMENTS+=("300 300 4 7 skill_based")
# EXPERIMENTS+=("300 300 5 7 skill_based")
# EXPERIMENTS+=("300 300 6 7 skill_based")
# EXPERIMENTS+=("300 300 7 7 skill_based")

# EXPERIMENTS+=("400 400 1 7 skill_based")
# EXPERIMENTS+=("400 400 2 7 skill_based")
# EXPERIMENTS+=("400 400 3 7 skill_based")
# EXPERIMENTS+=("400 400 4 7 skill_based")
# EXPERIMENTS+=("400 400 5 7 skill_based")
# EXPERIMENTS+=("400 400 6 7 skill_based")
# EXPERIMENTS+=("400 400 7 7 skill_based")

# EXPERIMENTS+=("500 500 1 7 skill_based")
# EXPERIMENTS+=("500 500 2 7 skill_based")
# EXPERIMENTS+=("500 500 3 7 skill_based")
# EXPERIMENTS+=("500 500 4 7 skill_based")
# EXPERIMENTS+=("500 500 5 7 skill_based")
# EXPERIMENTS+=("500 500 6 7 skill_based")
# EXPERIMENTS+=("500 500 7 7 skill_based")

EXPERIMENTS+=("600 600 1 7 skill_based")
EXPERIMENTS+=("600 600 2 7 skill_based")
EXPERIMENTS+=("600 600 3 7 skill_based")
EXPERIMENTS+=("600 600 4 7 skill_based")
EXPERIMENTS+=("600 600 5 7 skill_based")
EXPERIMENTS+=("600 600 6 7 skill_based")
EXPERIMENTS+=("600 600 7 7 skill_based")

EXPERIMENTS+=("700 700 1 7 skill_based")
EXPERIMENTS+=("700 700 2 7 skill_based")
EXPERIMENTS+=("700 700 3 7 skill_based")
EXPERIMENTS+=("700 700 4 7 skill_based")
EXPERIMENTS+=("700 700 5 7 skill_based")
EXPERIMENTS+=("700 700 6 7 skill_based")
EXPERIMENTS+=("700 700 7 7 skill_based")

EXPERIMENTS+=("800 800 1 7 skill_based")
EXPERIMENTS+=("800 800 2 7 skill_based")
EXPERIMENTS+=("800 800 3 7 skill_based")
EXPERIMENTS+=("800 800 4 7 skill_based")
EXPERIMENTS+=("800 800 5 7 skill_based")
EXPERIMENTS+=("800 800 6 7 skill_based")
EXPERIMENTS+=("800 800 7 7 skill_based")

EXPERIMENTS+=("900 900 1 7 skill_based")
EXPERIMENTS+=("900 900 2 7 skill_based")
EXPERIMENTS+=("900 900 3 7 skill_based")
EXPERIMENTS+=("900 900 4 7 skill_based")
EXPERIMENTS+=("900 900 5 7 skill_based")
EXPERIMENTS+=("900 900 6 7 skill_based")
EXPERIMENTS+=("900 900 7 7 skill_based")

EXPERIMENTS+=("1000 1000 1 7 skill_based")
EXPERIMENTS+=("1000 1000 2 7 skill_based")
EXPERIMENTS+=("1000 1000 3 7 skill_based")
EXPERIMENTS+=("1000 1000 4 7 skill_based")
EXPERIMENTS+=("1000 1000 5 7 skill_based")
EXPERIMENTS+=("1000 1000 6 7 skill_based")
EXPERIMENTS+=("1000 1000 7 7 skill_based")

# EXP_NAMES+=("w100-100-1-7")
# EXP_NAMES+=("w100-100-2-7")
# EXP_NAMES+=("w100-100-3-7")
# EXP_NAMES+=("w100-100-4-7")
# EXP_NAMES+=("w100-100-5-7")
# EXP_NAMES+=("w100-100-6-7")
# EXP_NAMES+=("w100-100-7-7")

# EXP_NAMES+=("w200-200-1-7")
# EXP_NAMES+=("w200-200-2-7")
# EXP_NAMES+=("w200-200-3-7")
# EXP_NAMES+=("w200-200-4-7")
# EXP_NAMES+=("w200-200-5-7")
# EXP_NAMES+=("w200-200-6-7")
# EXP_NAMES+=("w200-200-7-7")

# EXP_NAMES+=("w300-300-1-7")
# EXP_NAMES+=("w300-300-2-7")
# EXP_NAMES+=("w300-300-3-7")
# EXP_NAMES+=("w300-300-4-7")
# EXP_NAMES+=("w300-300-5-7")
# EXP_NAMES+=("w300-300-6-7")
# EXP_NAMES+=("w300-300-7-7")

# EXP_NAMES+=("w400-400-1-7")
# EXP_NAMES+=("w400-400-2-7")
# EXP_NAMES+=("w400-400-3-7")
# EXP_NAMES+=("w400-400-4-7")
# EXP_NAMES+=("w400-400-5-7")
# EXP_NAMES+=("w400-400-6-7")
# EXP_NAMES+=("w400-400-7-7")

# EXP_NAMES+=("w500-500-1-7")
# EXP_NAMES+=("w500-500-2-7")
# EXP_NAMES+=("w500-500-3-7")
# EXP_NAMES+=("w500-500-4-7")
# EXP_NAMES+=("w500-500-5-7")
# EXP_NAMES+=("w500-500-6-7")
# EXP_NAMES+=("w500-500-7-7")

EXP_NAMES+=("w600-600-1-7")
EXP_NAMES+=("w600-600-2-7")
EXP_NAMES+=("w600-600-3-7")
EXP_NAMES+=("w600-600-4-7")
EXP_NAMES+=("w600-600-5-7")
EXP_NAMES+=("w600-600-6-7")
EXP_NAMES+=("w600-600-7-7")

EXP_NAMES+=("w700-700-1-7")
EXP_NAMES+=("w700-700-2-7")
EXP_NAMES+=("w700-700-3-7")
EXP_NAMES+=("w700-700-4-7")
EXP_NAMES+=("w700-700-5-7")
EXP_NAMES+=("w700-700-6-7")
EXP_NAMES+=("w700-700-7-7")

EXP_NAMES+=("w800-800-1-7")
EXP_NAMES+=("w800-800-2-7")
EXP_NAMES+=("w800-800-3-7")
EXP_NAMES+=("w800-800-4-7")
EXP_NAMES+=("w800-800-5-7")
EXP_NAMES+=("w800-800-6-7")
EXP_NAMES+=("w800-800-7-7")

EXP_NAMES+=("w900-900-1-7")
EXP_NAMES+=("w900-900-2-7")
EXP_NAMES+=("w900-900-3-7")
EXP_NAMES+=("w900-900-4-7")
EXP_NAMES+=("w900-900-5-7")
EXP_NAMES+=("w900-900-6-7")
EXP_NAMES+=("w900-900-7-7")

EXP_NAMES+=("w1000-1000-1-7")
EXP_NAMES+=("w1000-1000-2-7")
EXP_NAMES+=("w1000-1000-3-7")
EXP_NAMES+=("w1000-1000-4-7")
EXP_NAMES+=("w1000-1000-5-7")
EXP_NAMES+=("w1000-1000-6-7")
EXP_NAMES+=("w1000-1000-7-7")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
