#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
python common/solvers.py module02-01-label-propagation/examples/tiny_graph.json --mode lp
