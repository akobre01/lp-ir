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
# SKILL BASED INTEGER EXPERIMENTS (OLD)
#############################
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp11-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp12-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp13-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp14-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp15-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp11-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp12-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp13-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp14-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp15-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp11-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp12-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp13-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp14-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp15-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp11-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp12-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp13-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp14-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp15-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

EXP_NAMES+=("exp11-relaxed-500-900")
EXP_NAMES+=("exp12-relaxed-500-900")
EXP_NAMES+=("exp13-relaxed-500-900")
EXP_NAMES+=("exp14-relaxed-500-900")
EXP_NAMES+=("exp15-relaxed-500-900")

EXP_NAMES+=("exp11-affinity-500-900")
EXP_NAMES+=("exp12-affinity-500-900")
EXP_NAMES+=("exp13-affinity-500-900")
EXP_NAMES+=("exp14-affinity-500-900")
EXP_NAMES+=("exp15-affinity-500-900")

EXP_NAMES+=("exp11-complete_relax-500-900")
EXP_NAMES+=("exp12-complete_relax-500-900")
EXP_NAMES+=("exp13-complete_relax-500-900")
EXP_NAMES+=("exp14-complete_relax-500-900")
EXP_NAMES+=("exp15-complete_relax-500-900")

EXP_NAMES+=("exp11-makespan-500-900")
EXP_NAMES+=("exp12-makespan-500-900")
EXP_NAMES+=("exp13-makespan-500-900")
EXP_NAMES+=("exp14-makespan-500-900")
EXP_NAMES+=("exp15-makespan-500-900")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
