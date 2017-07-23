#!/bin/bash

set -exu

ASSIGNMENT=$1
AFFS=$2
COVERAGE=3

# Plot the histogram of paper scores.
python -m src.plotting.plot_aff_hists $ASSIGNMENT $AFFS $COVERAGE

echo "[done.]"