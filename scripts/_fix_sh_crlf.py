#!/usr/bin/env python3
from pathlib import Path

paths = [
    Path("/mnt/d/proj/designs/eda_learning/scripts/rebuild_pseudocode_media.sh"),
    Path("/mnt/d/proj/designs/eda_learning/scripts/rebuild_placement_media.sh"),
]
paths.extend(Path("/mnt/d/proj/designs/eda_learning/scripts").glob("*.sh"))
paths.extend(Path("/mnt/d/proj/designs/eda_learning/.cursor/skills/module-slides/scripts").glob("*.sh"))
for p in paths:
    if not p.exists():
        continue
    b = p.read_bytes()
    nb = b.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if nb != b:
        p.write_bytes(nb)
        print("fixed", p)
    else:
        print("ok", p)
