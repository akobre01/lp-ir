#!/usr/bin/env bash

export PM_ROOT=`pwd`
export PM_DATA_ROOT=$PM_ROOT/data

if [ ! -f $PM_ROOT/.gitignore ]; then
    echo ".gitignore" > $PM_ROOT/.gitignore
    echo "target" >> $PM_ROOT/.gitignore
    echo ".idea" >> $PM_ROOT/.gitignore
    echo "__pycache__" >> $PM_ROOT/.gitignore
fi

# Setup log dir
mkdir -p logs
mkdir -p logs/cvpr

module load gurobi/702
