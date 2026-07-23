"""Helpers for learn_congestion Track A."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

Pos = Dict[str, Dict[str, float]]


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def gcell_geom(data: Mapping[str, Any]) -> Tuple[int, int, float, float, float]:
    g = data["gcell"]
    return int(g["nx"]), int(g["ny"]), float(g["cellW"]), float(g["cellH"]), float(data["capacity"])


def cell_gcell(x: float, y: float, nx: int, ny: int, cell_w: float, cell_h: float) -> Tuple[int, int]:
    i = int(x // cell_w)
    j = int(y // cell_h)
    return max(0, min(nx - 1, i)), max(0, min(ny - 1, j))


def net_bbox(net: Sequence[str], positions: Mapping[str, Mapping[str, float]]) -> Tuple[float, float, float, float]:
    xs = [float(positions[c]["x"]) for c in net if c in positions]
    ys = [float(positions[c]["y"]) for c in net if c in positions]
    return min(xs), min(ys), max(xs), max(ys)


def hpwl(net: Sequence[str], positions: Mapping[str, Mapping[str, float]]) -> float:
    x0, y0, x1, y1 = net_bbox(net, positions)
    return (x1 - x0) + (y1 - y0)


def zeros(nx: int, ny: int) -> List[List[float]]:
    return [[0.0 for _ in range(ny)] for _ in range(nx)]


def clone_positions(pos: Mapping[str, Mapping[str, float]]) -> Pos:
    return {k: {"x": float(v["x"]), "y": float(v["y"])} for k, v in pos.items()}
