#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
echo "== capacity 3 =="
python common/solvers.py "module01-05-size-constrained-agglomerative/examples/tiny_graph.json" --k 2 --capacity 3
echo "== capacity 2 =="
python common/solvers.py "module01-05-size-constrained-agglomerative/examples/tiny_graph.json" --k 2 --capacity 2
