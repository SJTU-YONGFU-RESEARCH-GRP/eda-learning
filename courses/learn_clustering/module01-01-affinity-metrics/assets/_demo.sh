#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
echo "== affinity modes =="
python common/solvers.py module01-01-affinity-metrics/examples/tiny_graph.json --mode affinity
