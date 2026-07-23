"""Reference bipartition solvers for learn_partitioning Track A."""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from graphutil import (
    BAD_SEED,
    GOLDEN_BIPART,
    Edge,
    adjacency,
    balance_metrics,
    cutsize,
    parts_string,
)


def _d_values(side: Dict[str, str], adj: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    d: Dict[str, float] = {}
    for v, s in side.items():
        ext = inn = 0.0
        for nbr, w in adj.get(v, {}).items():
            if side[nbr] == s:
                inn += w
            else:
                ext += w
        d[v] = ext - inn
    return d


def kernighan_lin(
    nodes: List[str],
    edges: List[Edge],
    initial: Dict[str, str],
    max_passes: int = 10,
) -> Dict[str, str]:
    """Classic KL pair-swap bipartition with rollback to best prefix."""
    adj = adjacency(edges)
    side = dict(initial)
    for _ in range(max_passes):
        unlocked = set(nodes)
        d = _d_values(side, adj)
        seq: List[Tuple[str, str, float]] = []
        working = dict(side)
        for _step in range(len(nodes) // 2):
            best = None
            for a in list(unlocked):
                for b in list(unlocked):
                    if a >= b or working[a] == working[b]:
                        continue
                    gab = d[a] + d[b] - 2 * adj.get(a, {}).get(b, 0.0)
                    if best is None or gab > best[2]:
                        best = (a, b, gab)
            if best is None:
                break
            a, b, g = best
            seq.append((a, b, g))
            working[a], working[b] = working[b], working[a]
            unlocked.discard(a)
            unlocked.discard(b)
            d = _d_values(working, adj)
        if not seq:
            break
        cum = 0.0
        best_k, best_cum = 0, 0.0
        for i, (_, _, g) in enumerate(seq, start=1):
            cum += g
            if cum > best_cum:
                best_cum, best_k = cum, i
        if best_k == 0 or best_cum <= 0:
            break
        for a, b, _ in seq[:best_k]:
            side[a], side[b] = side[b], side[a]
    return side


def fiduccia_mattheyses(
    nodes: List[str],
    edges: List[Edge],
    initial: Dict[str, str],
    max_passes: int = 10,
    balance_tol: float = 0.35,
) -> Dict[str, str]:
    """FM single-vertex moves with simple balance filter."""
    adj = adjacency(edges)
    side = dict(initial)
    parts = sorted({side[n] for n in nodes})
    if len(parts) != 2:
        return side
    pa, pb = parts[0], parts[1]

    def gain(v: str, cur: Dict[str, str]) -> float:
        s = cur[v]
        g = 0.0
        for nbr, w in adj.get(v, {}).items():
            g += w if cur[nbr] != s else -w
        return g

    def legal(v: str, cur: Dict[str, str]) -> bool:
        trial = dict(cur)
        trial[v] = pb if trial[v] == pa else pa
        m = balance_metrics(trial, {n: 1.0 for n in nodes})
        return m["imbalance"] is not None and m["imbalance"] <= balance_tol + 1e-9

    for _ in range(max_passes):
        unlocked = set(nodes)
        seq: List[Tuple[str, float]] = []
        working = dict(side)
        while unlocked:
            ranked = sorted(
                ((v, gain(v, working)) for v in unlocked if legal(v, working)),
                key=lambda t: (-t[1], t[0]),
            )
            if not ranked:
                break
            v, g = ranked[0]
            seq.append((v, g))
            working[v] = pb if working[v] == pa else pa
            unlocked.discard(v)
        if not seq:
            break
        cum = 0.0
        best_k, best_cum = 0, 0.0
        for i, (_, g) in enumerate(seq, start=1):
            cum += g
            if cum > best_cum:
                best_cum, best_k = cum, i
        if best_k == 0 or best_cum <= 0:
            break
        for v, _ in seq[:best_k]:
            side[v] = pb if side[v] == pa else pa
    return side


def summarize(assignment: Dict[str, str], edges: List[Edge], sizes: Optional[Dict[str, float]] = None) -> dict:
    sizes = sizes or {n: 1.0 for n in assignment}
    return {
        "parts": parts_string(assignment),
        "cutsize": cutsize(assignment, edges),
        "balance": balance_metrics(assignment, sizes),
    }


__all__ = [
    "BAD_SEED",
    "GOLDEN_BIPART",
    "kernighan_lin",
    "fiduccia_mattheyses",
    "summarize",
]
