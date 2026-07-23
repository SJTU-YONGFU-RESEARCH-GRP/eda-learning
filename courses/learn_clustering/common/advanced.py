"""Advanced reference solvers: LP, spectral, FM, multilevel, hypergraph, EDA objectives."""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from graphutil import Edge, adjacency, cutsize

Side = Dict[str, str]


def label_propagation(
    nodes: List[str],
    edges: List[Edge],
    max_iters: int = 50,
    order: Optional[List[str]] = None,
) -> Tuple[Dict[str, str], int]:
    """Asynchronous label propagation; ties -> lexicographically smallest label."""
    adj = adjacency(edges)
    labels = {n: n for n in nodes}
    seq = order or sorted(nodes)
    iters = 0
    for it in range(1, max_iters + 1):
        iters = it
        changed = 0
        for v in seq:
            votes: Dict[str, float] = defaultdict(float)
            for nbr, w in adj.get(v, {}).items():
                votes[labels[nbr]] += w
            if not votes:
                continue
            best_w = max(votes.values())
            candidates = sorted(lab for lab, w in votes.items() if abs(w - best_w) < 1e-12)
            new_lab = candidates[0]
            if new_lab != labels[v]:
                labels[v] = new_lab
                changed += 1
        if changed == 0:
            break
    return dict(labels), iters


def _laplacian(nodes: List[str], edges: List[Edge]) -> List[List[float]]:
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)
    L = [[0.0] * n for _ in range(n)]
    for u, v, w in edges:
        i, j = idx[u], idx[v]
        L[i][j] -= w
        L[j][i] -= w
        L[i][i] += w
        L[j][j] += w
    return L


def _dot(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(a: List[float]) -> float:
    return math.sqrt(_dot(a, a))


def spectral_bisection(
    nodes: List[str],
    edges: List[Edge],
    sizes: Optional[Dict[str, float]] = None,
) -> Tuple[Dict[str, str], List[Tuple[str, float]]]:
    """Fiedler bisection via shifted inverse iteration (pure Python, tiny n)."""
    n = len(nodes)
    if n < 2:
        return {nodes[0]: "0"}, [(nodes[0], 0.0)]
    L = _laplacian(nodes, edges)
    ones = [1.0 / math.sqrt(n)] * n
    x = [1.0 if i % 2 == 0 else -1.0 for i in range(n)]
    x = [xi - _dot(x, ones) * ones[i] for i, xi in enumerate(x)]
    xn = _norm(x) or 1.0
    x = [xi / xn for xi in x]

    eps = 1e-3
    M = [row[:] for row in L]
    for i in range(n):
        M[i][i] += eps

    for _ in range(80):
        y = x[:]
        for _sweep in range(40):
            y_new = y[:]
            for i in range(n):
                s = x[i] - sum(M[i][j] * y[j] for j in range(n) if j != i)
                y_new[i] = s / M[i][i]
            y = y_new
        y = [yi - _dot(y, ones) * ones[i] for i, yi in enumerate(y)]
        yn = _norm(y) or 1.0
        x = [yi / yn for yi in y]

    order = sorted(zip(nodes, x), key=lambda t: (t[1], t[0]))
    sizes = sizes or {n: 1.0 for n in nodes}
    total = sum(sizes[n] for n in nodes)
    best_asn: Optional[Dict[str, str]] = None
    best_cut = float("inf")
    for k in range(1, n):
        left = {order[i][0] for i in range(k)}
        asn = {n: ("0" if n in left else "1") for n in nodes}
        frac = sum(sizes[n] for n in left) / total
        if frac < 0.2 or frac > 0.8:
            continue
        c = cutsize(asn, edges)
        if c < best_cut - 1e-12:
            best_cut = c
            best_asn = asn
    if best_asn is None:
        k = n // 2
        left = {order[i][0] for i in range(k)}
        best_asn = {n: ("0" if n in left else "1") for n in nodes}
    return best_asn, order


def _d_values(side: Side, adj: Dict[str, Dict[str, float]]) -> Dict[str, float]:
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


def fiduccia_mattheyses(
    nodes: List[str],
    edges: List[Edge],
    initial: Side,
    max_passes: int = 10,
    balance_tol: float = 0.35,
) -> Tuple[Side, List[dict]]:
    """Full FM with single-vertex moves, locking, rollback, balance on count."""
    sides = {n: str(initial[n]) for n in nodes}
    adj = adjacency(edges)
    n = len(nodes)
    min_side = max(1, int(math.ceil(n * balance_tol)))
    history: List[dict] = []

    for pass_i in range(max_passes):
        locked: set[str] = set()
        work = dict(sides)
        d = _d_values(work, adj)
        sequence: List[Tuple[str, float]] = []
        cum = 0.0
        best_cum = 0.0
        best_k = 0

        while True:
            free = [v for v in nodes if v not in locked]
            if not free:
                break
            best: Optional[Tuple[str, float]] = None
            for v in free:
                cur = work[v]
                sz_cur = sum(1 for u in nodes if work[u] == cur)
                if sz_cur - 1 < min_side:
                    continue
                if (n - (sz_cur - 1)) < min_side:
                    continue
                g = d[v]
                if best is None or (g, v) > (best[1], best[0]):
                    best = (v, g)
            if best is None:
                break
            v, g = best
            cum += g
            sequence.append((v, g))
            if cum > best_cum + 1e-12:
                best_cum = cum
                best_k = len(sequence)
            work[v] = "1" if work[v] == "0" else "0"
            locked.add(v)
            d = _d_values(work, adj)

        if best_k <= 0 or best_cum <= 1e-12:
            history.append(
                {
                    "pass": pass_i,
                    "best_k": best_k,
                    "best_cum": best_cum,
                    "cut_before": cutsize(sides, edges),
                    "cut_after": cutsize(sides, edges),
                    "improved": False,
                }
            )
            break

        applied = dict(sides)
        for v, _g in sequence[:best_k]:
            applied[v] = "1" if applied[v] == "0" else "0"
        cut_before = cutsize(sides, edges)
        cut_after = cutsize(applied, edges)
        history.append(
            {
                "pass": pass_i,
                "best_k": best_k,
                "best_cum": best_cum,
                "cut_before": cut_before,
                "cut_after": cut_after,
                "moves": sequence[:best_k],
                "improved": cut_after + 1e-12 < cut_before,
            }
        )
        sides = applied
        if not history[-1]["improved"]:
            break
    return sides, history


def multilevel_cluster(
    nodes: List[str],
    edges: List[Edge],
    sizes: Dict[str, float],
    coarse_k: int = 2,
) -> Dict[str, str]:
    """Coarsen with greedy, then FM-refine the projected bipartition."""
    from solvers import greedy_pair_merge

    coarse = greedy_pair_merge(nodes, edges, sizes, target_k=coarse_k)
    labs = sorted(set(coarse.values()))
    if len(labs) != 2:
        return coarse
    bip = {n: ("0" if coarse[n] == labs[0] else "1") for n in nodes}
    refined, _ = fiduccia_mattheyses(nodes, edges, bip)
    return {n: f"P{refined[n]}" for n in nodes}


def load_hypergraph(path: Path | str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    nodes = list(data["nodes"])
    hedges = []
    for h in data["hyperedges"]:
        pins = sorted(set(h["pins"]))
        w = float(h.get("w", 1.0))
        if len(pins) >= 2:
            hedges.append({"pins": pins, "w": w, "id": h.get("id", "")})
    sizes = {n: float(data.get("node_sizes", {}).get(n, 1.0)) for n in nodes}
    return {"nodes": nodes, "hyperedges": hedges, "sizes": sizes}


def hyperedge_cut(assignment: Dict[str, str], hedges: List[dict]) -> float:
    total = 0.0
    for h in hedges:
        if len({assignment[p] for p in h["pins"]}) > 1:
            total += h["w"]
    return total


def hypergraph_greedy_cluster(
    nodes: List[str],
    hedges: List[dict],
    sizes: Dict[str, float],
    target_k: int,
) -> Dict[str, str]:
    members: Dict[str, set[str]] = {n: {n} for n in nodes}
    cur = set(nodes)
    work_hedges = [dict(h, pins=list(h["pins"])) for h in hedges]
    next_id = 0

    def pair_affinity(a: str, b: str) -> float:
        return sum(h["w"] for h in work_hedges if a in h["pins"] and b in h["pins"])

    while len(cur) > target_k:
        best = None
        for a in sorted(cur):
            for b in sorted(cur):
                if b <= a:
                    continue
                aff = pair_affinity(a, b)
                if aff <= 0:
                    continue
                cand = (aff, a, b)
                if best is None or cand > best:
                    best = cand
        if best is None:
            break
        _aff, a, b = best
        new_id = f"H{next_id}"
        next_id += 1
        members[new_id] = members[a] | members[b]
        del members[a]
        del members[b]
        cur.remove(a)
        cur.remove(b)
        cur.add(new_id)
        for h in work_hedges:
            pins2, seen = [], set()
            for p in h["pins"]:
                q = new_id if p in (a, b) else p
                if q not in seen:
                    pins2.append(q)
                    seen.add(q)
            h["pins"] = pins2
        work_hedges = [h for h in work_hedges if len(h["pins"]) >= 2]

    assignment: Dict[str, str] = {}
    for cid, origs in members.items():
        for n in origs:
            assignment[n] = cid
    return assignment


def congestion_aware_partition(
    nodes: List[str],
    edges: List[Edge],
    initial: Side,
    edge_congestion: Dict[Tuple[str, str], float],
    lam: float,
) -> Tuple[Side, float, float, float]:
    boosted: List[Edge] = []
    for u, v, w in edges:
        a, b = (u, v) if u < v else (v, u)
        boosted.append((u, v, w + lam * edge_congestion.get((a, b), 0.0)))
    refined, _ = fiduccia_mattheyses(nodes, boosted, initial)
    plain = cutsize(refined, edges)
    pen = 0.0
    for u, v, _w in edges:
        if refined[u] != refined[v]:
            a, b = (u, v) if u < v else (v, u)
            pen += edge_congestion.get((a, b), 0.0)
    return refined, plain, pen, plain + lam * pen


def timing_aware_partition(
    nodes: List[str],
    edges: List[Edge],
    initial: Side,
    criticality: Dict[Tuple[str, str], float],
) -> Tuple[Side, float, float]:
    weighted: List[Edge] = []
    for u, v, w in edges:
        a, b = (u, v) if u < v else (v, u)
        weighted.append((u, v, w * criticality.get((a, b), 1.0)))
    refined, _ = fiduccia_mattheyses(nodes, weighted, initial)
    return refined, cutsize(refined, edges), cutsize(refined, weighted)
