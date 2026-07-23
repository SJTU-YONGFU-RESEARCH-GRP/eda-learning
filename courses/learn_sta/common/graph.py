"""Timing-graph construction and levelization for learn_sta."""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Tuple

from timing_io import clone_timing, load_timing, pin_ids

# Goldens for common/tiny_timing.json (must match sta-core.js).
GOLDENS = {
    "pin_count": 6,
    "arc_count": 5,
    "cell_arcs": 2,
    "net_arcs": 3,
    "max_level": 5,
    "sources": ["in"],
    "sinks": ["out"],
    "topo": ["in", "u1/A", "u1/Y", "u2/A", "u2/Y", "out"],
    "levels": {
        "in": 0,
        "u1/A": 1,
        "u1/Y": 2,
        "u2/A": 3,
        "u2/Y": 4,
        "out": 5,
    },
    "path_delay": 3.2,  # sum of delays along the single chain
    "cell_delay_sum": 2.7,
}


def successors(timing: Dict[str, Any]) -> Dict[str, List[Tuple[str, float, str]]]:
    succ: Dict[str, List[Tuple[str, float, str]]] = defaultdict(list)
    for a in timing["arcs"]:
        succ[a["from"]].append((a["to"], float(a["delay"]), a["kind"]))
    return succ


def predecessors(timing: Dict[str, Any]) -> Dict[str, List[Tuple[str, float, str]]]:
    pred: Dict[str, List[Tuple[str, float, str]]] = defaultdict(list)
    for a in timing["arcs"]:
        pred[a["to"]].append((a["from"], float(a["delay"]), a["kind"]))
    return pred


def sources(timing: Dict[str, Any]) -> List[str]:
    ids = set(pin_ids(timing))
    has_in = {a["to"] for a in timing["arcs"]}
    return sorted(ids - has_in)


def sinks(timing: Dict[str, Any]) -> List[str]:
    ids = set(pin_ids(timing))
    has_out = {a["from"] for a in timing["arcs"]}
    return sorted(ids - has_out)


def arc_kind_counts(timing: Dict[str, Any]) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    for a in timing["arcs"]:
        counts[a["kind"]] += 1
    return dict(counts)


def levelize(timing: Dict[str, Any]) -> Optional[Dict[str, int]]:
    """Kahn levelization. Returns pin→level, or None if a cycle exists."""
    ids = pin_ids(timing)
    indeg = {p: 0 for p in ids}
    succ = successors(timing)
    for a in timing["arcs"]:
        if a["to"] not in indeg or a["from"] not in indeg:
            raise KeyError(f"arc endpoint missing pin: {a}")
        indeg[a["to"]] += 1
    q = deque([p for p in ids if indeg[p] == 0])
    levels: Dict[str, int] = {p: 0 for p in ids if indeg[p] == 0}
    order: List[str] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v, _d, _k in succ.get(u, []):
            indeg[v] -= 1
            cand = levels[u] + 1
            levels[v] = max(levels.get(v, 0), cand)
            if indeg[v] == 0:
                q.append(v)
    if len(order) != len(ids):
        return None
    return {p: levels[p] for p in ids}


def topo_order(timing: Dict[str, Any]) -> Optional[List[str]]:
    levels = levelize(timing)
    if levels is None:
        return None
    # Stable: by level, then pin id.
    return sorted(pin_ids(timing), key=lambda p: (levels[p], p))


def path_delay_sum(timing: Dict[str, Any]) -> float:
    return round(sum(float(a["delay"]) for a in timing["arcs"]), 6)


def cell_delay_sum(timing: Dict[str, Any]) -> float:
    return round(
        sum(float(a["delay"]) for a in timing["arcs"] if a["kind"] == "cell"),
        6,
    )


def summarize(timing: Dict[str, Any]) -> Dict[str, Any]:
    levels = levelize(timing)
    kinds = arc_kind_counts(timing)
    return {
        "pins": len(timing["pins"]),
        "arcs": len(timing["arcs"]),
        "cell_arcs": kinds.get("cell", 0),
        "net_arcs": kinds.get("net", 0),
        "sources": sources(timing),
        "sinks": sinks(timing),
        "levels": levels,
        "max_level": max(levels.values()) if levels else None,
        "topo": topo_order(timing),
        "path_delay": path_delay_sum(timing),
        "cell_delay_sum": cell_delay_sum(timing),
        "acyclic": levels is not None,
    }


def with_cycle(timing: Dict[str, Any]) -> Dict[str, Any]:
    """Return a clone with a back-edge out→in (creates a cycle)."""
    t = clone_timing(timing)
    t["arcs"].append({"from": "out", "to": "in", "delay": 0.1, "kind": "net"})
    t["name"] = t.get("name", "tiny") + "_cyclic"
    return t
