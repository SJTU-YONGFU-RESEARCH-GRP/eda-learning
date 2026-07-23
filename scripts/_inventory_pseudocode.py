#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / "courses"
SKIP = re.compile(r"module00-|module99-|offline", re.I)

for cid in ["learn_sta", "learn_partitioning", "learn_floorplanning", "learn_placement"]:
    print("===", cid, "===")
    for ex in sorted((ROOT / cid).glob("module*/EXAMPLES.md")):
        mid = ex.parent.name
        if SKIP.search(mid):
            continue
        text = ex.read_text(encoding="utf-8")
        has = "## Pseudocode" in text
        tr = ex.parent / "transcript.md"
        fences = 0
        slide2 = "?"
        if tr.exists():
            tt = tr.read_text(encoding="utf-8")
            fences = len(re.findall(r"^```", tt, re.M)) // 2
            m = re.search(r"^## Slide 2 — (.+)$", tt, re.M)
            slide2 = m.group(1) if m else "?"
        print(f"  {mid} ps={has} fences={fences} slide2={slide2!r}")
