#!/usr/bin/env bash
# Require a real Unix environment (Linux, WSL, or macOS). Refuse native Windows shells.
# Sourced by module-slides bash entry points.
#
# Usage:  source "$(dirname "$0")/_require_unix.sh"

_ms_uname="$(uname -s 2>/dev/null || true)"
case "$_ms_uname" in
  Linux*|Darwin*)
    unset _ms_uname
    ;;
  MINGW*|MSYS*|CYGWIN*|Windows_NT*|*)
    echo "ERROR: module-slides media scripts must run in Unix or WSL, not Windows." >&2
    echo "  Open a WSL shell (or Linux/macOS), cd to the repo, then re-run." >&2
    echo "  Example:" >&2
    echo "    cd /mnt/d/proj/designs/eda_learning   # adjust path" >&2
    echo "    bash .cursor/skills/module-slides/scripts/narrate_clips.sh courses/<course>/moduleNN-slug" >&2
    unset _ms_uname
    return 2 2>/dev/null || exit 2
    ;;
esac

# Prefer python3 on Unix
if [[ -z "${PYTHON:-}" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
  elif command -v python >/dev/null 2>&1; then
    PYTHON=python
  else
    echo "ERROR: python3 not found. Install Python 3 in WSL/Linux." >&2
    return 2 2>/dev/null || exit 2
  fi
  export PYTHON
fi
