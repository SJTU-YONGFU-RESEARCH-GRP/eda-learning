"""Load / save tiny timing JSON for learn_sta Track A."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, TypedDict


class Arc(TypedDict):
    from_: str  # stored as "from" in JSON
    to: str
    delay: float
    kind: str


def load_timing(path: Path | str) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    pins = data["pins"]
    arcs = [
        {
            "from": a["from"],
            "to": a["to"],
            "delay": float(a["delay"]),
            "kind": a["kind"],
        }
        for a in data["arcs"]
    ]
    return {
        "name": data.get("name", Path(path).stem),
        "clock": data.get("clock") or {},
        "pins": pins,
        "arcs": arcs,
        "notes": data.get("notes", ""),
    }


def pin_ids(timing: Dict[str, Any]) -> List[str]:
    return [p["id"] for p in timing["pins"]]


def clone_timing(timing: Dict[str, Any]) -> Dict[str, Any]:
    return json.loads(json.dumps(timing))
