#!/usr/bin/env bash
# Build MP4 from a module-slides deck.
# Preferred path: PPTX -> PDF -> PNG frames -> MP4 so video matches the deck.
# Must run in Unix or WSL (ffmpeg + poppler).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/_require_unix.sh"

TARGET_DIR=""
SECONDS_PER_SLIDE=5
AUDIO=""
FPS=30
PDF_DPI=200
BURN_CAPTIONS=0

usage() {
  cat >&2 <<'EOF'
Usage: build_video.sh --target-dir DIR [--seconds-per-slide N] [--audio PATH]
                      [--fps N] [--pdf-dpi N] [--burn-captions]

DIR can be:
  courses/<course>/moduleNN-slug        -> video.mp4  (module-slides)
  lectures/chapterN/parts/part-NN-slug  -> video.mp4  (legacy)
  lectures/chapterN                     -> video.mp4 (avoid for new work)
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-dir) TARGET_DIR="$2"; shift 2 ;;
    --seconds-per-slide) SECONDS_PER_SLIDE="$2"; shift 2 ;;
    --audio) AUDIO="$2"; shift 2 ;;
    --fps) FPS="$2"; shift 2 ;;
    --pdf-dpi) PDF_DPI="$2"; shift 2 ;;
    --burn-captions) BURN_CAPTIONS=1; shift ;;
    *) usage ;;
  esac
done

[[ -n "$TARGET_DIR" ]] || usage
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"
NAME="$(basename "$TARGET_DIR")"

if [[ "$NAME" == module* ]]; then
  if [[ -f "$TARGET_DIR/slides.pptx" ]]; then
    PPTX="$TARGET_DIR/slides.pptx"
    PDF="$TARGET_DIR/slides.pdf"
  else
    PPTX="$TARGET_DIR/clip.pptx"
    PDF="$TARGET_DIR/clip.pdf"
  fi
  OUT="$TARGET_DIR/video.mp4"
elif [[ "$NAME" == part-* || "$NAME" == clip-* ]]; then
  PPTX="$TARGET_DIR/clip.pptx"
  PDF="$TARGET_DIR/clip.pdf"
  OUT="$TARGET_DIR/video.mp4"
elif [[ "$NAME" =~ ^chapter[0-9]+$ ]]; then
  PPTX="$TARGET_DIR/$NAME.pptx"
  PDF="$TARGET_DIR/$NAME.pdf"
  OUT="$TARGET_DIR/video.mp4"
  echo "Warning: chapter-level MP4 can be long; prefer per-module MP4 for learners." >&2
else
  echo "ERROR: target dir must be moduleNN-*, part-*, clip-*, or chapterN: $TARGET_DIR" >&2
  exit 1
fi

FRAMES="$TARGET_DIR/frames"
CAPTIONS="$TARGET_DIR/audio/captions.srt"
TIMINGS="$TARGET_DIR/audio/slide_timings.json"

[[ -f "$PPTX" ]] || { echo "ERROR: missing PPTX: $PPTX" >&2; exit 1; }

command -v ffmpeg >/dev/null 2>&1 || {
  echo "ERROR: ffmpeg required for MP4 generation" >&2
  echo "HINT (Ubuntu/WSL): sudo apt install ffmpeg" >&2
  exit 1
}
command -v pdftoppm >/dev/null 2>&1 || {
  echo "ERROR: pdftoppm required for PDF rasterization" >&2
  echo "HINT (Ubuntu/WSL): sudo apt install poppler-utils" >&2
  exit 1
}

if [[ -z "$AUDIO" && -f "$TARGET_DIR/audio/full.mp3" ]]; then
  AUDIO="$TARGET_DIR/audio/full.mp3"
fi

if [[ ! -f "$PDF" || "$PPTX" -nt "$PDF" ]]; then
  bash "$SCRIPT_DIR/pptx_to_pdf.sh" "$PPTX" "$PDF"
fi

rm -rf "$FRAMES"
mkdir -p "$FRAMES"
echo "Rasterizing $PDF at ${PDF_DPI} DPI ..."
pdftoppm -png -r "$PDF_DPI" "$PDF" "$FRAMES/slide"
mapfile -t PNGS < <(find "$FRAMES" -name 'slide-*.png' | sort -V)
[[ ${#PNGS[@]} -gt 0 ]] || { echo "ERROR: no frames produced from $PDF" >&2; exit 1; }

CONCAT="$FRAMES/concat.txt"
: >"$CONCAT"

if [[ -f "$TIMINGS" ]]; then
  echo "Using slide timings from $TIMINGS"
  python3 - "$TIMINGS" "${#PNGS[@]}" "$CONCAT" "${PNGS[@]}" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

timings_path = Path(sys.argv[1])
n = int(sys.argv[2])
concat_path = Path(sys.argv[3])
pngs = sys.argv[4:]
data = json.loads(timings_path.read_text(encoding="utf-8"))

durations = []
for row in data[:n]:
    durations.append(float(row.get("duration", row.get("duration_sec", 5))))
while len(durations) < n:
    durations.append(5.0)

with concat_path.open("w", encoding="utf-8") as f:
    for png, duration in zip(pngs, durations, strict=False):
        f.write(f"file '{png}'\n")
        f.write(f"duration {duration}\n")
    f.write(f"file '{pngs[-1]}'\n")
PY
else
  echo "Using fixed ${SECONDS_PER_SLIDE}s per slide"
  for png in "${PNGS[@]}"; do
    echo "file '$png'" >>"$CONCAT"
    echo "duration $SECONDS_PER_SLIDE" >>"$CONCAT"
  done
  echo "file '${PNGS[-1]}'" >>"$CONCAT"
fi

SILENT="$FRAMES/silent.mp4"
VF="scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p"
ffmpeg -y -f concat -safe 0 -i "$CONCAT" -vf "$VF" -r "$FPS" \
  -c:v libx264 -pix_fmt yuv420p "$SILENT"

if [[ -n "$AUDIO" && -f "$AUDIO" ]]; then
  echo "Muxing audio: $AUDIO"
  if [[ $BURN_CAPTIONS -eq 1 && -f "$CAPTIONS" ]]; then
    ffmpeg -y -i "$SILENT" -i "$AUDIO" \
      -vf "$VF,subtitles=${CAPTIONS//:/\\:}" \
      -map 0:v:0 -map 1:a:0 \
      -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k \
      -shortest -movflags +faststart "$OUT"
  else
    ffmpeg -y -i "$SILENT" -i "$AUDIO" \
      -map 0:v:0 -map 1:a:0 \
      -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k \
      -shortest -movflags +faststart "$OUT"
  fi
else
  cp -f "$SILENT" "$OUT"
  echo "WARN: no audio/full.mp3 provided; created silent video." >&2
fi

echo "OK: $OUT (${#PNGS[@]} slides)"
