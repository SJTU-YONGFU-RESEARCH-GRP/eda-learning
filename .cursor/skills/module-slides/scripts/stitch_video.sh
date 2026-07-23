#!/usr/bin/env bash
# Stitch a short clip video: title card + clip audio (ffmpeg).
# Pass a module or part directory. Prefer build_video.sh for slide-timed frames.
set -euo pipefail

TARGET_DIR="${1:-}"
if [[ -z "${TARGET_DIR}" ]]; then
  echo "Usage: $0 courses/<course>/moduleNN-slug" >&2
  echo "   or: $0 lectures/chapterN/parts/part-NN-slug" >&2
  exit 1
fi

TARGET_DIR="$(cd "${TARGET_DIR}" && pwd)"
NAME="$(basename "${TARGET_DIR}")"
AUDIO="${TARGET_DIR}/audio/full.mp3"
SLIDES="${TARGET_DIR}/slides.md"
OUT="${TARGET_DIR}/video.mp4"

if [[ ! -f "${AUDIO}" ]]; then
  echo "Missing audio: ${AUDIO} (run synthesize_audio.sh first)" >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found on PATH" >&2
  exit 1
fi

if [[ "${NAME}" =~ ^chapter[0-9]+$ ]]; then
  echo "Warning: chapter-level video is legacy; prefer per-module videos." >&2
fi

TITLE="${NAME}"
if [[ -f "${SLIDES}" ]]; then
  TITLE="$(grep -m1 -E '^title:' "${SLIDES}" | sed 's/^title:[[:space:]]*//' || true)"
  [[ -z "${TITLE}" ]] && TITLE="${NAME}"
fi

# Escape drawtext-hostile characters lightly
SAFE_TITLE="${TITLE//:/ -}"
SAFE_TITLE="${SAFE_TITLE//\'/’}"

ffmpeg -y \
  -f lavfi -i "color=c=0x1a1a2e:s=1920x1080:d=1" \
  -i "${AUDIO}" \
  -vf "drawtext=text='${SAFE_TITLE}':fontcolor=white:fontsize=42:x=(w-text_w)/2:y=(h-text_h)/2" \
  -shortest -c:v libx264 -tune stillimage -c:a aac -pix_fmt yuv420p \
  "${OUT}"

echo "Wrote ${OUT}"
echo "Note: title-card + audio stub for a short clip. Prefer build_video.sh for slide-timed frames."
