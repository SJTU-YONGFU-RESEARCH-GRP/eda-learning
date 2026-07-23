#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
python common/solvers.py module02-07-fiduccia-mattheyses/examples/tiny_graph.json --mode fm --seed module02-05-kernighan-lin/examples/seed_partition.json
