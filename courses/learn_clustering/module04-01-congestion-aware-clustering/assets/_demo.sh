#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
python common/solvers.py module04-01-congestion-aware-clustering/examples/tiny_graph.json --mode cong --seed module02-05-kernighan-lin/examples/seed_partition.json --cong module04-01-congestion-aware-clustering/examples/congestion.json --lambda 5
