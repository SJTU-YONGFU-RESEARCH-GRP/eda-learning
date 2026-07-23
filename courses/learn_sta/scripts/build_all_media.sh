#!/usr/bin/env bash
# Build PPTX → PDF → audio → video for all learn_sta modules (Unix/WSL only).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SKILL="$ROOT/.cursor/skills/module-slides/scripts"
# shellcheck source=/dev/null
source "$SKILL/_require_unix.sh"

COURSE="$ROOT/courses/learn_sta"
NO_VIDEO=0
if [[ "${1:-}" == "--no-video" ]]; then NO_VIDEO=1; fi

mapfile -t MODS < <(find "$COURSE" -maxdepth 1 -type d -name 'module*' | sort)
echo "Modules: ${#MODS[@]}"
for d in "${MODS[@]}"; do
  echo "=== $(basename "$d") ==="
  python3 "$SKILL/transcript_to_outline.py" "$d"
  python3 "$SKILL/build_pptx.py" "$d"
  bash "$SKILL/pptx_to_pdf.sh" "$d/slides.pptx" || true
  if [[ "$NO_VIDEO" -eq 1 ]]; then
    bash "$SKILL/synthesize_audio.sh" "$d" || true
  else
    bash "$SKILL/narrate_clips.sh" "$d" || true
  fi
done
echo "Done. Publish: python3 platform/scripts/publish_course_platform.py learn_sta"
