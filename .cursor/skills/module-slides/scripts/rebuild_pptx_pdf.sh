#!/usr/bin/env bash
# Rebuild all lecture PPTX (parts + chapter decks), then export PDFs.
# Does NOT regenerate audio/video.
set -euo pipefail
cd /mnt/d/Thumbdrive/Papers/Fundamental-of-Dataset-Collection-Annotation-and-Management
SCRIPTS=".cursor/skills/module-slides/scripts"

echo "=== Rebuild all PPTX ==="
shopt -s nullglob
mapfile -t chapters < <(ls -d lectures/chapter[0-9]* | sort -V)
for ch in "${chapters[@]}"; do
  echo "--- $ch parts ---"
  for part in "$ch"/parts/part-*; do
    [[ -d "$part" ]] || continue
    [[ -f "$part/outline.yaml" ]] || continue
    python3 "$SCRIPTS/build_pptx.py" "$part"
  done
  echo "--- $ch chapter deck ---"
  python3 "$SCRIPTS/build_pptx.py" "$ch" --chapter-deck
done
echo "PPTX rebuild complete."

echo "=== Export all PDFs ==="
mapfile -t pptxs < <(find lectures -path 'lectures/chapter*/parts/*/clip.pptx' -o -path 'lectures/chapter*/chapter*.pptx' | sort -V)
for pptx in "${pptxs[@]}"; do
  echo "PDF: $pptx"
  bash "$SCRIPTS/pptx_to_pdf.sh" "$pptx"
done
echo "PDF export complete."
