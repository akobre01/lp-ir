#!/bin/bash

set -exu

CONFIG=$1

# Run the basic lp formulation of paper matching.
python -m src.exps.ir $CONFIG

exit