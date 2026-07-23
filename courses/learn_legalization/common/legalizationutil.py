"""Shared tiny-legalization I/O, legality, displacement, and HPWL for learn_legalization Track A."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

Pos = Dict[str, float]
Placement = Dict[str, Pos]


def load_legal(path: Path | str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    chip = data["chip"]
    cells = {c["id"]: int(c["width"]) for c in data["cells"]}
    fixed = {m["id"]: m for m in data.get("fixed_macros", [])}
    return {
        "chip": {
            "W": int(chip["W"]),
            "H": int(chip["H"]),
            "siteW": float(chip.get("siteW", 1)),
            "rowH": float(chip.get("rowH", 2)),
            "rows": [float(y) for y in chip["rows"]],
        },
        "cells": cells,
        "nets": [list(n) for n in data["nets"]],
        "fixed_macros": fixed,
        "starter_illegal": _clone_positions(data.get("starter_illegal", {})),
        "starter_float": _clone_positions(data.get("starter_float", {})),
        "raw": data,
    }


def _clone_positions(pos: Mapping[str, Mapping[str, float]]) -> Placement:
    return {cid: {"x": float(p["x"]), "y": float(p["y"])} for cid, p in pos.items()}


def clone_positions(pos: Mapping[str, Mapping[str, float]]) -> Placement:
    return _clone_positions(pos)


def cell_width(cells: Mapping[str, int], cid: str) -> int:
    return int(cells.get(cid, 1))


def row_height(chip: Mapping[str, float]) -> float:
    return float(chip["rowH"])


def is_site_aligned(x: float, eps: float = 1e-6) -> bool:
    return abs(x - round(x)) <= eps


def nearest_row(y: float, rows: Sequence[float]) -> float:
    return min(rows, key=lambda r: abs(y - r))


def in_chip(x: float, width: int, y: float, chip: Mapping[str, float]) -> bool:
    w = int(chip["W"])
    h = float(chip["H"])
    rh = row_height(chip)
    return 0 <= x and x + width <= w and 0 <= y and y + rh <= h


def intervals_overlap(a0: float, a1: float, b0: float, b1: float) -> bool:
    return a0 < b1 and b0 < a1


def same_row(y1: float, y2: float, eps: float = 1e-6) -> bool:
    return abs(y1 - y2) <= eps


def check_legality(
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip: Mapping[str, float],
    fixed: Mapping[str, Mapping] | None = None,
) -> Tuple[bool, str]:
    rows = list(chip["rows"])
    rh = row_height(chip)
    fixed = fixed or {}
    ids = list(positions.keys())

    for cid in ids:
        p = positions[cid]
        x, y = float(p["x"]), float(p["y"])
        w = cell_width(cells, cid)
        if not is_site_aligned(x):
            return False, f"{cid}: x={x} not site-aligned"
        if y not in rows and all(abs(y - r) > 1e-6 for r in rows):
            return False, f"{cid}: y={y} not on row bottom {rows}"
        if not in_chip(x, w, y, chip):
            return False, f"{cid}: outside chip"
        if cid in fixed:
            fx, fy = float(fixed[cid]["x"]), float(fixed[cid]["y"])
            if abs(x - fx) > 1e-6 or abs(y - fy) > 1e-6:
                return False, f"{cid}: fixed macro moved"

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            pa, pb = positions[a], positions[b]
            if not same_row(float(pa["y"]), float(pb["y"])):
                continue
            wa = cell_width(cells, a)
            wb = cell_width(cells, b)
            if intervals_overlap(float(pa["x"]), float(pa["x"]) + wa, float(pb["x"]), float(pb["x"]) + wb):
                return False, f"overlap {a} vs {b} on row y={pa['y']}"

    return True, "ok"


def hpwl(
    net: Sequence[str],
    positions: Mapping[str, Mapping[str, float]],
    *,
    cells: Mapping[str, int] | None = None,
    row_h: float = 2.0,
) -> float:
    """Half-perimeter using cell centers (matches legalization-core.js)."""
    xs: List[float] = []
    ys: List[float] = []
    for cid in net:
        p = positions.get(cid)
        if not p:
            continue
        w = float(cells.get(cid, 1)) if cells else 1.0
        xs.append(float(p["x"]) + w / 2.0)
        ys.append(float(p["y"]) + row_h / 2.0)
    if not xs:
        return 0.0
    return (max(xs) - min(xs)) + (max(ys) - min(ys))


def total_hpwl(
    nets: Iterable[Sequence[str]],
    positions: Mapping[str, Mapping[str, float]],
    *,
    cells: Mapping[str, int] | None = None,
    row_h: float = 2.0,
) -> float:
    return float(sum(hpwl(n, positions, cells=cells, row_h=row_h) for n in nets))


def total_displacement(
    before: Mapping[str, Mapping[str, float]],
    after: Mapping[str, Mapping[str, float]],
    *,
    fixed: Iterable[str] = (),
) -> float:
    """L1 on lower-left coords for all cells (matches legalization-core.js)."""
    del fixed  # API compat; JS sums every cell
    s = 0.0
    for cid, p0 in before.items():
        p1 = after.get(cid)
        if not p1:
            continue
        s += abs(float(p1["x"]) - float(p0["x"])) + abs(float(p1["y"]) - float(p0["y"]))
    return s


def summarize(positions: Mapping[str, Mapping[str, float]], nets: Sequence[Sequence[str]]) -> str:
    return f"HPWL={total_hpwl(nets, positions):.4g} cells={len(positions)}"
