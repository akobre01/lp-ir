#!/bin/bash

TIME=`(date +%Y%m%d%H%M%S)`

BASE_SRC_DIR="/home/akobren/akobren-on-canvas/software/repos/git/lp-ir/"
BASE_LOG_DIR="/home/akobren/akobren-on-canvas/software/repos/git/lp-ir/logs/"
EXPERIMENT_FILE="${BASE_SRC_DIR}matching_exp.py"
OUTDIR="${BASE_LOG_DIR}/${TIME}"

# the name of the symbolic link to this run's directory
LATEST=latest
mkdir -p $OUTDIR
#ln -Ffhs $OUTDIR "${EXPERIMENTS_BASE_DIR}/${LATEST}"

# experimental parameters

EXPERIMENTS=()
EXP_NAMES=()
# usage: distortExpr.py [-h] [-v] [-b] [-p] [-f [WEIGHTS_FILE]]
#                       reviewers papers reviews_per_paper itrs consts_per_itr
#                       matcher
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp1-500-900-0.5-2.0-skill_based")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp2-500-900-0.5-2.0-skill_based")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp3-500-900-0.5-2.0-skill_based")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp4-500-900-0.5-2.0-skill_based")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp5-500-900-0.5-2.0-skill_based")

EXPERIMENTS+=("500 900 3 6  -f ./weights/exp1-500-900-0.5-2.0-skill_based")
EXPERIMENTS+=("500 900 3 6  -f ./weights/exp2-500-900-0.5-2.0-skill_based")
EXPERIMENTS+=("500 900 3 6  -f ./weights/exp3-500-900-0.5-2.0-skill_based")
EXPERIMENTS+=("500 900 3 6  -f ./weights/exp4-500-900-0.5-2.0-skill_based")
EXPERIMENTS+=("500 900 3 6  -f ./weights/exp5-500-900-0.5-2.0-skill_based")

EXP_NAMES+=("00-relaxed-500-900")
EXP_NAMES+=("01-relaxed-500-900")
EXP_NAMES+=("02-relaxed-500-900")
EXP_NAMES+=("03-relaxed-500-900")
EXP_NAMES+=("04-relaxed-500-900")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N "relaxed-paper-matching"  -S /bin/sh
done

echo "[done.]"
