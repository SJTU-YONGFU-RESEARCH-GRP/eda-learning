#!/usr/bin/env bash
# Hierarchical module helper: ./scripts/module.sh SS-AA [--check|--demo|--help]
# Examples: ./scripts/module.sh 01-03 --check
#           ./scripts/module.sh 02-05 --demo
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
KEY="${1:-}"
shift || true
if [[ -z "$KEY" || "$KEY" == "--help" ]]; then
  echo "Usage: $0 SS-AA [--check|--demo|--help]"
  echo "  SS-AA matches moduleSS-AA-* (e.g. 01-03, 02-05, 99-00)"
  exit 0
fi
MOD_DIR="$(find "$ROOT" -maxdepth 1 -type d -name "module${KEY}-*" | head -1)"
if [[ -z "$MOD_DIR" ]]; then
  echo "No module directory for module${KEY}-*"
  exit 1
fi
ACTION="${1:---check}"
case "$ACTION" in
  --check)
    echo "Module $KEY self-check (Track A)"
    echo "Module dir: $MOD_DIR"
    command -v bash >/dev/null && echo "[OK] bash"
    [[ -f "$MOD_DIR/EXAMPLES.md" ]] && echo "[OK] EXAMPLES.md" || echo "[INFO] no EXAMPLES.md"
    [[ -f "$MOD_DIR/CHECKLIST.md" ]] && echo "[OK] CHECKLIST.md"
    [[ -f "$MOD_DIR/transcript.md" ]] && echo "[OK] transcript.md"
    [[ -f "$MOD_DIR/examples/tiny_legal.json" ]] && echo "[OK] examples/tiny_legal.json" || echo "[INFO] no examples/tiny_legal.json"
    echo "[INFO] Track B lab link is in README.md"
    echo "[INFO] --check placeholder: implement goldens when solvers land"
    ;;
  --demo)
    echo "Demo: open $MOD_DIR/EXAMPLES.md and README.md"
    ;;
  *)
    echo "Unknown option: $ACTION"
    exit 1
    ;;
esac
