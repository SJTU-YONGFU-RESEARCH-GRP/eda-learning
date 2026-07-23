#!/usr/bin/env bash
# Capture a lab UI snapshot for module-slides (wraps capture_lab_snapshot.py).
# Must run in Unix or WSL (Playwright Chromium).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/_require_unix.sh"
exec "${PYTHON}" "${SCRIPT_DIR}/capture_lab_snapshot.py" "$@"
