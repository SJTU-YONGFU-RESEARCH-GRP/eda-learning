"""Congestion solvers (Track A) — mirror platform/assets/congestion-core.js."""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence, Tuple

from congestionutil import (
    cell_gcell,
    clone_positions,
    gcell_geom,
    hpwl,
    net_bbox,
    zeros,
)

Pos = Dict[str, Dict[str, float]]


def _tiles_for_bbox(
    x0: float, y0: float, x1: float, y1: float, nx: int, ny: int, cw: float, ch: float
) -> List[Tuple[int, int]]:
    i0, j0 = cell_gcell(x0, y0, nx, ny, cw, ch)
    i1, j1 = cell_gcell(x1, y1, nx, ny, cw, ch)
    if i0 > i1:
        i0, i1 = i1, i0
    if j0 > j1:
        j0, j1 = j1, j0
    return [(i, j) for i in range(i0, i1 + 1) for j in range(j0, j1 + 1)]


def rudy_demand(positions: Mapping[str, Mapping[str, float]], data: Mapping[str, Any]) -> List[List[float]]:
    nx, ny, cw, ch, _ = gcell_geom(data)
    demand = zeros(nx, ny)
    for net in data["nets"]:
        x0, y0, x1, y1 = net_bbox(net, positions)
        wl = hpwl(net, positions)
        tiles = _tiles_for_bbox(x0, y0, x1, y1, nx, ny, cw, ch)
        dens = wl / max(1, len(tiles))
        for i, j in tiles:
            demand[i][j] += dens
    return demand


def _deposit_line(
    demand: List[List[float]],
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    amt: float,
    nx: int,
    ny: int,
    cw: float,
    ch: float,
) -> None:
    tiles = _tiles_for_bbox(x0, y0, x1, y1, nx, ny, cw, ch)
    share = amt / max(1, len(tiles))
    for i, j in tiles:
        demand[i][j] += share


def probabilistic_demand(
    positions: Mapping[str, Mapping[str, float]], data: Mapping[str, Any]
) -> List[List[float]]:
    nx, ny, cw, ch, _ = gcell_geom(data)
    demand = zeros(nx, ny)

    def two_pin(pos: Mapping[str, Mapping[str, float]], a: str, b: str, scale: float = 1.0) -> None:
        ax, ay = float(pos[a]["x"]), float(pos[a]["y"])
        bx, by = float(pos[b]["x"]), float(pos[b]["y"])
        # H then V
        _deposit_line(demand, ax, ay, bx, ay, 0.5 * scale, nx, ny, cw, ch)
        _deposit_line(demand, bx, ay, bx, by, 0.5 * scale, nx, ny, cw, ch)
        # V then H
        _deposit_line(demand, ax, ay, ax, by, 0.5 * scale, nx, ny, cw, ch)
        _deposit_line(demand, ax, by, bx, by, 0.5 * scale, nx, ny, cw, ch)

    for net in data["nets"]:
        if len(net) == 2:
            two_pin(positions, net[0], net[1])
        else:
            x0, y0, x1, y1 = net_bbox(net, positions)
            cx, cy = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
            positions_ext = dict(positions)
            positions_ext["__c"] = {"x": cx, "y": cy}
            for p in net:
                two_pin(positions_ext, "__c", p, scale=1.0 / max(1, len(net)))
    return demand


def congestion_map(demand: Sequence[Sequence[float]], capacity: float) -> List[List[float]]:
    return [[float(d) / capacity for d in col] for col in demand]


def overflow_metrics(demand: Sequence[Sequence[float]], capacity: float) -> dict:
    ov = [[max(0.0, float(d) - capacity) for d in col] for col in demand]
    flat = [v for col in ov for v in col]
    return {
        "total": sum(flat),
        "max": max(flat) if flat else 0.0,
        "count": sum(1 for v in flat if v > 0),
        "perCell": ov,
    }


def hottest(cong: Sequence[Sequence[float]]) -> Tuple[int, int, float]:
    best = (0, 0, -1.0)
    for i, col in enumerate(cong):
        for j, v in enumerate(col):
            if v > best[2]:
                best = (i, j, float(v))
    return best


def inflate_widths(
    positions: Mapping[str, Mapping[str, float]],
    widths: Mapping[str, float],
    cong: Sequence[Sequence[float]],
    data: Mapping[str, Any],
    alpha: float = 0.5,
) -> Dict[str, float]:
    nx, ny, cw, ch, _ = gcell_geom(data)
    out = {k: float(v) for k, v in widths.items()}
    for cid, p in positions.items():
        i, j = cell_gcell(float(p["x"]), float(p["y"]), nx, ny, cw, ch)
        c = float(cong[i][j])
        if c > 1.0:
            out[cid] = float(widths.get(cid, 1.0)) * (1.0 + alpha * (c - 1.0))
    return out


def net_weights_from_congestion(
    positions: Mapping[str, Mapping[str, float]],
    cong: Sequence[Sequence[float]],
    data: Mapping[str, Any],
    beta: float = 1.0,
) -> List[float]:
    nx, ny, cw, ch, _ = gcell_geom(data)
    weights: List[float] = []
    for net in data["nets"]:
        x0, y0, x1, y1 = net_bbox(net, positions)
        tiles = _tiles_for_bbox(x0, y0, x1, y1, nx, ny, cw, ch)
        mean = sum(float(cong[i][j]) for i, j in tiles) / max(1, len(tiles))
        weights.append(1.0 + beta * mean)
    return weights


def placement_feedback_lite(
    positions: Mapping[str, Mapping[str, float]], data: Mapping[str, Any], alpha: float = 0.5
) -> Pos:
    nx, ny, cw, ch, cap = gcell_geom(data)
    demand = rudy_demand(positions, data)
    cong = congestion_map(demand, cap)
    ov = overflow_metrics(demand, cap)["perCell"]
    out = clone_positions(positions)
    chip_w = float(data["chip"]["W"])
    chip_h = float(data["chip"]["H"])
    for cid, p in list(out.items()):
        i, j = cell_gcell(p["x"], p["y"], nx, ny, cw, ch)
        if ov[i][j] <= 0:
            continue
        best = (i, j, ov[i][j])
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < nx and 0 <= nj < ny and ov[ni][nj] < best[2]:
                best = (ni, nj, ov[ni][nj])
        ti, tj = best[0], best[1]
        tx = (ti + 0.5) * cw
        ty = (tj + 0.5) * ch
        out[cid] = {
            "x": max(0.0, min(chip_w - 1.0, 0.5 * (p["x"] + tx))),
            "y": max(0.0, min(chip_h - 1.0, 0.5 * (p["y"] + ty))),
        }
    return out
