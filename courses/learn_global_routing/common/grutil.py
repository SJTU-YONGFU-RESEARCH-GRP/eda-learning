"""Helpers for learn_global_routing Track A."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

GCell = Tuple[int, int]
Edge = Tuple[GCell, GCell]
Pos = Dict[str, Dict[str, float]]


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def gcell_geom(data: Mapping[str, Any]) -> Tuple[int, int, float, float, float]:
    g = data["gcell"]
    cap = float(data.get("edge_capacity", data.get("capacity", 2)))
    return int(g["nx"]), int(g["ny"]), float(g["cellW"]), float(g["cellH"]), cap


def cell_gcell(x: float, y: float, nx: int, ny: int, cell_w: float, cell_h: float) -> GCell:
    i = int(x // cell_w)
    j = int(y // cell_h)
    return max(0, min(nx - 1, i)), max(0, min(ny - 1, j))


def cell_gcell_from_data(x: float, y: float, data: Mapping[str, Any]) -> GCell:
    nx, ny, cw, ch, _ = gcell_geom(data)
    return cell_gcell(x, y, nx, ny, cw, ch)


def terminals(positions: Mapping[str, Mapping[str, float]], data: Mapping[str, Any]) -> Dict[str, GCell]:
    nx, ny, cw, ch, _ = gcell_geom(data)
    return {cid: cell_gcell(float(p["x"]), float(p["y"]), nx, ny, cw, ch) for cid, p in positions.items()}


def edge_key(a: GCell, b: GCell) -> Edge:
    return tuple(sorted((a, b)))  # type: ignore[return-value]


def edge_list(nx: int, ny: int) -> List[Edge]:
    edges: List[Edge] = []
    for i in range(nx):
        for j in range(ny):
            if i + 1 < nx:
                edges.append(edge_key((i, j), (i + 1, j)))
            if j + 1 < ny:
                edges.append(edge_key((i, j), (i, j + 1)))
    return edges


def neighbors(g: GCell, nx: int, ny: int) -> List[GCell]:
    i, j = g
    out: List[GCell] = []
    if i + 1 < nx:
        out.append((i + 1, j))
    if i > 0:
        out.append((i - 1, j))
    if j + 1 < ny:
        out.append((i, j + 1))
    if j > 0:
        out.append((i, j - 1))
    return out
