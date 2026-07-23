"""Reference legalization solvers for learn_legalization Track A (ports of legalization-core.js)."""
from __future__ import annotations

from typing import Dict, List, Mapping, Optional, Sequence, Set, Tuple

from legalizationutil import cell_width, clone_positions, nearest_row

Placement = Dict[str, Dict[str, float]]


def _fixed_map(fixed_macros: Optional[Mapping[str, Mapping]]) -> Dict[str, Dict[str, float]]:
    fixed_macros = fixed_macros or {}
    out: Dict[str, Dict[str, float]] = {}
    for cid, meta in fixed_macros.items():
        out[cid] = {"x": float(meta["x"]), "y": float(meta["y"])}
    return out


def _snap_x(x: float, w: int, chip_w: int) -> float:
    s = round(x)
    return float(max(0, min(chip_w - w, s)))


def greedy_snap(
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip: Mapping[str, float],
    *,
    fixed_macros: Optional[Mapping[str, Mapping]] = None,
) -> Placement:
    """Snap floats to nearest site x and row bottom y (skip fixed macros)."""
    fixed = _fixed_map(fixed_macros)
    rows = list(chip["rows"])
    w_chip = int(chip["W"])
    out = clone_positions(positions)
    for cid, p in out.items():
        if cid in fixed:
            out[cid] = {"x": fixed[cid]["x"], "y": fixed[cid]["y"]}
            continue
        w = cell_width(cells, cid)
        out[cid] = {
            "x": _snap_x(float(p["x"]), w, w_chip),
            "y": float(nearest_row(float(p["y"]), rows)),
        }
    return out


def _intervals_overlap(a0: float, a1: float, b0: float, b1: float) -> bool:
    return a0 < b1 and b0 < a1


def _pack_row_avoiding(
    ids: Sequence[str],
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip_w: int,
    blocked: List[Tuple[float, float]],
) -> Dict[str, float]:
    sorted_ids = sorted(ids, key=lambda c: (float(positions[c]["x"]), c))
    blocked = sorted(blocked, key=lambda b: b[0])
    out: Dict[str, float] = {}
    cursor = 0.0
    for cid in sorted_ids:
        w = cell_width(cells, cid)
        x = max(cursor, _snap_x(float(positions[cid]["x"]), w, chip_w))
        moved = True
        while moved:
            moved = False
            for b0, b1 in blocked:
                if _intervals_overlap(x, x + w, b0, b1):
                    x = b1
                    moved = True
        if x + w > chip_w:
            x = float(max(0, chip_w - w))
        out[cid] = x
        cursor = x + w
        blocked = sorted(blocked + [(x, x + w)], key=lambda b: b[0])
    return out


def overlap_remove(
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip: Mapping[str, float],
    *,
    fixed_macros: Optional[Mapping[str, Mapping]] = None,
) -> Placement:
    """Snap, then per-row left pack keeping relative order (JS overlapRemoval)."""
    fixed = _fixed_map(fixed_macros)
    snapped = greedy_snap(positions, cells, chip, fixed_macros=fixed_macros)
    rows = list(chip["rows"])
    w_chip = int(chip["W"])
    by_row: List[List[str]] = [[] for _ in rows]
    for cid in snapped:
        if cid in fixed:
            continue
        y = float(snapped[cid]["y"])
        ri = min(range(len(rows)), key=lambda i: abs(rows[i] - y))
        by_row[ri].append(cid)

    out = clone_positions(snapped)
    for cid, fp in fixed.items():
        out[cid] = {"x": fp["x"], "y": fp["y"]}

    for ri, row_y in enumerate(rows):
        ids = by_row[ri]
        if not ids:
            continue
        blocked: List[Tuple[float, float]] = []
        for fid, fp in fixed.items():
            if abs(fp["y"] - row_y) < 1e-9:
                blocked.append((fp["x"], fp["x"] + cell_width(cells, fid)))
        placed = _pack_row_avoiding(ids, snapped, cells, w_chip, blocked)
        for cid in ids:
            out[cid] = {"x": placed[cid], "y": float(row_y)}
    return out


def abacus_lite(
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip: Mapping[str, float],
    *,
    fixed_macros: Optional[Mapping[str, Mapping]] = None,
) -> Placement:
    """Abacus-lite: process by increasing x; try each row; min L1 displacement (JS port)."""
    fixed = _fixed_map(fixed_macros)
    origin = clone_positions(positions)
    rows = list(chip["rows"])
    w_chip = int(chip["W"])
    order = sorted(
        [c for c in origin if c not in fixed],
        key=lambda c: (float(origin[c]["x"]), c),
    )
    placed: Placement = {cid: {"x": fp["x"], "y": fp["y"]} for cid, fp in fixed.items()}

    for cid in order:
        w = cell_width(cells, cid)
        best = None
        best_cost = float("inf")
        for row_y in rows:
            occupied = [
                (float(p["x"]), float(p["x"]) + cell_width(cells, oid))
                for oid, p in placed.items()
                if abs(float(p["y"]) - row_y) < 1e-9
            ]
            occupied.sort()
            prefer = _snap_x(float(origin[cid]["x"]), w, w_chip)

            def try_place(start: float) -> Optional[float]:
                xx = start
                for _ in range(w_chip + 2):
                    hit = None
                    for o0, o1 in occupied:
                        if _intervals_overlap(xx, xx + w, o0, o1):
                            hit = (o0, o1)
                            break
                    if hit is None:
                        return xx if xx + w <= w_chip else None
                    xx = hit[1]
                return None

            cand = try_place(prefer)
            if cand is None:
                cand = try_place(0.0)
            if cand is None:
                continue
            cost = abs(cand - float(origin[cid]["x"])) + abs(row_y - float(origin[cid]["y"]))
            if cost < best_cost - 1e-12 or (
                abs(cost - best_cost) <= 1e-12 and (best is None or cand < best["x"])
            ):
                best_cost = cost
                best = {"x": float(cand), "y": float(row_y)}
        if best is None:
            best = {
                "x": _snap_x(float(origin[cid]["x"]), w, w_chip),
                "y": float(nearest_row(float(origin[cid]["y"]), rows)),
            }
        placed[cid] = best

    out: Placement = {}
    snapped = greedy_snap(positions, cells, chip, fixed_macros=fixed_macros)
    for cid in origin:
        out[cid] = placed.get(cid) or snapped[cid]
    return out


def tetris_lite(
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip: Mapping[str, float],
    *,
    fixed_macros: Optional[Mapping[str, Mapping]] = None,
    order: Optional[Sequence[str]] = None,
) -> Placement:
    """Tetris-lite = overlap_remove (JS tetrisLegalize)."""
    del order  # unused; kept for API compatibility
    return overlap_remove(positions, cells, chip, fixed_macros=fixed_macros)


def legalize_cost(
    positions: Mapping[str, Mapping[str, float]],
    origin: Mapping[str, Mapping[str, float]],
    nets: Sequence[Sequence[str]],
    *,
    lambda_: float = 1.0,
) -> float:
    from legalizationutil import total_displacement, total_hpwl

    return total_hpwl(nets, positions) + lambda_ * total_displacement(origin, positions)
