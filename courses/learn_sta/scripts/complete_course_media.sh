#!/usr/bin/env bash
# Capture STA walkthroughs + inject transcripts, then build all media (Unix/WSL).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
SKILL="$ROOT/.cursor/skills/module-slides/scripts"
# shellcheck source=/dev/null
source "$SKILL/_require_unix.sh"

LABS=(
  module01-01-timing-graph
  module01-03-arrival-required
  module02-01-slack-setup-hold
  module02-03-critical-path
  module03-01-incremental-update
  module03-03-false-multicycle-lite
)

echo "=== Capturing algorithm walkthroughs ==="
for m in "${LABS[@]}"; do
  echo "--- $m ---"
  python3 "$SKILL/capture_algorithm_walkthrough.py" \
    "courses/learn_sta/$m" --inject-transcript
done

echo "=== Building all media ==="
bash courses/learn_sta/scripts/build_all_media.sh

echo "=== Publish ==="
python3 platform/scripts/publish_course_platform.py learn_sta
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/learn_sta --modules

echo "DONE learn_sta"
