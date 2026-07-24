#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning
for m in \
  module01-01-routing-grid \
  module01-03-pin-access \
  module02-01-lee-maze \
  module02-03-astar-route \
  module02-05-track-usage \
  module02-07-via-assignment \
  module03-01-drc-spacing \
  module03-03-ripup-detailed \
  module04-01-sequential-detailed
do
  echo "=== $m ==="
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
    "courses/learn_routing/$m" --inject-transcript
done
echo CAPTURE_OK
