#!/usr/bin/env bash
# Convert a module-slides PPTX to PDF using LibreOffice/soffice.
# Must run in Unix or WSL.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/_require_unix.sh"

usage() {
  echo "Usage: $0 <path/to/clip-or-chapter.pptx> [output.pdf]" >&2
  exit 1
}

[[ $# -ge 1 ]] || usage

PPTX="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
[[ -f "$PPTX" ]] || { echo "ERROR: not found: $PPTX" >&2; exit 1; }

OUT_DIR="$(dirname "$PPTX")"
if [[ $# -ge 2 ]]; then
  PDF="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
else
  PDF="${PPTX%.pptx}.pdf"
fi

WORK_DIR="/tmp/book_slides_pdf_$$"
WORK_PPTX="$WORK_DIR/$(basename "$PPTX")"
mkdir -p "$WORK_DIR"
cp -f "$PPTX" "$WORK_PPTX"

cleanup() {
  rm -rf "$WORK_DIR"
}
trap cleanup EXIT

convert_with() {
  local bin="$1"
  echo "Converting with $bin ..."
  "$bin" --headless --nologo --nofirststartwizard --convert-to pdf \
    --outdir "$WORK_DIR" "$WORK_PPTX"
}

if command -v soffice >/dev/null 2>&1; then
  convert_with soffice
elif command -v libreoffice >/dev/null 2>&1; then
  convert_with libreoffice
elif command -v unoconv >/dev/null 2>&1; then
  unoconv -f pdf -o "$PDF" "$PPTX"
else
  echo "ERROR: install LibreOffice (soffice/libreoffice) or unoconv for pptx -> pdf" >&2
  echo "HINT (Ubuntu/WSL): sudo apt install libreoffice-impress default-jre-headless" >&2
  exit 1
fi

GENERATED="$WORK_DIR/$(basename "$WORK_PPTX" .pptx).pdf"
if [[ -f "$GENERATED" ]]; then
  mkdir -p "$(dirname "$PDF")"
  cp -f "$GENERATED" "$PDF"
fi

[[ -f "$PDF" ]] || {
  echo "ERROR: PDF not created at $PDF" >&2
  exit 1
}

echo "OK: $PDF ($(wc -c <"$PDF") bytes)"
