"""Grid helpers for learn_routing Track A."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

Grid = Tuple[int, int]
Seg = Dict[str, Any]
Blockage = Tuple[int, int, int, int]  # x, y, w, h


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def grid_size(data: Mapping[str, Any]) -> Tuple[int, int, float]:
    g = data["grid"]
    cap = float(data.get("track_capacity", 1))
    return int(g["nx"]), int(g["ny"]), cap


def pin_grid(x: float, y: float, nx: int, ny: int) -> Grid:
    gx = int(round(x))
    gy = int(round(y))
    return max(0, min(nx - 1, gx)), max(0, min(ny - 1, gy))


def pin_grid_from_data(x: float, y: float, data: Mapping[str, Any]) -> Grid:
    nx, ny, _ = grid_size(data)
    return pin_grid(x, y, nx, ny)


def blockages(data: Mapping[str, Any]) -> List[Blockage]:
    out: List[Blockage] = []
    for b in data.get("blockages", []):
        out.append((int(b["x"]), int(b["y"]), int(b["w"]), int(b["h"])))
    return out


def cell_blocked(gx: int, gy: int, blocks: Sequence[Blockage]) -> bool:
    for bx, by, bw, bh in blocks:
        if bx <= gx < bx + bw and by <= gy < by + bh:
            return True
    return False


def neighbors4(
    gx: int,
    gy: int,
    nx: int,
    ny: int,
    blocks: Sequence[Blockage] = (),
) -> List[Grid]:
    out: List[Grid] = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx_, ny_ = gx + dx, gy + dy
        if 0 <= nx_ < nx and 0 <= ny_ < ny and not cell_blocked(nx_, ny_, blocks):
            out.append((nx_, ny_))
    return out


def terminals(positions: Mapping[str, Mapping[str, float]], data: Mapping[str, Any]) -> Dict[str, Grid]:
    nx, ny, _ = grid_size(data)
    blocks = blockages(data)
    term: Dict[str, Grid] = {}
    for cid, p in positions.items():
        g = pin_grid(float(p["x"]), float(p["y"]), nx, ny)
        if cell_blocked(g[0], g[1], blocks):
            # nudge to nearest free neighbor for toy instances
            for nb in neighbors4(g[0], g[1], nx, ny, blocks):
                g = nb
                break
        term[cid] = g
    return term


def h_edge(a: Grid, b: Grid) -> Tuple[str, Grid, Grid]:
    """Directed M1 horizontal edge (left→right canonical key)."""
    if a[0] <= b[0]:
        return ("M1", a, b)
    return ("M1", b, a)


def v_edge(a: Grid, b: Grid) -> Tuple[str, Grid, Grid]:
    """Directed M2 vertical edge (bottom→top canonical key)."""
    if a[1] <= b[1]:
        return ("M2", a, b)
    return ("M2", b, a)


def track_key(layer: str, a: Grid, b: Grid) -> Tuple[str, Grid, Grid]:
    if layer == "M1":
        return h_edge(a, b)
    return v_edge(a, b)
