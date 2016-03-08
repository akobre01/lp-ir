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
EXPERIMENTS+=("1196 1299 5 7 'relaxed' -f ./weights/tpms.out -l ${OUTDIR}/")
EXPERIMENTS+=("1196 1299 5 7 'affinity' -f ./weights/tpms.out -l ${OUTDIR}/")
EXPERIMENTS+=("1196 1299 5 7 'complete-relax' -f ./weights/tpms.out -l ${OUTDIR}/")
EXPERIMENTS+=("1196 1299 5 7 'makespan' -f ./weights/tpms.out -l ${OUTDIR}/")

EXP_NAMES+=("exp21-relaxed-1196-1299")
EXP_NAMES+=("exp22-affinity-1196-1299")
EXP_NAMES+=("exp23-complete_relax-1196-1299")
EXP_NAMES+=("exp24-makespan-1196-1299")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
