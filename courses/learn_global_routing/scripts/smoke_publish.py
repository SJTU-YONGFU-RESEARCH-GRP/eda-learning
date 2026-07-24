#!/usr/bin/env python3
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[3]
cat = json.loads((ROOT / "platform/assets/catalog.json").read_text(encoding="utf-8"))
x = next(c for c in cat["courses"] if c["id"] == "learn_global_routing")
print("status", x["status"])
print("labs", len(x["labs"]))
print("shipped", sum(1 for l in x["labs"] if l["status"] == "shipped"))
print("media", sum(1 for l in x["labs"] if l["media"]["video"] and l["media"]["pdf"]))
vids = list((ROOT / "courses/learn_global_routing").glob("module*/video.mp4"))
print("video_files", len(vids))
for path in (
    "http://127.0.0.1:8080/courses/learn_global_routing/",
    "http://127.0.0.1:8080/courses/learn_global_routing/labs/pattern-l-route/",
    "http://127.0.0.1:8080/tools/pattern-l-route/",
):
    try:
        with urlopen(path, timeout=5) as r:
            print(path, r.status)
    except Exception as e:
        print(path, "ERR", e)
