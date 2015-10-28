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
EXPERIMENTS+=("48 1250 3 90 'relaxed' -f ./weights/exp16-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'relaxed' -f ./weights/exp17-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'relaxed' -f ./weights/exp18-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'relaxed' -f ./weights/exp19-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'relaxed' -f ./weights/exp20-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")

EXPERIMENTS+=("48 1250 3 90 'affinity' -f ./weights/exp16-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'affinity' -f ./weights/exp17-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'affinity' -f ./weights/exp18-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'affinity' -f ./weights/exp19-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'affinity' -f ./weights/exp20-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")

EXPERIMENTS+=("48 1250 3 90 'complete-relax' -f ./weights/exp16-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'complete-relax' -f ./weights/exp17-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'complete-relax' -f ./weights/exp18-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'complete-relax' -f ./weights/exp19-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'complete-relax' -f ./weights/exp20-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")

EXPERIMENTS+=("48 1250 3 90 'makespan' -f ./weights/exp16-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'makespan' -f ./weights/exp17-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'makespan' -f ./weights/exp18-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'makespan' -f ./weights/exp19-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")
EXPERIMENTS+=("48 1250 3 90 'makespan' -f ./weights/exp20-48-1250-0.5-2.0-skill_based.out -l ${OUTDIR}/")

EXP_NAMES+=("exp16-relaxed-48-1250")
EXP_NAMES+=("exp17-relaxed-48-1250")
EXP_NAMES+=("exp18-relaxed-48-1250")
EXP_NAMES+=("exp19-relaxed-48-1250")
EXP_NAMES+=("exp20-relaxed-48-1250")

EXP_NAMES+=("exp16-affinity-48-1250")
EXP_NAMES+=("exp17-affinity-48-1250")
EXP_NAMES+=("exp18-affinity-48-1250")
EXP_NAMES+=("exp19-affinity-48-1250")
EXP_NAMES+=("exp20-affinity-48-1250")

EXP_NAMES+=("exp16-complete_relax-48-1250")
EXP_NAMES+=("exp17-complete_relax-48-1250")
EXP_NAMES+=("exp18-complete_relax-48-1250")
EXP_NAMES+=("exp19-complete_relax-48-1250")
EXP_NAMES+=("exp20-complete_relax-48-1250")

EXP_NAMES+=("exp16-makespan-48-1250")
EXP_NAMES+=("exp17-makespan-48-1250")
EXP_NAMES+=("exp18-makespan-48-1250")
EXP_NAMES+=("exp19-makespan-48-1250")
EXP_NAMES+=("exp20-makespan-48-1250")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
