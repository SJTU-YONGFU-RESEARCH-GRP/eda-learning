#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
echo "== Kernighan-Lin on bad seed =="
python common/solvers.py module02-05-kernighan-lin/examples/tiny_graph.json \
  --mode kl --seed module02-05-kernighan-lin/examples/seed_partition.json
