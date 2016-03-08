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

#############################
# SKILL BASED SKILL_AND_DIFFICULTY EXPERIMENTS
#############################
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp22-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp23-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp24-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp25-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp22-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp23-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp24-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp25-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp22-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp23-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp24-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp25-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp22-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp23-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp24-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp25-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

EXP_NAMES+=("exp21-relaxed-500-900")
EXP_NAMES+=("exp22-relaxed-500-900")
EXP_NAMES+=("exp23-relaxed-500-900")
EXP_NAMES+=("exp24-relaxed-500-900")
EXP_NAMES+=("exp25-relaxed-500-900")

EXP_NAMES+=("exp21-affinity-500-900")
EXP_NAMES+=("exp22-affinity-500-900")
EXP_NAMES+=("exp23-affinity-500-900")
EXP_NAMES+=("exp24-affinity-500-900")
EXP_NAMES+=("exp25-affinity-500-900")

EXP_NAMES+=("exp21-complete_relax-500-900")
EXP_NAMES+=("exp22-complete_relax-500-900")
EXP_NAMES+=("exp23-complete_relax-500-900")
EXP_NAMES+=("exp24-complete_relax-500-900")
EXP_NAMES+=("exp25-complete_relax-500-900")

EXP_NAMES+=("exp21-makespan-500-900")
EXP_NAMES+=("exp22-makespan-500-900")
EXP_NAMES+=("exp23-makespan-500-900")
EXP_NAMES+=("exp24-makespan-500-900")
EXP_NAMES+=("exp25-makespan-500-900")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
