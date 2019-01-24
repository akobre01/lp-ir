#!/bin/bash

set -exu

CONFIG=$1

# Run pr4a paper matching.
python -m src.exps.pr4a $CONFIG

exit