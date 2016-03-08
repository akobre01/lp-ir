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
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp6-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp7-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp8-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp9-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp10-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp6-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp7-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp8-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp9-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp10-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp6-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp7-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp8-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp9-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp10-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp6-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp7-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp8-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp9-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp10-500-900-0.0-0.0-uniform.out -l ${OUTDIR}/")

# EXP_NAMES+=("exp6-uni-relaxed-500-900")
# EXP_NAMES+=("exp7-uni-relaxed-500-900")
# EXP_NAMES+=("exp8-uni-relaxed-500-900")
# EXP_NAMES+=("exp9-uni-relaxed-500-900")
# EXP_NAMES+=("exp10-uni-relaxed-500-900")

# EXP_NAMES+=("exp6-uni-affinity-500-900")
# EXP_NAMES+=("exp7-uni-affinity-500-900")
# EXP_NAMES+=("exp8-uni-affinity-500-900")
# EXP_NAMES+=("exp9-uni-affinity-500-900")
# EXP_NAMES+=("exp10-uni-affinity-500-900")

# EXP_NAMES+=("exp6-uni-complete_relax-500-900")
# EXP_NAMES+=("exp7-uni-complete_relax-500-900")
# EXP_NAMES+=("exp8-uni-complete_relax-500-900")
# EXP_NAMES+=("exp9-uni-complete_relax-500-900")
# EXP_NAMES+=("exp10-uni-complete_relax-500-900")

# EXP_NAMES+=("exp6-uni-makespan-500-900")
# EXP_NAMES+=("exp7-uni-makespan-500-900")
# EXP_NAMES+=("exp8-uni-makespan-500-900")
# EXP_NAMES+=("exp9-uni-makespan-500-900")
# EXP_NAMES+=("exp10-uni-makespan-500-900")

# ############################
# # SKILL BASED EXPERIMENTS
# ############################
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp1-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp2-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp3-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp4-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp5-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp1-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp2-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp3-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp4-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp5-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp1-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp2-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp3-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp4-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp5-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp1-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp2-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp3-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp4-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp5-500-900-0.5-2.0-skill_based.out -l ${OUTDIR}/")

# EXP_NAMES+=("exp1-relaxed-500-900")
# EXP_NAMES+=("exp2-relaxed-500-900")
# EXP_NAMES+=("exp3-relaxed-500-900")
# EXP_NAMES+=("exp4-relaxed-500-900")
# EXP_NAMES+=("exp5-relaxed-500-900")

# EXP_NAMES+=("exp1-affinity-500-900")
# EXP_NAMES+=("exp2-affinity-500-900")
# EXP_NAMES+=("exp3-affinity-500-900")
# EXP_NAMES+=("exp4-affinity-500-900")
# EXP_NAMES+=("exp5-affinity-500-900")

# EXP_NAMES+=("exp1-complete_relax-500-900")
# EXP_NAMES+=("exp2-complete_relax-500-900")
# EXP_NAMES+=("exp3-complete_relax-500-900")
# EXP_NAMES+=("exp4-complete_relax-500-900")
# EXP_NAMES+=("exp5-complete_relax-500-900")

# EXP_NAMES+=("exp1-makespan-500-900")
# EXP_NAMES+=("exp2-makespan-500-900")
# EXP_NAMES+=("exp3-makespan-500-900")
# EXP_NAMES+=("exp4-makespan-500-900")
# EXP_NAMES+=("exp5-makespan-500-900")

#############################
# SKILL AND DIFFICULTY BASED INTEGER EXPERIMENTS
#############################
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp26-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp27-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp28-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp29-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp30-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp26-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp27-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp28-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp29-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp30-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp26-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp27-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp28-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp29-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp30-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp26-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp27-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp28-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp29-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp30-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

EXP_NAMES+=("exp26-relaxed-500-900")
EXP_NAMES+=("exp27-relaxed-500-900")
EXP_NAMES+=("exp28-relaxed-500-900")
EXP_NAMES+=("exp29-relaxed-500-900")
EXP_NAMES+=("exp30-relaxed-500-900")

EXP_NAMES+=("exp26-affinity-500-900")
EXP_NAMES+=("exp27-affinity-500-900")
EXP_NAMES+=("exp28-affinity-500-900")
EXP_NAMES+=("exp29-affinity-500-900")
EXP_NAMES+=("exp30-affinity-500-900")

EXP_NAMES+=("exp26-complete_relax-500-900")
EXP_NAMES+=("exp27-complete_relax-500-900")
EXP_NAMES+=("exp28-complete_relax-500-900")
EXP_NAMES+=("exp29-complete_relax-500-900")
EXP_NAMES+=("exp30-complete_relax-500-900")

EXP_NAMES+=("exp26-makespan-500-900")
EXP_NAMES+=("exp27-makespan-500-900")
EXP_NAMES+=("exp28-makespan-500-900")
EXP_NAMES+=("exp29-makespan-500-900")
EXP_NAMES+=("exp30-makespan-500-900")

#############################
# SKILL BASED SKILL_AND_DIFFICULTY EXPERIMENTS
#############################
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp22-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp23-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp24-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp25-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp22-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp23-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp24-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp25-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp22-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp23-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp24-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp25-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp22-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp23-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp24-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp25-500-900-0.5-2.0-skill_and_difficulty.out -l ${OUTDIR}/")

# EXP_NAMES+=("exp21-relaxed-500-900")
# EXP_NAMES+=("exp22-relaxed-500-900")
# EXP_NAMES+=("exp23-relaxed-500-900")
# EXP_NAMES+=("exp24-relaxed-500-900")
# EXP_NAMES+=("exp25-relaxed-500-900")

# EXP_NAMES+=("exp21-affinity-500-900")
# EXP_NAMES+=("exp22-affinity-500-900")
# EXP_NAMES+=("exp23-affinity-500-900")
# EXP_NAMES+=("exp24-affinity-500-900")
# EXP_NAMES+=("exp25-affinity-500-900")

# EXP_NAMES+=("exp21-complete_relax-500-900")
# EXP_NAMES+=("exp22-complete_relax-500-900")
# EXP_NAMES+=("exp23-complete_relax-500-900")
# EXP_NAMES+=("exp24-complete_relax-500-900")
# EXP_NAMES+=("exp25-complete_relax-500-900")

# EXP_NAMES+=("exp21-makespan-500-900")
# EXP_NAMES+=("exp22-makespan-500-900")
# EXP_NAMES+=("exp23-makespan-500-900")
# EXP_NAMES+=("exp24-makespan-500-900")
# EXP_NAMES+=("exp25-makespan-500-900")

# #############################
# # SKILL BASED INTEGER EXPERIMENTS (OLD)
# #############################
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp11-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp12-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp13-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp14-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'relaxed' -f ./weights/exp15-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp11-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp12-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp13-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp14-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'affinity' -f ./weights/exp15-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp11-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp12-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp13-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp14-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'complete-relax' -f ./weights/exp15-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp11-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp12-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp13-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp14-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")
# EXPERIMENTS+=("500 900 3 6 'makespan' -f ./weights/exp15-500-900-0.5-2.0-integer.out -l ${OUTDIR}/")

# EXP_NAMES+=("exp11-relaxed-500-900")
# EXP_NAMES+=("exp12-relaxed-500-900")
# EXP_NAMES+=("exp13-relaxed-500-900")
# EXP_NAMES+=("exp14-relaxed-500-900")
# EXP_NAMES+=("exp15-relaxed-500-900")

# EXP_NAMES+=("exp11-affinity-500-900")
# EXP_NAMES+=("exp12-affinity-500-900")
# EXP_NAMES+=("exp13-affinity-500-900")
# EXP_NAMES+=("exp14-affinity-500-900")
# EXP_NAMES+=("exp15-affinity-500-900")

# EXP_NAMES+=("exp11-complete_relax-500-900")
# EXP_NAMES+=("exp12-complete_relax-500-900")
# EXP_NAMES+=("exp13-complete_relax-500-900")
# EXP_NAMES+=("exp14-complete_relax-500-900")
# EXP_NAMES+=("exp15-complete_relax-500-900")

# EXP_NAMES+=("exp11-makespan-500-900")
# EXP_NAMES+=("exp12-makespan-500-900")
# EXP_NAMES+=("exp13-makespan-500-900")
# EXP_NAMES+=("exp14-makespan-500-900")
# EXP_NAMES+=("exp15-makespan-500-900")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
