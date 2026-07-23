#!/usr/bin/env bash
# Sync slides from transcript, rebuild PPTX/PDF, per-slide TTS, and narrated MP4.
# Accepts module-slides dirs (courses/.../moduleNN-slug) or legacy part-* dirs.
# Must run in Unix or WSL (not Windows PowerShell / cmd).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/_require_unix.sh"

VOICE="${VOICE:-en-US-JennyNeural}"

usage() {
  echo "Usage: $0 courses/<course>/moduleNN-slug [more module dirs...]" >&2
  echo "   or: $0 --course-dir courses/<course>   # all moduleNN-* dirs" >&2
  echo "   or: $0 --chapter-dir lectures/chapterN  # legacy parts/" >&2
  exit 1
}

resolve_pptx() {
  local d="$1"
  if [[ -f "$d/slides.pptx" ]]; then
    echo "$d/slides.pptx"
  elif [[ -f "$d/clip.pptx" ]]; then
    echo "$d/clip.pptx"
  else
    echo ""
  fi
}

CLIPS=()
if [[ "${1:-}" == "--course-dir" ]]; then
  [[ -n "${2:-}" ]] || usage
  COURSE_DIR="$(cd "$2" && pwd)"
  while IFS= read -r -d '' d; do
    CLIPS+=("$d")
  done < <(find "$COURSE_DIR" -mindepth 1 -maxdepth 1 -type d -name 'module*' -print0 2>/dev/null | sort -z)
elif [[ "${1:-}" == "--chapter-dir" ]]; then
  [[ -n "${2:-}" ]] || usage
  CHAPTER_DIR="$(cd "$2" && pwd)"
  while IFS= read -r -d '' d; do
    CLIPS+=("$d")
  done < <(find "$CHAPTER_DIR/parts" -mindepth 1 -maxdepth 1 -type d -name 'part-*' -print0 2>/dev/null | sort -z)
else
  [[ $# -ge 1 ]] || usage
  for arg in "$@"; do
    CLIPS+=("$(cd "$arg" && pwd)")
  done
fi

[[ ${#CLIPS[@]} -gt 0 ]] || { echo "No module/part directories found." >&2; exit 1; }

if ! command -v edge-tts >/dev/null 2>&1; then
  python3 -m pip install -q edge-tts
fi

for clip in "${CLIPS[@]}"; do
  echo
  echo "======== $(basename "$clip") ========"
  if [[ ! -f "$clip/transcript.md" ]]; then
    echo "SKIP: no transcript.md in $clip" >&2
    continue
  fi
  python3 "${SCRIPT_DIR}/transcript_to_outline.py" "$clip"
  python3 "${SCRIPT_DIR}/build_pptx.py" "$clip"
  python3 "${SCRIPT_DIR}/verify_transcript_consistency.py" "$clip"
  PPTX="$(resolve_pptx "$clip")"
  if [[ -z "$PPTX" ]]; then
    echo "ERROR: no slides.pptx or clip.pptx in $clip" >&2
    exit 1
  fi
  bash "${SCRIPT_DIR}/pptx_to_pdf.sh" "$PPTX"
  python3 "${SCRIPT_DIR}/synthesize_audio.py" "$clip" --voice "$VOICE"
  bash "${SCRIPT_DIR}/build_video.sh" --target-dir "$clip"
done

echo
echo "Done: ${#CLIPS[@]} module/part(s) synced and narrated."
