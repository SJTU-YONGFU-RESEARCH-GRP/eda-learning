"""Floorplanning metrics and legality (Track A)."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

Outline = Mapping[str, float]
Rect = Mapping[str, Any]
Pack = Mapping[str, Rect]


def outline_area(outline: Outline) -> float:
    return float(outline["w"]) * float(outline["h"])


def module_area_sum(modules: Sequence[Mapping[str, Any]]) -> float:
    return float(sum(float(m["w"]) * float(m["h"]) for m in modules))


def deadspace(outline: Outline, modules: Sequence[Mapping[str, Any]]) -> float:
    return outline_area(outline) - module_area_sum(modules)


def density(outline: Outline, modules: Sequence[Mapping[str, Any]]) -> float:
    return module_area_sum(modules) / outline_area(outline)


def rects_overlap(a: Rect, b: Rect) -> bool:
    """Interior overlap only; edge-touching is allowed."""
    return not (
        a["x"] + a["w"] <= b["x"]
        or b["x"] + b["w"] <= a["x"]
        or a["y"] + a["h"] <= b["y"]
        or b["y"] + b["h"] <= a["y"]
    )


def inside_outline(r: Rect, outline: Outline) -> bool:
    return (
        r["x"] >= 0
        and r["y"] >= 0
        and r["x"] + r["w"] <= outline["w"]
        and r["y"] + r["h"] <= outline["h"]
    )


def pack_to_list(pack: Pack) -> List[Dict[str, Any]]:
    return [{"id": i, **dict(r)} for i, r in pack.items()]


def is_legal_packing(pack: Pack, outline: Outline) -> bool:
    lst = pack_to_list(pack)
    for r in lst:
        if not inside_outline(r, outline):
            return False
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if rects_overlap(lst[i], lst[j]):
                return False
    return True


def legality_report(pack: Pack, outline: Outline) -> Dict[str, Any]:
    lst = pack_to_list(pack)
    for r in lst:
        if not inside_outline(r, outline):
            return {"legal": False, "reason": f"{r['id']} outside outline"}
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if rects_overlap(lst[i], lst[j]):
                return {
                    "legal": False,
                    "reason": f"{lst[i]['id']} overlaps {lst[j]['id']}",
                }
    return {"legal": True, "reason": "ok"}
