#!/bin/bash/env bash

set -exu

COVERAGE=3.0

for ms in {0.0..${COVERAGE}..0.5}
    do
        srun ./run_mmbb_single ${ms}
done

echo "[done.]"