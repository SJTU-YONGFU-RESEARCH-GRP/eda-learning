"""Shared tiny-graph I/O and metrics for learn_clustering Track A."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

Edge = Tuple[str, str, float]


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


def affinity_edge_weight(edges: Iterable[Edge]) -> List[Tuple[str, str, float]]:
    """Affinity = edge weight for each undirected edge."""
    return sorted(((u, v, w) for u, v, w in edges), key=lambda t: (-t[2], t[0], t[1]))


def affinity_shared_neighbors(
    nodes: List[str], edges: Iterable[Edge]
) -> List[Tuple[str, str, float]]:
    """
    Affinity = weighted shared-neighbor overlap + direct edge weight.
    score(u,v) = w(u,v) + sum_x min(w(u,x), w(v,x)) over common neighbors x.
    Only emits pairs that have either a direct edge or a shared neighbor.
    """
    adj = adjacency(edges)
    scores: Dict[Tuple[str, str], float] = {}
    for u, v, w in edges:
        a, b = (u, v) if u < v else (v, u)
        scores[(a, b)] = scores.get((a, b), 0.0) + w

    for i, u in enumerate(nodes):
        nu = adj.get(u, {})
        for v in nodes[i + 1 :]:
            nv = adj.get(v, {})
            shared = 0.0
            for x, wu in nu.items():
                if x == v:
                    continue
                if x in nv:
                    shared += min(wu, nv[x])
            if shared <= 0 and (u, v) not in scores and (v, u) not in scores:
                continue
            a, b = (u, v) if u < v else (v, u)
            scores[(a, b)] = scores.get((a, b), 0.0) + shared

    return sorted(
        ((u, v, s) for (u, v), s in scores.items()),
        key=lambda t: (-t[2], t[0], t[1]),
    )


def cutsize(assignment: Dict[str, str], edges: Iterable[Edge]) -> float:
    """Sum of weights of edges whose endpoints are in different clusters."""
    total = 0.0
    for u, v, w in edges:
        if assignment[u] != assignment[v]:
            total += w
    return total


def cluster_sizes(assignment: Dict[str, str], sizes: Dict[str, float]) -> Dict[str, float]:
    out: Dict[str, float] = defaultdict(float)
    for node, cid in assignment.items():
        out[cid] += sizes[node]
    return dict(out)


def balance_ratio(assignment: Dict[str, str], sizes: Dict[str, float]) -> float:
    """max_cluster_size / avg_cluster_size (1.0 = perfectly equal)."""
    cs = cluster_sizes(assignment, sizes)
    if not cs:
        return 1.0
    vals = list(cs.values())
    avg = sum(vals) / len(vals)
    return max(vals) / avg if avg > 0 else float("inf")


def contract_pair(
    nodes: List[str],
    edges: List[Edge],
    sizes: Dict[str, float],
    a: str,
    b: str,
    new_id: str,
) -> tuple[List[str], List[Edge], Dict[str, float]]:
    """Contract clusters/nodes a and b into new_id."""
    keep = [n for n in nodes if n not in (a, b)] + [new_id]
    new_sizes = {n: sizes[n] for n in keep if n != new_id}
    new_sizes[new_id] = sizes[a] + sizes[b]
    weight: Dict[Tuple[str, str], float] = defaultdict(float)
    for u, v, w in edges:
        u2 = new_id if u in (a, b) else u
        v2 = new_id if v in (a, b) else v
        if u2 == v2:
            continue
        if u2 > v2:
            u2, v2 = v2, u2
        weight[(u2, v2)] += w
    new_edges = [(u, v, w) for (u, v), w in weight.items()]
    return keep, new_edges, new_sizes
