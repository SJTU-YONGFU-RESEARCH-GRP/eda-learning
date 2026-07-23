#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
python common/solvers.py module03-01-multilevel-clustering/examples/tiny_graph.json --mode multilevel
