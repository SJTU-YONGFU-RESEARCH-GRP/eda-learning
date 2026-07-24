#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning
for m in \
  module01-01-routing-graph \
  module01-03-terminal-gcells \
  module02-01-pattern-l-route \
  module02-03-pattern-z-route \
  module02-05-maze-gcell-route \
  module02-07-multipin-tree \
  module03-01-edge-overflow \
  module03-03-ripup-reroute \
  module04-01-sequential-global
do
  echo "=== $m ==="
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
    "courses/learn_global_routing/$m" --inject-transcript
done
echo CAPTURE_OK
