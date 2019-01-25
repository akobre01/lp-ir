#!/bin/bash

set -exu

CONFIG=$1

# Run the basic lp formulation of paper matching.
# Don't worry: the irdalb is misnamed and can handle lb or not.
python -m src.exps.irdalb $CONFIG

exit