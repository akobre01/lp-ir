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
# SKILL BASED INTEGER EXPERIMENTS
#############################
EXPERIMENTS+=("48 1250 3 90 'relaxed' -f ./weights/exp31-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'relaxed' -f ./weights/exp32-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'relaxed' -f ./weights/exp33-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'relaxed' -f ./weights/exp34-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'relaxed' -f ./weights/exp35-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

EXPERIMENTS+=("48 1250 3 90 'affinity' -f ./weights/exp31-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'affinity' -f ./weights/exp32-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'affinity' -f ./weights/exp33-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'affinity' -f ./weights/exp34-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'affinity' -f ./weights/exp35-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

EXPERIMENTS+=("48 1250 3 90 'complete-relax' -f ./weights/exp31-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'complete-relax' -f ./weights/exp32-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'complete-relax' -f ./weights/exp33-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'complete-relax' -f ./weights/exp34-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'complete-relax' -f ./weights/exp35-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

EXPERIMENTS+=("48 1250 3 90 'makespan' -f ./weights/exp31-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'makespan' -f ./weights/exp32-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'makespan' -f ./weights/exp33-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'makespan' -f ./weights/exp34-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'makespan' -f ./weights/exp35-48-1250-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

EXP_NAMES+=("exp31-relaxed-48-1250")
EXP_NAMES+=("exp32-relaxed-48-1250")
EXP_NAMES+=("exp33-relaxed-48-1250")
EXP_NAMES+=("exp34-relaxed-48-1250")
EXP_NAMES+=("exp35-relaxed-48-1250")

EXP_NAMES+=("exp31-affinity-48-1250")
EXP_NAMES+=("exp32-affinity-48-1250")
EXP_NAMES+=("exp33-affinity-48-1250")
EXP_NAMES+=("exp34-affinity-48-1250")
EXP_NAMES+=("exp35-affinity-48-1250")

EXP_NAMES+=("exp31-complete_relax-48-1250")
EXP_NAMES+=("exp32-complete_relax-48-1250")
EXP_NAMES+=("exp33-complete_relax-48-1250")
EXP_NAMES+=("exp34-complete_relax-48-1250")
EXP_NAMES+=("exp35-complete_relax-48-1250")

EXP_NAMES+=("exp31-makespan-48-1250")
EXP_NAMES+=("exp32-makespan-48-1250")
EXP_NAMES+=("exp33-makespan-48-1250")
EXP_NAMES+=("exp34-makespan-48-1250")
EXP_NAMES+=("exp35-makespan-48-1250")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
