#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning
for m in \
  module01-01-cutsize-balance \
  module01-03-initial-bipartition \
  module02-01-kl-partition \
  module02-03-fm-partition \
  module02-05-spectral-partition \
  module02-07-recursive-bisection \
  module03-01-multiway-partition \
  module03-03-terminal-propagation \
  module03-05-hypergraph-partition \
  module04-01-multilevel-partition
do
  echo "=== $m ==="
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
    "courses/learn_partitioning/$m" --inject-transcript
done
echo CAPTURE_OK
ls courses/learn_partitioning/module*/assets/steps/*.png | wc -l
