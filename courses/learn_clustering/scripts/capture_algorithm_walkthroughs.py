#!/usr/bin/env python3
"""Thin wrapper: prefer the module-slides skill capture script.

  python courses/learn_clustering/scripts/capture_algorithm_walkthroughs.py
  python courses/learn_clustering/scripts/capture_algorithm_walkthroughs.py --algo kernighan-lin
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / ".cursor" / "skills" / "module-slides" / "scripts" / "capture_algorithm_walkthrough.py"

MODULES = [
    "module01-01-affinity-metrics",
    "module01-03-greedy-pair-merge",
    "module01-05-size-constrained-agglomerative",
    "module02-01-label-propagation",
    "module02-03-spectral-bisection",
    "module02-05-kernighan-lin",
    "module02-07-fiduccia-mattheyses",
    "module03-01-multilevel-clustering",
    "module03-03-hypergraph-clustering",
    "module04-01-congestion-aware-clustering",
    "module04-03-timing-aware-clustering",
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--algo", help="Limit to one lab/algo id")
    ap.add_argument("--inject-transcript", action="store_true")
    ap.add_argument("--skip-capture", action="store_true")
    args = ap.parse_args()
    if not SKILL.is_file():
        print(f"missing skill script: {SKILL}", file=sys.stderr)
        return 1

    course = ROOT / "courses" / "learn_clustering"
    mods = MODULES
    if args.algo:
        mods = [m for m in MODULES if args.algo in m or m.endswith(args.algo)]
        # also match by lab slug substring
        if not mods:
            mods = [m for m in MODULES if args.algo.replace("_", "-") in m]

    rc = 0
    for name in mods:
        cmd = [sys.executable, str(SKILL), str(course / name)]
        if args.inject_transcript:
            cmd.append("--inject-transcript")
        if args.skip_capture:
            cmd.append("--skip-capture")
        if args.algo:
            cmd.extend(["--algo", args.algo])
        print("+", " ".join(cmd))
        r = subprocess.call(cmd)
        if r != 0:
            rc = r
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
