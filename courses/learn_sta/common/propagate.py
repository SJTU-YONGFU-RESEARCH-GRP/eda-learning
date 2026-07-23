"""Arrival / required / slack / critical path / incremental for learn_sta."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

from graph import levelize, sinks, sources, successors, predecessors
from timing_io import clone_timing, pin_ids

# Must match platform/assets/sta-core.js PROP_GOLDENS
PROP_GOLDENS = {
    "period": 10.0,
    "arrival": {
        "in": 0.0,
        "u1/A": 0.0,
        "u1/Y": 1.2,
        "u2/A": 1.5,
        "u2/Y": 3.0,
        "out": 3.2,
    },
    "required_setup": {
        "out": 10.0,
        "u2/Y": 9.8,
        "u2/A": 8.3,
        "u1/Y": 8.0,
        "u1/A": 6.8,
        "in": 6.8,
    },
    "setup_slack_out": 6.8,
    "hold_slack_out": 3.2,
    "critical_path": ["in", "u1/A", "u1/Y", "u2/A", "u2/Y", "out"],
    "incremental": {
        "edit_from": "u1/A",
        "edit_to": "u1/Y",
        "new_delay": 2.0,
        "arrival_out": 4.0,
        "setup_slack_out": 6.0,
        "invalidated": ["u1/Y", "u2/A", "u2/Y", "out"],
    },
    "multicycle": {
        "setup_cycles": 2,
        "required_out": 20.0,
        "setup_slack_out": 16.8,
    },
}


def _round6(x: float) -> float:
    return round(x + 0.0, 6)


def _topo(timing: Dict[str, Any]) -> Optional[List[str]]:
    levels = levelize(timing)
    if levels is None:
        return None
    return sorted(pin_ids(timing), key=lambda p: (levels[p], p))


def propagate_arrival(
    timing: Dict[str, Any],
    *,
    arrival_at: Optional[Dict[str, float]] = None,
    disable_arcs: Optional[Set[Tuple[str, str]]] = None,
) -> Optional[Dict[str, float]]:
    order = _topo(timing)
    if order is None:
        return None
    disabled = disable_arcs or set()
    arr: Dict[str, float] = {}
    for p in sources(timing):
        arr[p] = 0.0 if not arrival_at or p not in arrival_at else float(arrival_at[p])
    if arrival_at:
        for p, v in arrival_at.items():
            arr[p] = float(v)
    pred = predecessors(timing)
    for p in order:
        if p in arr:
            continue
        incoming = [(u, d, k) for u, d, k in pred.get(p, []) if (u, p) not in disabled]
        if not incoming:
            arr[p] = float(arrival_at.get(p, 0.0)) if arrival_at else 0.0
            continue
        best = max(arr[u] + d for u, d, _k in incoming if u in arr)
        arr[p] = _round6(best)
    return arr


def propagate_required(
    timing: Dict[str, Any],
    *,
    mode: str = "setup",
    setup_cycles: int = 1,
    required_at: Optional[Dict[str, float]] = None,
    disable_arcs: Optional[Set[Tuple[str, str]]] = None,
) -> Optional[Dict[str, float]]:
    order = _topo(timing)
    if order is None:
        return None
    disabled = disable_arcs or set()
    period = float(timing.get("clock", {}).get("period", 10.0))
    req: Dict[str, float] = {}
    for p in sinks(timing):
        if required_at and p in required_at:
            req[p] = float(required_at[p])
        elif mode == "hold":
            req[p] = 0.0
        else:
            req[p] = _round6(period * setup_cycles)
    if required_at:
        for p, v in required_at.items():
            req[p] = float(v)
    succ = successors(timing)
    for p in reversed(order):
        if p in req:
            continue
        outgoing = [(v, d, k) for v, d, k in succ.get(p, []) if (p, v) not in disabled]
        vals = [req[v] - d for v, d, _k in outgoing if v in req]
        if vals:
            req[p] = _round6(min(vals))
    return req


def setup_slack(arr: Dict[str, float], req: Dict[str, float], pin: str) -> Optional[float]:
    if pin not in arr or pin not in req:
        return None
    return _round6(req[pin] - arr[pin])


def hold_slack(arr: Dict[str, float], req_hold: Dict[str, float], pin: str) -> Optional[float]:
    if pin not in arr or pin not in req_hold:
        return None
    return _round6(arr[pin] - req_hold[pin])


def critical_path_to(
    timing: Dict[str, Any], arr: Dict[str, float], pin: str
) -> Optional[List[str]]:
    if pin not in arr:
        return None
    path = [pin]
    cur = pin
    pred = predecessors(timing)
    for _ in range(len(pin_ids(timing)) + 2):
        incoming = pred.get(cur, [])
        if not incoming:
            break
        best = None
        for u, d, _k in incoming:
            if u not in arr:
                continue
            cand = _round6(arr[u] + d)
            if abs(cand - arr[cur]) < 1e-9 and (best is None or arr[u] >= arr[best[0]]):
                best = (u, d)
        if best is None:
            break
        path.append(best[0])
        cur = best[0]
    path.reverse()
    return path


def fanout_cone(timing: Dict[str, Any], start: str) -> List[str]:
    succ = successors(timing)
    seen = {start}
    q = [start]
    while q:
        u = q.pop(0)
        for v, _d, _k in succ.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return sorted(seen, key=lambda p: (levelize(timing) or {}).get(p, 0))


def incremental_arrival(
    timing: Dict[str, Any],
    edit_from: str,
    edit_to: str,
    new_delay: float,
    base_arr: Dict[str, float],
) -> Tuple[Dict[str, Any], Dict[str, float], List[str]]:
    tt = clone_timing(timing)
    found = False
    for a in tt["arcs"]:
        if a["from"] == edit_from and a["to"] == edit_to:
            a["delay"] = float(new_delay)
            found = True
            break
    if not found:
        raise KeyError(f"missing arc {edit_from}->{edit_to}")
    invalidated = fanout_cone(tt, edit_to)
    arr = dict(base_arr)
    for p in invalidated:
        arr.pop(p, None)
    order = _topo(tt)
    assert order is not None
    pred = predecessors(tt)
    for p in order:
        if p not in invalidated and p in arr:
            continue
        if p in sources(tt) and p not in arr:
            arr[p] = 0.0
        incoming = pred.get(p, [])
        if not incoming:
            arr.setdefault(p, 0.0)
            continue
        best = max(arr[u] + d for u, d, _k in incoming if u in arr)
        arr[p] = _round6(best)
    return tt, arr, invalidated
