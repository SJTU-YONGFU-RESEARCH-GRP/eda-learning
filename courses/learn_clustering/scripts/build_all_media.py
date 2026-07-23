#!/usr/bin/env python3
"""Forward to the WSL/Linux bash builder — do not run media on native Windows.

Canonical:
  bash courses/learn_clustering/scripts/build_all_media.sh
"""
from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path

BASH_SCRIPT = Path(__file__).resolve().with_name("build_all_media.sh")


def main() -> int:
    system = platform.system()
    if system == "Windows":
        print(
            "module-slides media must run in WSL or Linux, not Windows.\n"
            "Open a WSL shell and run:\n"
            "  bash courses/learn_clustering/scripts/build_all_media.sh\n"
            "Or:\n"
            "  wsl -e bash -lc 'cd /mnt/d/proj/designs/eda_learning && "
            "bash courses/learn_clustering/scripts/build_all_media.sh'",
            file=sys.stderr,
        )
        return 2
    if not BASH_SCRIPT.is_file():
        print(f"missing {BASH_SCRIPT}", file=sys.stderr)
        return 1
    return subprocess.call(["bash", str(BASH_SCRIPT), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
