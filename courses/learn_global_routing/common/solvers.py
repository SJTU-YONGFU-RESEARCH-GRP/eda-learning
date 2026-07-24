"""Global routing solvers (Track A)."""
from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence, Tuple

from grutil import (
    GCell,
    Edge,
    edge_key,
    gcell_geom,
    neighbors,
    terminals,
)

# re-export grutil helpers used by tests
from grutil import cell_gcell, cell_gcell_from_data, load  # noqa: F401


def _walk_h(path: List[GCell], i0: int, i1: int, j: int) -> None:
    if i0 == i1:
        return
    step = 1 if i1 > i0 else -1
    i = i0
    while i != i1:
        i += step
        path.append((i, j))


def _walk_v(path: List[GCell], i: int, j0: int, j1: int) -> None:
    if j0 == j1:
        return
    step = 1 if j1 > j0 else -1
    j = j0
    while j != j1:
        j += step
        path.append((i, j))


def l_route(a: GCell, b: GCell, prefer: str = "HV") -> List[GCell]:
    if a == b:
        return [a]
    ai, aj = a
    bi, bj = b
    path: List[GCell] = [a]
    if prefer.upper() == "HV":
        _walk_h(path, ai, bi, aj)
        _walk_v(path, bi, aj, bj)
    else:
        _walk_v(path, ai, aj, bj)
        _walk_h(path, ai, bi, bj)
    return path


def z_route(a: GCell, b: GCell, prefer: str = "HZ") -> List[GCell]:
    ai, aj = a
    bi, bj = b
    if ai == bi or aj == bj:
        return l_route(a, b, "HV" if prefer.upper().startswith("H") else "VH")
    path: List[GCell] = [a]
    if prefer.upper() == "HZ":
        mid_i = (ai + bi) // 2
        _walk_h(path, ai, mid_i, aj)
        _walk_v(path, mid_i, aj, bj)
        _walk_h(path, mid_i, bi, bj)
    else:
        mid_j = (aj + bj) // 2
        _walk_v(path, ai, aj, mid_j)
        _walk_h(path, ai, bi, mid_j)
        _walk_v(path, bi, mid_j, bj)
    return path


def path_to_edges(path: Sequence[GCell]) -> List[Edge]:
    edges: List[Edge] = []
    for k in range(len(path) - 1):
        edges.append(edge_key(path[k], path[k + 1]))
    return edges


def maze_route(
    a: GCell,
    b: GCell,
    usage: Mapping[Edge, int],
    capacity: float,
    nx: int,
    ny: int,
) -> Optional[List[GCell]]:
    if a == b:
        return [a]
    cap = int(capacity)
    queue: deque[tuple[GCell, List[GCell]]] = deque([(a, [a])])
    visited = {a}
    while queue:
        cur, path = queue.popleft()
        for nb in neighbors(cur, nx, ny):
            e = edge_key(cur, nb)
            if usage.get(e, 0) >= cap:
                continue
            if nb == b:
                return path + [nb]
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, path + [nb]))
    return None


def _bbox_center_gcell(pins: Sequence[GCell]) -> GCell:
    is_ = [p[0] for p in pins]
    js_ = [p[1] for p in pins]
    return (min(is_) + max(is_)) // 2, (min(js_) + max(js_)) // 2


def multipin_star(pins: Sequence[GCell], prefer: str = "HV") -> List[GCell]:
    if not pins:
        return []
    if len(pins) == 1:
        return [pins[0]]
    center = _bbox_center_gcell(pins)
    cells: set[GCell] = set()
    for pin in pins:
        for c in l_route(center, pin, prefer):
            cells.add(c)
    return sorted(cells)


def multipin_star_edges(pins: Sequence[GCell], prefer: str = "HV") -> List[Edge]:
    if len(pins) <= 1:
        return []
    center = _bbox_center_gcell(pins)
    edges: List[Edge] = []
    for pin in pins:
        edges.extend(path_to_edges(l_route(center, pin, prefer)))
    return edges


def _route_two_pin(
    a: GCell,
    b: GCell,
    mode: str,
    usage: Mapping[Edge, int],
    capacity: float,
    nx: int,
    ny: int,
) -> List[Edge]:
    m = mode.lower()
    if m == "maze":
        path = maze_route(a, b, usage, capacity, nx, ny)
        if path is None:
            path = l_route(a, b, "HV")
    elif m in ("z_hz", "z"):
        path = z_route(a, b, "HZ")
    elif m == "z_vh":
        path = z_route(a, b, "VH")
    elif m == "l_vh":
        path = l_route(a, b, "VH")
    else:
        path = l_route(a, b, "HV")
    return path_to_edges(path)


def route_nets(
    nets: Sequence[Sequence[str]],
    term: Mapping[str, GCell],
    mode: str = "l_hv",
    capacity: float = 2,
    nx: int = 4,
    ny: int = 2,
) -> Dict[Edge, int]:
    usage: Dict[Edge, int] = {}
    for net in nets:
        pins = [term[c] for c in net if c in term]
        if len(pins) < 2:
            continue
        if len(pins) == 2:
            edges = _route_two_pin(pins[0], pins[1], mode, usage, capacity, nx, ny)
        else:
            edges = multipin_star_edges(pins, "HV" if "vh" not in mode.lower() else "VH")
        for e in edges:
            usage[e] = usage.get(e, 0) + 1
    return usage


def route_nets_with_routes(
    nets: Sequence[Sequence[str]],
    term: Mapping[str, GCell],
    mode: str = "l_hv",
    capacity: float = 2,
    nx: int = 4,
    ny: int = 2,
) -> tuple[Dict[int, List[Edge]], Dict[Edge, int]]:
    usage: Dict[Edge, int] = {}
    routes: Dict[int, List[Edge]] = {}
    for idx, net in enumerate(nets):
        pins = [term[c] for c in net if c in term]
        if len(pins) < 2:
            continue
        if len(pins) == 2:
            edges = _route_two_pin(pins[0], pins[1], mode, usage, capacity, nx, ny)
        else:
            edges = multipin_star_edges(pins, "HV" if "vh" not in mode.lower() else "VH")
        routes[idx] = edges
        for e in edges:
            usage[e] = usage.get(e, 0) + 1
    return routes, usage


def edge_overflow(usage: Mapping[Edge, int], capacity: float) -> dict:
    cap = float(capacity)
    per: Dict[Edge, float] = {}
    total = 0.0
    max_ov = 0.0
    count = 0
    for e, u in usage.items():
        ov = max(0.0, float(u) - cap)
        per[e] = ov
        total += ov
        if ov > max_ov:
            max_ov = ov
        if ov > 0:
            count += 1
    return {"total": total, "max": max_ov, "count": count, "perEdge": per}


def _net_overflow(edges: Sequence[Edge], usage: Mapping[Edge, int], capacity: float) -> float:
    cap = float(capacity)
    return sum(max(0.0, float(usage.get(e, 0)) - cap) for e in edges)


def ripup_reroute(
    routes: Mapping[int, Sequence[Edge]],
    usage: MutableMapping[Edge, int],
    capacity: float,
    nets: Sequence[Sequence[str]],
    term: Mapping[str, GCell],
    nx: int = 4,
    ny: int = 2,
) -> Dict[Edge, int]:
    if not routes:
        return dict(usage)
    worst_idx = max(routes.keys(), key=lambda k: _net_overflow(routes[k], usage, capacity))
    for e in routes[worst_idx]:
        usage[e] = usage.get(e, 0) - 1
        if usage[e] <= 0:
            usage.pop(e, None)
    net = nets[worst_idx]
    pins = [term[c] for c in net if c in term]
    if len(pins) < 2:
        return dict(usage)
    if len(pins) == 2:
        path = maze_route(pins[0], pins[1], usage, capacity, nx, ny)
        new_edges = path_to_edges(path) if path else _route_two_pin(pins[0], pins[1], "l_vh", usage, capacity, nx, ny)
    else:
        new_edges = multipin_star_edges(pins, "VH")
    for e in new_edges:
        usage[e] = usage.get(e, 0) + 1
    return dict(usage)


def route_from_data(data: Mapping[str, Any], mode: str = "l_hv") -> Dict[Edge, int]:
    nx, ny, _, _, cap = gcell_geom(data)
    term = terminals(data["placement"], data)
    return route_nets(data["nets"], term, mode, cap, nx, ny)
