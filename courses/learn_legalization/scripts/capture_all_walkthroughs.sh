#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning
for m in \
  module01-01-site-row-model \
  module01-03-legality-metrics \
  module02-01-greedy-snap \
  module02-03-overlap-removal \
  module02-05-abacus-row-pack \
  module02-07-tetris-row-pack \
  module03-01-fixed-macros \
  module03-03-displacement-hpwl \
  module04-01-detailed-vs-global
do
  echo "=== $m ==="
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
    "courses/learn_legalization/$m" --inject-transcript
done
echo CAPTURE_OK
ls courses/learn_legalization/module*/assets/steps/*.png 2>/dev/null | wc -l
