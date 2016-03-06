#!/bin/bash

TIME=`(date +%Y%m%d%H%M%S)`

BASE_LOG_DIR="/home/akobren/akobren-on-canvas/software/repos/git/lp-ir/logs/"
EXPERIMENT_FILE="/home/akobren/akobren-on-canvas/software/repos/git/lp-ir/src/exps/SeqIncreaseMake.py"
OUTDIR="${BASE_LOG_DIR}/${TIME}"

mkdir -p $OUTDIR

EXPERIMENTS=()
EXP_NAMES=()
# usage: SeqIncreaseMake.py [-h] rev_max pap_revs weight_file step
"python SeqIncreaseMake.py 3 3 ../../data/train/200-200-2.0-5.0-skill_based/weights.txt 0.5"
#############################
# SKILL BASED EXPERIMENTS
#############################
EXPERIMENTS+=("5 5 ../../data/train/100-100-1.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/100-100-2.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/100-100-3.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/100-100-4.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/100-100-5.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/100-100-6.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/100-100-7.0-7.0-skill_based/weights.txt 0.1")

EXPERIMENTS+=("5 5 ../../data/train/200-200-1.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/200-200-2.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/200-200-3.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/200-200-4.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/200-200-5.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/200-200-6.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/200-200-7.0-7.0-skill_based/weights.txt 0.1")

EXPERIMENTS+=("5 5 ../../data/train/300-300-1.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/300-300-2.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/300-300-3.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/300-300-4.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/300-300-5.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/300-300-6.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/300-300-7.0-7.0-skill_based/weights.txt 0.1")

EXPERIMENTS+=("5 5 ../../data/train/400-400-1.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/400-400-2.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/400-400-3.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/400-400-4.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/400-400-5.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/400-400-6.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/400-400-7.0-7.0-skill_based/weights.txt 0.1")

EXPERIMENTS+=("5 5 ../../data/train/500-500-1.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/500-500-2.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/500-500-3.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/500-500-4.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/500-500-5.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/500-500-6.0-7.0-skill_based/weights.txt 0.1")
EXPERIMENTS+=("5 5 ../../data/train/500-500-7.0-7.0-skill_based/weights.txt 0.1")

EXP_NAMES+=("sim100-100-1-7")
EXP_NAMES+=("sim100-100-2-7")
EXP_NAMES+=("sim100-100-3-7")
EXP_NAMES+=("sim100-100-4-7")
EXP_NAMES+=("sim100-100-5-7")
EXP_NAMES+=("sim100-100-6-7")
EXP_NAMES+=("sim100-100-7-7")

EXP_NAMES+=("sim200-200-1-7")
EXP_NAMES+=("sim200-200-2-7")
EXP_NAMES+=("sim200-200-3-7")
EXP_NAMES+=("sim200-200-4-7")
EXP_NAMES+=("sim200-200-5-7")
EXP_NAMES+=("sim200-200-6-7")
EXP_NAMES+=("sim200-200-7-7")

EXP_NAMES+=("sim300-300-1-7")
EXP_NAMES+=("sim300-300-2-7")
EXP_NAMES+=("sim300-300-3-7")
EXP_NAMES+=("sim300-300-4-7")
EXP_NAMES+=("sim300-300-5-7")
EXP_NAMES+=("sim300-300-6-7")
EXP_NAMES+=("sim300-300-7-7")

EXP_NAMES+=("sim400-400-1-7")
EXP_NAMES+=("sim400-400-2-7")
EXP_NAMES+=("sim400-400-3-7")
EXP_NAMES+=("sim400-400-4-7")
EXP_NAMES+=("sim400-400-5-7")
EXP_NAMES+=("sim400-400-6-7")
EXP_NAMES+=("sim400-400-7-7")

EXP_NAMES+=("sim500-500-1-7")
EXP_NAMES+=("sim500-500-2-7")
EXP_NAMES+=("sim500-500-3-7")
EXP_NAMES+=("sim500-500-4-7")
EXP_NAMES+=("sim500-500-5-7")
EXP_NAMES+=("sim500-500-6-7")
EXP_NAMES+=("sim500-500-7-7")

for ((i = 0; i < ${#EXPERIMENTS[@]}; i++))
do
    echo "/share/apps/python-2.7.10/bin/python2.7 ${EXPERIMENT_FILE} ${EXPERIMENTS[$i]}" | qsub -V -cwd  -j y -o ${OUTDIR}/${EXP_NAMES[$i]}".log" -l mem_token=10G  -N ${EXP_NAMES[$i]}  -S /bin/sh
done

echo "[done.]"
