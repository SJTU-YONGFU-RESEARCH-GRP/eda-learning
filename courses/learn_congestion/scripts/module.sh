#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
KEY="${1:-}"
shift || true
if [[ -z "$KEY" || "$KEY" == "--help" ]]; then
  echo "Usage: $0 SS-AA [--check|--demo|--help]"
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
    [[ -f "$MOD_DIR/EXAMPLES.md" ]] && echo "[OK] EXAMPLES.md"
    [[ -f "$ROOT/common/tiny_cong.json" ]] && echo "[OK] common/tiny_cong.json"
    python3 -c "import sys; sys.path.insert(0,'$ROOT'); from common.solvers import rudy_demand; from common.congestionutil import load; print('[OK] solvers', rudy_demand(load('$ROOT/common/tiny_cong.json')['placement'], load('$ROOT/common/tiny_cong.json')) is not None)"
    ;;
  --demo)
    echo "Demo: open $MOD_DIR/EXAMPLES.md"
    ;;
  *)
    echo "Unknown option: $ACTION"; exit 1
    ;;
esac
