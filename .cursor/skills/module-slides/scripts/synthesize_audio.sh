#!/usr/bin/env bash
# Synthesize TTS audio from transcript.md using edge-tts.
# Prefer a part dir: lectures/chapterN/parts/part-NN-slug
# Must run in Unix or WSL.
#
# Only narration PROSE is spoken. Never spoken:
#   - the H1 title line
#   - metadata lines (**Clip id:**, **Estimated duration:**, **Sources:** ...)
#   - "## Slide N — ..." headings (visual anchors for authors, not narration)
# File paths and symbols are rewritten into listener-friendly words.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/_require_unix.sh"

CHAPTER_DIR="${1:-}"
VOICE="${VOICE:-en-US-JennyNeural}"

if [[ -z "${CHAPTER_DIR}" ]]; then
  echo "Usage: $0 lectures/chapterN/parts/part-NN-slug" >&2
  exit 1
fi

CHAPTER_DIR="$(cd "${CHAPTER_DIR}" && pwd)"
TRANSCRIPT="${CHAPTER_DIR}/transcript.md"
AUDIO_DIR="${CHAPTER_DIR}/audio"
FULL_AUDIO="${AUDIO_DIR}/full.mp3"

if [[ ! -f "${TRANSCRIPT}" ]]; then
  echo "Missing transcript: ${TRANSCRIPT}" >&2
  exit 1
fi

if ! command -v edge-tts >/dev/null 2>&1; then
  echo "edge-tts not found. Install with: pip install edge-tts" >&2
  exit 1
fi

mkdir -p "${AUDIO_DIR}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPEECH="$(mktemp)"
trap 'rm -f "${SPEECH}"' EXIT

python3 "${SCRIPT_DIR}/transcript_to_speech.py" "${TRANSCRIPT}" "${SPEECH}"

edge-tts --voice "${VOICE}" --file "${SPEECH}" --write-media "${FULL_AUDIO}"
echo "Wrote ${FULL_AUDIO}"
