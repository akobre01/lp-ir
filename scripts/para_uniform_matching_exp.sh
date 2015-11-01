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

#################################
# UNIFORM EXPERIMENTS
#################################
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp6-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp7-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp8-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp9-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp10-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp6-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp7-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp8-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp9-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp10-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp6-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp7-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp8-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp9-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp10-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp6-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp7-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp8-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp9-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp10-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")

EXP_NAMES+=("exp6-uni-relaxed-500-900")
EXP_NAMES+=("exp7-uni-relaxed-500-900")
EXP_NAMES+=("exp8-uni-relaxed-500-900")
EXP_NAMES+=("exp9-uni-relaxed-500-900")
EXP_NAMES+=("exp10-uni-relaxed-500-900")

EXP_NAMES+=("exp6-uni-affinity-500-900")
EXP_NAMES+=("exp7-uni-affinity-500-900")
EXP_NAMES+=("exp8-uni-affinity-500-900")
EXP_NAMES+=("exp9-uni-affinity-500-900")
EXP_NAMES+=("exp10-uni-affinity-500-900")

EXP_NAMES+=("exp6-uni-complete_relax-500-900")
EXP_NAMES+=("exp7-uni-complete_relax-500-900")
EXP_NAMES+=("exp8-uni-complete_relax-500-900")
EXP_NAMES+=("exp9-uni-complete_relax-500-900")
EXP_NAMES+=("exp10-uni-complete_relax-500-900")

EXP_NAMES+=("exp6-uni-makespan-500-900")
EXP_NAMES+=("exp7-uni-makespan-500-900")
EXP_NAMES+=("exp8-uni-makespan-500-900")
EXP_NAMES+=("exp9-uni-makespan-500-900")
EXP_NAMES+=("exp10-uni-makespan-500-900")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
