#!/usr/bin/env bash

function join_by { local IFS="$1"; shift; echo "$*"; }

ARGS=`join_by ' ' $@`

python -m src.plotting.tex_table_from_json $ARGS

exit