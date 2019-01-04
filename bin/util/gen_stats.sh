#!/bin/bash

set -exu

CONFIG_DIR=$1

# Generate the statistics of the matching.
python -m src.utils.match_stats $CONFIG_DIR

exit