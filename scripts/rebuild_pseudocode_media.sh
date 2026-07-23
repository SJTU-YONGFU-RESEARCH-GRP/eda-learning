#!/usr/bin/env bash
# Sync outline/pptx/verify for labs that have Algorithm sketch fences, then narrate.
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning

# Normalize CRLF on skill shell scripts
python3 - <<'PY'
from pathlib import Path
for p in Path(".cursor/skills/module-slides/scripts").glob("*.sh"):
    b = p.read_bytes()
    nb = b.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if nb != b:
        p.write_bytes(nb)
PY

COURSES=(learn_sta learn_partitioning learn_floorplanning learn_placement)

for c in "${COURSES[@]}"; do
  echo "======== SYNC $c ========"
  for tr in courses/"$c"/module*/transcript.md; do
    m=$(dirname "$tr")
    if grep -q '## Slide .* — Algorithm sketch' "$tr"; then
      echo "-- $m"
      python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py "$m"
      python3 .cursor/skills/module-slides/scripts/build_pptx.py "$m"
      python3 .cursor/skills/module-slides/scripts/verify_transcript_consistency.py "$m"
      bash .cursor/skills/module-slides/scripts/pptx_to_pdf.sh "$m/slides.pptx"
    fi
  done
  echo "======== NARRATE $c ========"
  bash .cursor/skills/module-slides/scripts/narrate_clips.sh --course-dir "courses/$c"
done

echo ALL_COURSES_DONE
