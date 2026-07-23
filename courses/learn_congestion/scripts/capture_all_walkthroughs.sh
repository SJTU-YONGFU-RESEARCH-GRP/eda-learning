#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning
for m in \
  module01-01-gcell-grid \
  module01-03-capacity-demand \
  module02-01-rudy-estimate \
  module02-03-probabilistic-demand \
  module02-05-congestion-map \
  module02-07-overflow-metrics \
  module03-01-cell-inflator \
  module03-03-net-weighting \
  module04-01-placement-feedback
do
  echo "=== $m ==="
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
    "courses/learn_congestion/$m" --inject-transcript
done
echo CAPTURE_OK
