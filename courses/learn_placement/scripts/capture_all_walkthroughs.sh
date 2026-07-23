#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning
for m in \
  module01-01-hpwl-metrics \
  module01-03-net-models \
  module02-01-force-directed-place \
  module02-03-quadratic-place \
  module02-05-analytical-place \
  module02-07-sa-placement \
  module03-01-density-bins \
  module03-03-spread-legalize-lite \
  module04-01-timing-driven-place
do
  echo "=== $m ==="
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
    "courses/learn_placement/$m" --inject-transcript
done
echo CAPTURE_OK
ls courses/learn_placement/module*/assets/steps/*.png | wc -l
