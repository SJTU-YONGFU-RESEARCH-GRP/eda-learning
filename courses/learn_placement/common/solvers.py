"""Reference placement solvers for learn_placement Track A (force / SA lite ports)."""
from __future__ import annotations

import math
from typing import Dict, Mapping, Optional, Sequence, Set

from placementutil import (
    clone_positions,
    neighbors_of,
    total_hpwl,
)

Placement = Dict[str, Dict[str, float]]


def force_directed_place(
    positions: Mapping[str, Mapping[str, float]],
    cells: Sequence[str],
    nets: Sequence[Sequence[str]],
    *,
    iters: int = 5,
    alpha: float = 0.12,
    center_pull: float = 0.02,
    fixed: Optional[Sequence[str]] = None,
    cx: float = 4.0,
    cy: float = 4.0,
) -> Placement:
    """Force-directed place: partial spring pull + weak center pull (placement-core.js port)."""
    fixed_set: Set[str] = set(fixed or ())
    pos = clone_positions(positions)
    adj = neighbors_of(cells, nets)

    for _ in range(iters):
        nxt = clone_positions(pos)
        for cid in cells:
            if cid in fixed_set:
                continue
            nbs = list(adj.get(cid, ()))
            if not nbs:
                continue
            sx = sum(pos[nb]["x"] for nb in nbs)
            sy = sum(pos[nb]["y"] for nb in nbs)
            tx = sx / len(nbs)
            ty = sy / len(nbs)
            nxt[cid]["x"] = pos[cid]["x"] + alpha * (tx - pos[cid]["x"]) + center_pull * (
                cx - pos[cid]["x"]
            )
            nxt[cid]["y"] = pos[cid]["y"] + alpha * (ty - pos[cid]["y"]) + center_pull * (
                cy - pos[cid]["y"]
            )
        pos = nxt
    return pos


def quadratic_place(
    positions: Mapping[str, Mapping[str, float]],
    cells: Sequence[str],
    nets: Sequence[Sequence[str]],
    *,
    iters: int = 6,
    fixed: Optional[Sequence[str]] = None,
    blend: float = 0.55,
) -> Placement:
    """Quadratic-lite: Gauss–Seidel neighbor average with fixed pads."""
    fixed_set: Set[str] = set(fixed if fixed is not None else ("A", "D"))
    pos = clone_positions(positions)
    adj = neighbors_of(cells, nets)

    for _ in range(iters):
        for cid in cells:
            if cid in fixed_set:
                continue
            nbs = list(adj.get(cid, ()))
            if not nbs:
                continue
            ax = sum(pos[nb]["x"] for nb in nbs) / len(nbs)
            ay = sum(pos[nb]["y"] for nb in nbs) / len(nbs)
            pos[cid]["x"] = blend * ax + (1.0 - blend) * pos[cid]["x"]
            pos[cid]["y"] = blend * ay + (1.0 - blend) * pos[cid]["y"]
    return pos


def _mulberry32_js(seed: int):
    """Match JS mulberry32 bit-for-bit (placement-core.js)."""
    a = seed & 0xFFFFFFFF

    def u32(x: int) -> int:
        return x & 0xFFFFFFFF

    def imul(x: int, y: int) -> int:
        return u32(x * y)

    def rand() -> float:
        nonlocal a
        a = u32(a + 0x6D2B79F5)
        t = a
        t = imul(t ^ (t >> 15), 1 | t)
        t = u32(t + imul(t ^ (t >> 7), 61 | t)) ^ t
        return (u32(t ^ (t >> 14))) / 4294967296.0

    return rand


def sa_place(
    positions: Mapping[str, Mapping[str, float]],
    cells: Sequence[str],
    nets: Sequence[Sequence[str]],
    *,
    moves: int = 60,
    t0: float = 3.0,
    cool: float = 0.94,
    step: float = 1.0,
    seed: int = 42,
) -> dict:
    """Simulated annealing placement (placement-core.js saPlace port)."""
    rand = _mulberry32_js(seed)
    pos = clone_positions(positions)
    cur = total_hpwl(nets, pos)
    best = clone_positions(pos)
    best_hpwl = cur
    T = t0
    accepted = 0
    rejected = 0
    history = [{"hpwl": cur, "T": T}]
    cell_list = list(cells)

    for m in range(moves):
        cid = cell_list[int(rand() * len(cell_list)) % len(cell_list)]
        trial = clone_positions(pos)
        axis = "x" if rand() < 0.5 else "y"
        delta = (-1 if rand() < 0.5 else 1) * step * (0.5 + rand())
        trial[cid] = {"x": pos[cid]["x"], "y": pos[cid]["y"]}
        trial[cid][axis] = pos[cid][axis] + delta
        trial[cid]["x"] = max(-1.0, min(9.0, trial[cid]["x"]))
        trial[cid]["y"] = max(-1.0, min(9.0, trial[cid]["y"]))
        nxt = total_hpwl(nets, trial)
        d = nxt - cur
        if d <= 0 or rand() < math.exp(-d / max(T, 1e-9)):
            pos = trial
            cur = nxt
            accepted += 1
            if cur < best_hpwl:
                best_hpwl = cur
                best = clone_positions(pos)
        else:
            rejected += 1
        T *= cool
        if m % 10 == 9:
            history.append({"hpwl": cur, "T": T})

    return {
        "positions": best,
        "hpwl": best_hpwl,
        "accepted": accepted,
        "rejected": rejected,
        "history": history,
        "final_hpwl": cur,
    }


def summarize(positions: Mapping[str, Mapping[str, float]], nets: Sequence[Sequence[str]]) -> str:
    return f"HPWL={total_hpwl(nets, positions):.4g} cells={len(positions)}"
