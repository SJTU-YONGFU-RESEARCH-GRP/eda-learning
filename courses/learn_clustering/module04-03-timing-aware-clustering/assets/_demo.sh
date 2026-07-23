#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
python common/solvers.py module04-03-timing-aware-clustering/examples/tiny_graph.json --mode timing --seed module02-05-kernighan-lin/examples/seed_partition.json --crit module04-03-timing-aware-clustering/examples/criticality.json
