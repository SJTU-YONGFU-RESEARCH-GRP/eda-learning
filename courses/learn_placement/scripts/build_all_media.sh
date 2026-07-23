#!/usr/bin/env bash
# Build learn_placement media in WSL/Linux (canonical module-slides path).
#
# From repo root (WSL or Linux — not Windows):
#   bash courses/learn_placement/scripts/build_all_media.sh
#   bash courses/learn_placement/scripts/build_all_media.sh --pptx-only
#   bash courses/learn_placement/scripts/build_all_media.sh --no-video
#
# Requires: python3, soffice (LibreOffice), edge-tts; ffmpeg+pdftoppm for video.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ROOT="$(cd "${COURSE_DIR}/../.." && pwd)"
SKILL="${ROOT}/.cursor/skills/module-slides/scripts"

# shellcheck source=/dev/null
source "${SKILL}/_require_unix.sh"

DO_PPTX=1
DO_NARRATE=1
DO_VIDEO=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pptx-only) DO_NARRATE=0; DO_VIDEO=0 ;;
    --no-video) DO_VIDEO=0 ;;
    --help|-h)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown flag: $1" >&2
      exit 2
      ;;
  esac
  shift
done

cd "$ROOT"

if [[ ! -d "$SKILL" ]]; then
  echo "ERROR: missing skill scripts at $SKILL" >&2
  exit 1
fi

ALL=(
  module00-00-intro
  module01-01-hpwl-metrics
  module01-03-net-models
  module02-01-force-directed-place
  module02-03-quadratic-place
  module02-05-analytical-place
  module02-07-sa-placement
  module03-01-density-bins
  module03-03-spread-legalize-lite
  module04-01-timing-driven-place
  module05-01-offline-benchmark-compare
  module99-00-wrap
)

if [[ "$DO_PPTX" -eq 1 && "$DO_NARRATE" -eq 0 ]]; then
  echo "=== PPTX only ==="
  for m in "${ALL[@]}"; do
    d="${COURSE_DIR}/${m}"
    python3 "${SKILL}/transcript_to_outline.py" "$d"
    python3 "${SKILL}/build_pptx.py" "$d"
    python3 "${SKILL}/verify_transcript_consistency.py" "$d"
  done
fi

if [[ "$DO_NARRATE" -eq 1 ]]; then
  echo "=== Narrate (outline + PPTX + PDF + audio${DO_VIDEO:+ + video}) ==="
  if [[ "$DO_VIDEO" -eq 1 ]]; then
    bash "${SKILL}/narrate_clips.sh" --course-dir "$COURSE_DIR"
  else
    for m in "${ALL[@]}"; do
      d="${COURSE_DIR}/${m}"
      echo
      echo "======== ${m} ========"
      python3 "${SKILL}/transcript_to_outline.py" "$d"
      python3 "${SKILL}/build_pptx.py" "$d"
      python3 "${SKILL}/verify_transcript_consistency.py" "$d"
      pptx="$d/slides.pptx"
      [[ -f "$pptx" ]] || pptx="$d/clip.pptx"
      bash "${SKILL}/pptx_to_pdf.sh" "$pptx"
      python3 "${SKILL}/synthesize_audio.py" "$d" --voice "${VOICE:-en-US-JennyNeural}"
    done
  fi

  echo "=== Platform publish (catalog + course pages + course-media) ==="
  python3 "${ROOT}/platform/scripts/publish_course_platform.py" learn_placement
fi

echo
echo "Done (WSL). Course: $COURSE_DIR"
