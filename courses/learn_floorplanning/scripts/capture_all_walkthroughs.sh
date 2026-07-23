#!/usr/bin/env bash
# Capture floorplanning walkthrough frames + inject transcripts (Unix/WSL).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SKILL="$ROOT/.cursor/skills/module-slides/scripts"
COURSE="$ROOT/courses/learn_floorplanning"
cd "$ROOT"

MODS=(
  module01-01-fixed-outline
  module01-03-area-deadspace
  module02-01-slicing-floorplan
  module02-03-bstar-tree
  module02-05-sequence-pair
  module03-01-simulated-annealing-fp
  module03-03-soft-module-sizing
  module03-05-macro-placement
  module04-01-hierarchical-floorplan
  module04-03-pin-assignment
)

for m in "${MODS[@]}"; do
  echo "===== $m ====="
  python3 "$SKILL/capture_algorithm_walkthrough.py" \
    "$COURSE/$m" --inject-transcript
done
echo "ALL_CAPTURE_OK"
