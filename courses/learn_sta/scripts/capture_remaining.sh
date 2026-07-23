#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning
SKILL=.cursor/skills/module-slides/scripts
source "$SKILL/_require_unix.sh"

LABS=(
  module01-03-arrival-required
  module02-01-slack-setup-hold
  module02-03-critical-path
  module03-01-incremental-update
  module03-03-false-multicycle-lite
)

for m in "${LABS[@]}"; do
  echo "=== CAPTURE $m ==="
  python3 "$SKILL/capture_algorithm_walkthrough.py" \
    "courses/learn_sta/$m" --inject-transcript
done
echo "CAPTURE DONE"
