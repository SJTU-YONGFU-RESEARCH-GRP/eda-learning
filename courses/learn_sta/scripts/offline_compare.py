#!/usr/bin/env python3
"""Offline harness: compare toy STA metrics on the shared tiny netlist."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "common"))

from propagate import (  # noqa: E402
    PROP_GOLDENS,
    critical_path_to,
    propagate_arrival,
    propagate_required,
    setup_slack,
)
from timing_io import load_timing  # noqa: E402


def main() -> int:
    t = load_timing(ROOT / "common" / "tiny_timing.json")
    arr = propagate_arrival(t)
    req = propagate_required(t)
    assert arr and req
    slack = setup_slack(arr, req, "out")
    path = critical_path_to(t, arr, "out")
    report = {
        "instance": t.get("name"),
        "A_out": arr["out"],
        "R_out": req["out"],
        "setup_slack_out": slack,
        "critical_path": path,
        "golden_slack": PROP_GOLDENS["setup_slack_out"],
        "match_golden": abs((slack or 0) - PROP_GOLDENS["setup_slack_out"]) < 1e-9,
        "external_timer": None,
        "notes": "Plug an open timer here when available; until then validate toy goldens.",
    }
    out = ROOT / "module05-01-offline-benchmark-compare" / "examples" / "compare_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"wrote {out}")
    return 0 if report["match_golden"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
