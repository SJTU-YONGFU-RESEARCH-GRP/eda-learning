#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = (
    "Open EXAMPLES.md for this module and find the Pseudocode section—"
    "that written sketch is what you implement in the Track A solvers "
    "and what the browser challenges measure."
)
NEW = (
    "Open this module's examples file and find the Pseudocode section. "
    "That written sketch is what you implement on the implement track "
    "and what the browser challenges measure."
)

n = 0
for p in ROOT.glob("module*/transcript.md"):
    t = p.read_text(encoding="utf-8")
    if OLD in t:
        p.write_text(t.replace(OLD, NEW), encoding="utf-8", newline="\n")
        n += 1
print(f"fixed {n}")
