"""Clock tree instance helpers (Track A)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, MutableMapping, Sequence, Tuple, Union

Point = Union[Dict[str, float], Tuple[float, float], List[float]]


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _xy(p: Point) -> Tuple[float, float]:
    if isinstance(p, (tuple, list)):
        return float(p[0]), float(p[1])
    return float(p["x"]), float(p["y"])


def sink_points(placement: Mapping[str, Mapping[str, float]], sinks: Sequence[str]) -> List[dict[str, Any]]:
    return [{"id": sid, "x": placement[sid]["x"], "y": placement[sid]["y"]} for sid in sinks]


def manhattan(a: Point, b: Point) -> float:
    ax, ay = _xy(a)
    bx, by = _xy(b)
    return abs(ax - bx) + abs(ay - by)


def chip_bbox(chip: Mapping[str, float]) -> dict[str, float]:
    return {"xmin": 0.0, "ymin": 0.0, "xmax": float(chip["W"]), "ymax": float(chip["H"])}


def edge_key(a: Point, b: Point) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    ax, ay = _xy(a)
    bx, by = _xy(b)
    pa = (round(ax, 6), round(ay, 6))
    pb = (round(bx, 6), round(by, 6))
    return (pa, pb) if pa <= pb else (pb, pa)


def normalize_edge(a: Point, b: Point) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    return edge_key(a, b)
