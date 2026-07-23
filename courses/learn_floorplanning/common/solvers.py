"""Reference solvers / helpers for learn_floorplanning Track A."""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence

from goldens import (
    GOLDEN_BSTAR,
    GOLDEN_PACK,
    GOLDEN_POLISH,
    GOLDEN_SP,
    MODULES,
    OUTLINE,
)
from metrics import deadspace, density, is_legal_packing, legality_report
from pack import (
    eval_polish,
    pack_bstar,
    pack_hierarchical,
    pack_sequence_pair,
    resize_soft,
)

TINY_NETS = [["A", "B"], ["B", "C"], ["C", "E"], ["A", "D"], ["D", "B"]]


def hpwl(pack: Mapping[str, Mapping[str, Any]], nets: Sequence[Sequence[str]] = TINY_NETS) -> float:
    total = 0.0
    for net in nets:
        xs: List[float] = []
        ys: List[float] = []
        for i in net:
            r = pack[i]
            xs.append(r["x"] + r["w"] / 2)
            ys.append(r["y"] + r["h"] / 2)
        total += max(xs) - min(xs) + (max(ys) - min(ys))
    return total


def cost(pack: Mapping[str, Mapping[str, Any]], outline: Mapping[str, float] = OUTLINE) -> float:
    legal = 0.0 if is_legal_packing(pack, outline) else 1000.0
    ds = deadspace(outline, MODULES)
    wire = hpwl(pack)
    bb_w = max(r["x"] + r["w"] for r in pack.values())
    bb_h = max(r["y"] + r["h"] for r in pack.values())
    aspect = abs(bb_w / bb_h - outline["w"] / outline["h"]) * 10
    return legal + ds * 0.1 + wire + aspect


def run_polish_golden() -> Dict[str, Any]:
    return eval_polish(GOLDEN_POLISH, MODULES)


def run_bstar_golden() -> Dict[str, Any]:
    return pack_bstar(GOLDEN_BSTAR, MODULES)


def run_sp_golden() -> Dict[str, Any]:
    return pack_sequence_pair(GOLDEN_SP["pos"], GOLDEN_SP["neg"], MODULES)


def summary() -> Dict[str, Any]:
    polish = run_polish_golden()
    return {
        "deadspace": deadspace(OUTLINE, MODULES),
        "density": density(OUTLINE, MODULES),
        "golden_legal": is_legal_packing(GOLDEN_PACK, OUTLINE),
        "polish_bb": (polish["w"], polish["h"]),
        "polish_legal": is_legal_packing(polish["pack"], OUTLINE),
        "bstar_legal": is_legal_packing(run_bstar_golden(), OUTLINE),
        "sp_legal": is_legal_packing(run_sp_golden(), OUTLINE),
        "hier_legal": is_legal_packing(pack_hierarchical(), OUTLINE),
        "golden_cost": cost(GOLDEN_PACK),
    }
