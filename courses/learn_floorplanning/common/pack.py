"""Packing representations: polish, B*-tree, sequence pair (Track A)."""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

Module = Mapping[str, Any]
Pack = Dict[str, Dict[str, Any]]


def eval_polish(tokens: Sequence[str], modules: Sequence[Module]) -> Dict[str, Any]:
    by_id = {m["id"]: m for m in modules}
    stack: List[Dict[str, Any]] = []
    for t in tokens:
        if t in ("H", "V"):
            if len(stack) < 2:
                raise ValueError("polish underflow")
            b = stack.pop()
            a = stack.pop()
            if t == "V":
                w = a["w"] + b["w"]
                h = max(a["h"], b["h"])
                kids = list(a["kids"]) + [
                    {**k, "x": k["x"] + a["w"]} for k in b["kids"]
                ]
            else:
                w = max(a["w"], b["w"])
                h = a["h"] + b["h"]
                kids = list(a["kids"]) + [
                    {**k, "y": k["y"] + a["h"]} for k in b["kids"]
                ]
            stack.append({"w": w, "h": h, "kids": kids})
        else:
            m = by_id[t]
            stack.append(
                {
                    "w": m["w"],
                    "h": m["h"],
                    "kids": [{"id": m["id"], "x": 0, "y": 0, "w": m["w"], "h": m["h"]}],
                }
            )
    if len(stack) != 1:
        raise ValueError("polish leftover")
    root = stack[0]
    pack = {
        k["id"]: {"x": k["x"], "y": k["y"], "w": k["w"], "h": k["h"]}
        for k in root["kids"]
    }
    return {"pack": pack, "w": root["w"], "h": root["h"]}


def pack_bstar(tree: Mapping[str, Any], modules: Sequence[Module]) -> Pack:
    by_id = {m["id"]: m for m in modules}
    pack: Pack = {}
    contour: List[Dict[str, float]] = []

    def contour_y(x1: float, x2: float) -> float:
        y = 0.0
        for seg in contour:
            if not (seg["x2"] <= x1 or seg["x1"] >= x2):
                y = max(y, seg["h"])
        return y

    def set_contour(x1: float, x2: float, h: float) -> None:
        nxt: List[Dict[str, float]] = []
        for seg in contour:
            if seg["x2"] <= x1 or seg["x1"] >= x2:
                nxt.append(seg)
            else:
                if seg["x1"] < x1:
                    nxt.append({"x1": seg["x1"], "x2": x1, "h": seg["h"]})
                if seg["x2"] > x2:
                    nxt.append({"x1": x2, "x2": seg["x2"], "h": seg["h"]})
        nxt.append({"x1": x1, "x2": x2, "h": h})
        nxt.sort(key=lambda s: s["x1"])
        contour[:] = nxt

    def place(node: Optional[Mapping[str, Any]], x: float) -> None:
        if not node:
            return
        m = by_id[node["id"]]
        y = contour_y(x, x + m["w"])
        pack[node["id"]] = {"x": x, "y": y, "w": m["w"], "h": m["h"]}
        set_contour(x, x + m["w"], y + m["h"])
        place(node.get("left"), x + m["w"])
        place(node.get("right"), x)

    place(tree, 0.0)
    return pack


def pack_sequence_pair(
    pos: Sequence[str], neg: Sequence[str], modules: Sequence[Module]
) -> Pack:
    by_id = {m["id"]: m for m in modules}
    pos_idx = {i: n for n, i in enumerate(pos)}
    neg_idx = {i: n for n, i in enumerate(neg)}
    pack: Pack = {
        i: {"x": 0.0, "y": 0.0, "w": by_id[i]["w"], "h": by_id[i]["h"]} for i in pos
    }
    order = sorted(pos, key=lambda i: pos_idx[i])
    for id_ in order:
        x = 0.0
        for other in pos:
            if other == id_:
                continue
            if pos_idx[other] < pos_idx[id_] and neg_idx[other] < neg_idx[id_]:
                x = max(x, pack[other]["x"] + pack[other]["w"])
        pack[id_]["x"] = x
    for id_ in order:
        y = 0.0
        for other in pos:
            if other == id_:
                continue
            if pos_idx[other] < pos_idx[id_] and neg_idx[other] > neg_idx[id_]:
                y = max(y, pack[other]["y"] + pack[other]["h"])
        pack[id_]["y"] = y
    return pack


def resize_soft(mod: Module, aspect: float) -> Dict[str, Any]:
    out = dict(mod)
    if not mod.get("soft"):
        return out
    area = float(mod["w"]) * float(mod["h"])
    w = max(1, round((area * aspect) ** 0.5))
    h = max(1, round(area / w))
    while w * h > area and w > 1:
        w -= 1
    while w * h < area:
        h += 1
    out["w"] = w
    out["h"] = h
    return out


def pack_hierarchical() -> Pack:
    left = {
        "A": {"x": 0, "y": 0, "w": 3, "h": 2},
        "B": {"x": 3, "y": 0, "w": 2, "h": 3},
    }
    right = {
        "C": {"x": 0, "y": 0, "w": 2, "h": 2},
        "D": {"x": 2, "y": 0, "w": 3, "h": 1},
        "E": {"x": 2, "y": 1, "w": 2, "h": 2},
    }
    pack = {i: dict(r) for i, r in left.items()}
    ox = 5
    for i, r in right.items():
        pack[i] = {"x": r["x"] + ox, "y": r["y"], "w": r["w"], "h": r["h"]}
    return pack
