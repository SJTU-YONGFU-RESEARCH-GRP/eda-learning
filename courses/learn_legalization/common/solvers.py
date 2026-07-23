"""Reference legalization solvers for learn_legalization Track A (stubs aligned to JS API names)."""
from __future__ import annotations

from typing import Dict, Mapping, Optional, Sequence, Set

from legalizationutil import (
    cell_width,
    check_legality,
    clone_positions,
    nearest_row,
)

Placement = Dict[str, Dict[str, float]]


def _fixed_set(fixed_macros: Mapping[str, Mapping]) -> Set[str]:
    return set(fixed_macros.keys())


def greedy_snap(
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip: Mapping[str, float],
    *,
    fixed_macros: Optional[Mapping[str, Mapping]] = None,
) -> Placement:
    """Snap floats to nearest site x and row bottom y (skip fixed macros)."""
    fixed_macros = fixed_macros or {}
    fixed = _fixed_set(fixed_macros)
    rows = list(chip["rows"])
    w_chip = int(chip["W"])
    out = clone_positions(positions)

    for cid, p in out.items():
        if cid in fixed:
            out[cid] = {"x": float(fixed_macros[cid]["x"]), "y": float(fixed_macros[cid]["y"])}
            continue
        x = round(float(p["x"]))
        width = cell_width(cells, cid)
        x = max(0, min(x, w_chip - width))
        y = nearest_row(float(p["y"]), rows)
        out[cid] = {"x": float(x), "y": float(y)}
    return out


def overlap_remove(
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip: Mapping[str, float],
    *,
    fixed_macros: Optional[Mapping[str, Mapping]] = None,
) -> Placement:
    """Shift cells along each row left-to-right until intervals are disjoint."""
    fixed_macros = fixed_macros or {}
    fixed = _fixed_set(fixed_macros)
    w_chip = int(chip["W"])
    out = clone_positions(positions)
    rows = sorted({float(out[c]["y"]) for c in out})

    for row_y in rows:
        row_cells = [c for c in out if abs(float(out[c]["y"]) - row_y) < 1e-6]
        row_cells.sort(key=lambda c: float(out[c]["x"]))
        cursor = 0.0
        for cid in row_cells:
            if cid in fixed:
                cursor = max(cursor, float(out[cid]["x"]) + cell_width(cells, cid))
                continue
            width = cell_width(cells, cid)
            x = max(float(out[cid]["x"]), cursor)
            if x + width > w_chip:
                x = float(w_chip - width)
            out[cid] = {"x": x, "y": row_y}
            cursor = x + width
    return out


def abacus_lite(
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip: Mapping[str, float],
    *,
    fixed_macros: Optional[Mapping[str, Mapping]] = None,
) -> Placement:
    """Abacus-style row pack: sort by x, collapse clusters toward x=0 / obstacles."""
    fixed_macros = fixed_macros or {}
    out = overlap_remove(positions, cells, chip, fixed_macros=fixed_macros)
    w_chip = int(chip["W"])
    rows = sorted({float(out[c]["y"]) for c in out})

    for row_y in rows:
        obstacles: list[tuple[float, float]] = []
        for cid, meta in fixed_macros.items():
            if abs(float(out[cid]["y"]) - row_y) < 1e-6:
                obstacles.append((float(meta["x"]), float(meta["x"]) + cell_width(cells, cid)))
        obstacles.sort()

        movable = [c for c in out if abs(float(out[c]["y"]) - row_y) < 1e-6 and c not in fixed_macros]
        movable.sort(key=lambda c: float(out[c]["x"]))
        cursor = 0.0
        obs_i = 0
        for cid in movable:
            width = cell_width(cells, cid)
            while obs_i < len(obstacles) and obstacles[obs_i][1] <= cursor:
                cursor = obstacles[obs_i][1]
                obs_i += 1
            if obs_i < len(obstacles) and cursor + width > obstacles[obs_i][0]:
                cursor = obstacles[obs_i][1]
                obs_i += 1
            x = min(cursor, float(w_chip - width))
            out[cid] = {"x": float(x), "y": row_y}
            cursor = x + width
    return out


def tetris_lite(
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip: Mapping[str, float],
    *,
    fixed_macros: Optional[Mapping[str, Mapping]] = None,
    order: Optional[Sequence[str]] = None,
) -> Placement:
    """Tetris-style: leftmost free slot per row in processing order."""
    fixed_macros = fixed_macros or {}
    w_chip = int(chip["W"])
    rows = list(chip["rows"])
    out = clone_positions(positions)

    for cid in out:
        if cid not in fixed_macros:
            out[cid]["y"] = nearest_row(float(out[cid]["y"]), rows)

    proc = list(order) if order else sorted(out.keys(), key=lambda c: float(out[c]["x"]))

    for row_y in rows:
        occ = [False] * w_chip
        for cid, meta in fixed_macros.items():
            if abs(float(out[cid]["y"]) - row_y) < 1e-6:
                x0 = int(float(meta["x"]))
                for s in range(x0, min(w_chip, x0 + cell_width(cells, cid))):
                    occ[s] = True

        for cid in proc:
            if cid in fixed_macros or abs(float(out[cid]["y"]) - row_y) > 1e-6:
                continue
            width = cell_width(cells, cid)
            placed = False
            for x in range(w_chip - width + 1):
                if all(not occ[x + k] for k in range(width)):
                    out[cid] = {"x": float(x), "y": row_y}
                    for k in range(width):
                        occ[x + k] = True
                    placed = True
                    break
            if not placed:
                out[cid]["y"] = row_y
    return out


def summarize_legal(
    positions: Mapping[str, Mapping[str, float]],
    cells: Mapping[str, int],
    chip: Mapping[str, float],
    nets: Sequence[Sequence[str]],
    *,
    fixed_macros: Optional[Mapping[str, Mapping]] = None,
) -> str:
    ok, reason = check_legality(positions, cells, chip, fixed_macros)
    from legalizationutil import total_hpwl

    return f"legal={ok} ({reason}) HPWL={total_hpwl(nets, positions):.4g}"
