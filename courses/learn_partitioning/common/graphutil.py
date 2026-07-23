"""Shared tiny-graph I/O and metrics for learn_partitioning Track A."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

Edge = Tuple[str, str, float]

BAD_SEED = {"A": "0", "E": "0", "B": "1", "C": "1", "D": "1"}
GOLDEN_BIPART = {"A": "0", "B": "0", "C": "0", "D": "1", "E": "1"}


def load_graph(path: Path | str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    nodes = list(data["nodes"])
    edges: List[Edge] = []
    for e in data["edges"]:
        u, v, w = e["u"], e["v"], float(e["w"])
        if u == v:
            continue
        if u > v:
            u, v = v, u
        edges.append((u, v, w))
    sizes = {n: float(data.get("node_sizes", {}).get(n, 1.0)) for n in nodes}
    return {"nodes": nodes, "edges": edges, "sizes": sizes, "raw": data}


def adjacency(edges: Iterable[Edge]) -> Dict[str, Dict[str, float]]:
    adj: Dict[str, Dict[str, float]] = defaultdict(dict)
    for u, v, w in edges:
        adj[u][v] = adj[u].get(v, 0.0) + w
        adj[v][u] = adj[v].get(u, 0.0) + w
    return adj


def cutsize(assignment: Dict[str, str], edges: Iterable[Edge]) -> float:
    total = 0.0
    for u, v, w in edges:
        if assignment[u] != assignment[v]:
            total += w
    return total


def part_sizes(assignment: Dict[str, str], sizes: Dict[str, float]) -> Dict[str, float]:
    out: Dict[str, float] = defaultdict(float)
    for node, part in assignment.items():
        out[part] += sizes.get(node, 1.0)
    return dict(out)


def balance_metrics(assignment: Dict[str, str], sizes: Dict[str, float]) -> dict:
    ps = part_sizes(assignment, sizes)
    labs = sorted(ps)
    if len(labs) != 2:
        return {"parts": ps, "labels": labs, "ratio": None, "imbalance": None}
    s0, s1 = ps[labs[0]], ps[labs[1]]
    total = s0 + s1
    lo, hi = min(s0, s1), max(s0, s1)
    return {
        "parts": ps,
        "labels": labs,
        "sizes": [s0, s1],
        "ratio": lo / hi if hi else None,
        "imbalance": abs(s0 - s1) / total if total else None,
    }


def parts_string(assignment: Dict[str, str]) -> str:
    groups: Dict[str, List[str]] = defaultdict(list)
    for n, p in assignment.items():
        groups[p].append(n)
    chunks = ["".join(sorted(v)) for v in groups.values()]
    return "|".join(sorted(chunks))
