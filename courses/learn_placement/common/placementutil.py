"""Shared tiny-placement I/O and HPWL metrics for learn_placement Track A."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

Pos = Dict[str, float]
Placement = Dict[str, Pos]

# Goldens aligned with platform/assets/placement-core.js
STARTER_HPWL = 52
GOLDEN_HPWL = 14
STARTER_TIMING_HPWL = 116
GOLDEN_TIMING_HPWL = 30
FORCE_HPWL_AFTER = 18.7
QUADRATIC_HPWL_AFTER = 48
ANALYTICAL_HPWL_AFTER = 48.1
SA_HPWL_AFTER = 49.6


def load_place(path: Path | str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    cells = list(data["cells"])
    nets = [list(n) for n in data["nets"]]
    weights = list(data.get("net_weights", [1] * len(nets)))
    fixed = list(data.get("fixed_pads", []))
    return {
        "cells": cells,
        "nets": nets,
        "net_weights": weights,
        "fixed_pads": fixed,
        "starter": {k: {"x": float(v["x"]), "y": float(v["y"])} for k, v in data["starter"].items()},
        "golden": {k: {"x": float(v["x"]), "y": float(v["y"])} for k, v in data["golden"].items()},
        "overlap": {
            k: {"x": float(v["x"]), "y": float(v["y"])} for k, v in data.get("overlap", {}).items()
        },
        "raw": data,
    }


def clone_positions(pos: Mapping[str, Mapping[str, float]]) -> Placement:
    return {cid: {"x": float(p["x"]), "y": float(p["y"])} for cid, p in pos.items()}


def hpwl(net: Sequence[str], positions: Mapping[str, Mapping[str, float]]) -> float:
    xs: List[float] = []
    ys: List[float] = []
    for cid in net:
        p = positions.get(cid)
        if not p:
            continue
        xs.append(float(p["x"]))
        ys.append(float(p["y"]))
    if not xs:
        return 0.0
    return (max(xs) - min(xs)) + (max(ys) - min(ys))


def total_hpwl(nets: Iterable[Sequence[str]], positions: Mapping[str, Mapping[str, float]]) -> float:
    return float(sum(hpwl(n, positions) for n in nets))


def clique_hpwl(net: Sequence[str], positions: Mapping[str, Mapping[str, float]]) -> float:
    s = 0.0
    for i in range(len(net)):
        for j in range(i + 1, len(net)):
            s += hpwl([net[i], net[j]], positions)
    return s


def star_hpwl(
    net: Sequence[str],
    positions: Mapping[str, Mapping[str, float]],
    hub: str | None = None,
) -> float:
    h = hub if hub is not None else net[0]
    return float(sum(hpwl([h, cid], positions) for cid in net if cid != h))


def timing_weighted_hpwl(
    nets: Sequence[Sequence[str]],
    positions: Mapping[str, Mapping[str, float]],
    weights: Sequence[float],
) -> float:
    s = 0.0
    for i, net in enumerate(nets):
        w = float(weights[i]) if i < len(weights) else 1.0
        s += w * hpwl(net, positions)
    return s


def neighbors_of(cells: Sequence[str], nets: Sequence[Sequence[str]]) -> Dict[str, set]:
    adj: Dict[str, set] = {c: set() for c in cells}
    for net in nets:
        for i in range(len(net)):
            for j in range(i + 1, len(net)):
                adj[net[i]].add(net[j])
                adj[net[j]].add(net[i])
    return adj


def density_bins(
    positions: Mapping[str, Mapping[str, float]],
    *,
    nx: int = 2,
    ny: int = 2,
    x0: float = 0.0,
    y0: float = 0.0,
    x1: float = 8.0,
    y1: float = 8.0,
    capacity: int = 1,
) -> dict:
    bw = (x1 - x0) / nx
    bh = (y1 - y0) / ny
    counts = [[0 for _ in range(nx)] for _ in range(ny)]
    for p in positions.values():
        bx = int((float(p["x"]) - x0) // bw)
        by = int((float(p["y"]) - y0) // bh)
        bx = max(0, min(nx - 1, bx))
        by = max(0, min(ny - 1, by))
        counts[by][bx] += 1
    overflow = 0
    for row in counts:
        for c in row:
            overflow += max(0, c - capacity)
    return {
        "counts": counts,
        "overflow": overflow,
        "capacity": capacity,
        "nx": nx,
        "ny": ny,
    }


def round1(n: float) -> float:
    return round(n * 10.0) / 10.0


def near(a: float, b: float, eps: float = 0.15) -> bool:
    return abs(a - b) <= eps
