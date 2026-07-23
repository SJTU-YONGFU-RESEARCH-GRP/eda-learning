#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
python common/solvers.py "module01-03-greedy-pair-merge/examples/tiny_graph.json" --k 2
