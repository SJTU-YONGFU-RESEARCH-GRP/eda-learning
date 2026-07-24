"""Detailed routing solvers (Track A)."""
from __future__ import annotations

import heapq
from collections import deque
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence, Tuple

from drutil import (
    Grid,
    Seg,
    blockages,
    cell_blocked,
    grid_size,
    h_edge,
    load,
    neighbors4,
    pin_grid,
    pin_grid_from_data,
    terminals,
    track_key,
    v_edge,
)

TrackKey = Tuple[str, Grid, Grid]


def lee_maze(
    start: Grid,
    goal: Grid,
    blocked: Sequence[Grid] | None = None,
    nx: int = 12,
    ny: int = 8,
) -> Optional[List[Grid]]:
    if start == goal:
        return [start]
    block_set = set(blocked or ())
    if start in block_set or goal in block_set:
        return None
    queue: deque[tuple[Grid, List[Grid]]] = deque([(start, [start])])
    visited = {start}
    while queue:
        cur, path = queue.popleft()
        for nb in neighbors4(cur[0], cur[1], nx, ny):
            if nb in block_set:
                continue
            if nb == goal:
                return path + [nb]
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, path + [nb]))
    return None


def _astar_cost(usage: Mapping[TrackKey, int], cap: float, layer: str, a: Grid, b: Grid) -> float:
    key = track_key(layer, a, b)
    u = usage.get(key, 0)
    if u >= cap:
        return 1.0 + 10.0 * (u - cap + 1)
    return 1.0


def astar_route(
    start: Grid,
    goal: Grid,
    usage: Mapping[TrackKey, int],
    cap: float,
    nx: int = 12,
    ny: int = 8,
    blocks: Sequence[tuple[int, int, int, int]] = (),
) -> Optional[List[Grid]]:
    if start == goal:
        return [start]
    if cell_blocked(start[0], start[1], blocks) or cell_blocked(goal[0], goal[1], blocks):
        return None

    def h(g: Grid) -> float:
        return abs(g[0] - goal[0]) + abs(g[1] - goal[1])

    open_heap: list[tuple[float, float, Grid, List[Grid]]] = [(h(start), 0.0, start, [start])]
    best_g: Dict[Grid, float] = {start: 0.0}
    while open_heap:
        _, g_cost, cur, path = heapq.heappop(open_heap)
        if g_cost > best_g.get(cur, float("inf")):
            continue
        if cur == goal:
            return path
        gx, gy = cur
        for dx, dy, layer in ((1, 0, "M1"), (-1, 0, "M1"), (0, 1, "M2"), (0, -1, "M2")):
            nb = (gx + dx, gy + dy)
            if not (0 <= nb[0] < nx and 0 <= nb[1] < ny):
                continue
            if cell_blocked(nb[0], nb[1], blocks):
                continue
            step = _astar_cost(usage, cap, layer, cur, nb)
            ng = g_cost + step
            if ng < best_g.get(nb, float("inf")):
                best_g[nb] = ng
                heapq.heappush(open_heap, (ng + h(nb), ng, nb, path + [nb]))
    return None


def l_route_layers(start: Grid, goal: Grid, prefer: str = "HV") -> List[Seg]:
    """L-route with H on M1, V on M2; via at bend."""
    if start == goal:
        return [{"x": start[0], "y": start[1], "layer": "M1"}]
    sx, sy = start
    gx, gy = goal
    segs: List[Seg] = [{"x": sx, "y": sy, "layer": "M1"}]
    if prefer.upper() == "VH":
        y_step = 1 if gy > sy else -1
        for y in range(sy + y_step, gy + y_step, y_step):
            segs.append({"x": sx, "y": y, "layer": "M2"})
        if sy != gy:
            segs.append({"x": sx, "y": gy, "layer": "M1", "via": True})
        x_step = 1 if gx > sx else -1
        for x in range(sx + x_step, gx + x_step, x_step):
            segs.append({"x": x, "y": gy, "layer": "M1"})
    else:
        x_step = 1 if gx > sx else -1
        for x in range(sx + x_step, gx + x_step, x_step):
            segs.append({"x": x, "y": sy, "layer": "M1"})
        if sx != gx:
            segs.append({"x": gx, "y": sy, "layer": "M2", "via": True})
        y_step = 1 if gy > sy else -1
        for y in range(sy + y_step, gy + y_step, y_step):
            segs.append({"x": gx, "y": y, "layer": "M2"})
    if segs[-1]["x"] != gx or segs[-1]["y"] != gy:
        segs.append({"x": gx, "y": gy, "layer": segs[-1]["layer"]})
    return segs


def segments_to_path(segs: Sequence[Seg]) -> List[Grid]:
    return [(int(s["x"]), int(s["y"])) for s in segs]


def path_track_usage(segments: Sequence[Seg]) -> Dict[TrackKey, int]:
    usage: Dict[TrackKey, int] = {}
    path = segments_to_path(segments)
    for k in range(len(path) - 1):
        a, b = path[k], path[k + 1]
        if a[0] == b[0]:
            key = v_edge(a, b)
        else:
            key = h_edge(a, b)
        usage[key] = usage.get(key, 0) + 1
    return usage


def track_overflow(usage: Mapping[TrackKey, int], cap: float) -> dict:
    total = 0.0
    max_ov = 0.0
    count = 0
    per: Dict[TrackKey, float] = {}
    for e, u in usage.items():
        ov = max(0.0, float(u) - cap)
        per[e] = ov
        total += ov
        max_ov = max(max_ov, ov)
        if ov > 0:
            count += 1
    return {"total": total, "max": max_ov, "count": count, "perTrack": per}


def drc_spacing_lite(segments: Sequence[Seg], min_dist: int = 1) -> dict:
    """Fail if same-layer parallel segments on adjacent tracks are too close."""
    by_layer: Dict[str, List[Grid]] = {"M1": [], "M2": []}
    for s in segments:
        layer = str(s.get("layer", "M1"))
        by_layer.setdefault(layer, []).append((int(s["x"]), int(s["y"])))
    for layer, pts in by_layer.items():
        for i, a in enumerate(pts):
            for b in pts[i + 1 :]:
                if layer == "M1" and a[1] == b[1]:
                    dist = abs(a[0] - b[0])
                    if 0 < dist <= min_dist:
                        return {"pass": False, "violation": {"layer": layer, "a": a, "b": b, "dist": dist}}
                if layer == "M2" and a[0] == b[0]:
                    dist = abs(a[1] - b[1])
                    if 0 < dist <= min_dist:
                        return {"pass": False, "violation": {"layer": layer, "a": a, "b": b, "dist": dist}}
    return {"pass": True, "violation": None}


def _route_two_pin(
    a: Grid,
    b: Grid,
    mode: str,
    usage: Mapping[TrackKey, int],
    cap: float,
    nx: int,
    ny: int,
    blocks: Sequence[tuple[int, int, int, int]],
) -> List[Seg]:
    m = mode.lower()
    if m == "lee":
        blocked = [g for bx, by, bw, bh in blocks for g in _cells_in_rect(bx, by, bw, bh)]
        path = lee_maze(a, b, blocked=blocked, nx=nx, ny=ny)
        if path is None:
            path = [a, b]
        segs = []
        for k, p in enumerate(path):
            layer = "M1"
            if k > 0:
                layer = "M2" if path[k][0] == path[k - 1][0] else "M1"
            segs.append({"x": p[0], "y": p[1], "layer": layer})
        return segs
    if m == "l_hv":
        return l_route_layers(a, b, "HV")
    if m == "l_vh":
        return l_route_layers(a, b, "VH")
    path = astar_route(a, b, usage, cap, nx, ny, blocks)
    if path is None:
        return l_route_layers(a, b, "HV")
    segs: List[Seg] = []
    for k, p in enumerate(path):
        layer = "M1"
        if k > 0:
            layer = "M2" if path[k][0] == path[k - 1][0] else "M1"
        segs.append({"x": p[0], "y": p[1], "layer": layer})
    return segs


def _cells_in_rect(x: int, y: int, w: int, h: int) -> List[Grid]:
    return [(xi, yi) for xi in range(x, x + w) for yi in range(y, y + h)]


def _multipin_star_segments(pins: Sequence[Grid], prefer: str = "HV") -> List[Seg]:
    if len(pins) <= 1:
        return [{"x": pins[0][0], "y": pins[0][1], "layer": "M1"}] if pins else []
    is_ = [p[0] for p in pins]
    js_ = [p[1] for p in pins]
    center = ((min(is_) + max(is_)) // 2, (min(js_) + max(js_)) // 2)
    segs: List[Seg] = []
    for pin in pins:
        segs.extend(l_route_layers(center, pin, prefer))
    return segs


def sequential_detailed(
    nets: Sequence[Sequence[str]],
    term: Mapping[str, Grid],
    mode: str = "astar",
    cap: float = 1,
    nx: int = 12,
    ny: int = 8,
    blocks: Sequence[tuple[int, int, int, int]] = (),
) -> tuple[Dict[int, List[Seg]], Dict[TrackKey, int]]:
    usage: Dict[TrackKey, int] = {}
    routes: Dict[int, List[Seg]] = {}
    for idx, net in enumerate(nets):
        pins = [term[c] for c in net if c in term]
        if len(pins) < 2:
            continue
        if len(pins) == 2:
            segs = _route_two_pin(pins[0], pins[1], mode, usage, cap, nx, ny, blocks)
        else:
            segs = _multipin_star_segments(pins, "HV" if "vh" not in mode.lower() else "VH")
        routes[idx] = segs
        for e, c in path_track_usage(segs).items():
            usage[e] = usage.get(e, 0) + c
    return routes, usage


def _net_overflow(segs: Sequence[Seg], usage: Mapping[TrackKey, int], cap: float) -> float:
    local = path_track_usage(segs)
    return sum(max(0.0, float(usage.get(e, 0)) - cap) for e in local)


def ripup_detailed(
    routes: Mapping[int, Sequence[Seg]],
    usage: MutableMapping[TrackKey, int],
    cap: float,
    terminals_map: Mapping[str, Grid],
    nets: Sequence[Sequence[str]],
    nx: int = 12,
    ny: int = 8,
    blocks: Sequence[tuple[int, int, int, int]] = (),
) -> Dict[TrackKey, int]:
    if not routes:
        return dict(usage)
    worst_idx = max(routes.keys(), key=lambda k: _net_overflow(routes[k], usage, cap))
    for e, c in path_track_usage(routes[worst_idx]).items():
        usage[e] = usage.get(e, 0) - c
        if usage[e] <= 0:
            usage.pop(e, None)
    net = nets[worst_idx]
    pins = [terminals_map[c] for c in net if c in terminals_map]
    if len(pins) < 2:
        return dict(usage)
    if len(pins) == 2:
        segs = _route_two_pin(pins[0], pins[1], "astar", usage, cap, nx, ny, blocks)
    else:
        segs = _multipin_star_segments(pins, "VH")
    for e, c in path_track_usage(segs).items():
        usage[e] = usage.get(e, 0) + c
    routes_dict = dict(routes)
    routes_dict[worst_idx] = segs
    return dict(usage)


def route_from_data(data: Mapping[str, Any], mode: str = "astar") -> Dict[TrackKey, int]:
    nx, ny, cap = grid_size(data)
    blocks = blockages(data)
    term = terminals(data["placement"], data)
    _, usage = sequential_detailed(data["nets"], term, mode, cap, nx, ny, blocks)
    return usage
