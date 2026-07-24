#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning
SKILL=.cursor/skills/module-slides/scripts
for m in courses/learn_congestion/module*/; do
  base=$(basename "$m")
  case "$base" in
    module00-*|module05-*|module99-*) continue ;;
  esac
  echo "=== lab snap $base ==="
  python3 "$SKILL/capture_lab_snapshot.py" "$m" || true
done
python3 "$SKILL/capture_lab_snapshot.py" \
  courses/learn_congestion/module00-00-intro --lab index --name tools-index.png || true
echo LAB_SNAPS_OK
ls courses/learn_congestion/module*/assets/lab-starter.png 2>/dev/null | wc -l
