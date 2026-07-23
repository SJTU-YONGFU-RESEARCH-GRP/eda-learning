"""Golden instances shared by Track A and browser labs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent

OUTLINE = {"w": 10, "h": 8}

MODULES: List[Dict[str, Any]] = [
    {"id": "A", "w": 3, "h": 2, "soft": True, "aspect_min": 0.5, "aspect_max": 2.0},
    {"id": "B", "w": 2, "h": 3, "soft": False},
    {"id": "C", "w": 2, "h": 2, "soft": False},
    {"id": "D", "w": 3, "h": 1, "soft": False},
    {"id": "E", "w": 2, "h": 2, "soft": False},
]

# Area sum = 23; outline = 80; deadspace = 57; density = 0.2875
GOLDEN_PACK = {
    "A": {"x": 0, "y": 0, "w": 3, "h": 2},
    "B": {"x": 3, "y": 0, "w": 2, "h": 3},
    "C": {"x": 5, "y": 0, "w": 2, "h": 2},
    "D": {"x": 0, "y": 2, "w": 3, "h": 1},
    "E": {"x": 7, "y": 0, "w": 2, "h": 2},
}

BAD_PACK = {
    "A": {"x": 0, "y": 0, "w": 3, "h": 2},
    "B": {"x": 3, "y": 0, "w": 2, "h": 3},
    "C": {"x": 5, "y": 0, "w": 2, "h": 2},
    "D": {"x": 0, "y": 2, "w": 3, "h": 1},
    "E": {"x": 9, "y": 0, "w": 2, "h": 2},  # overflows
}

OVERLAP_PACK = {
    "A": {"x": 0, "y": 0, "w": 3, "h": 2},
    "B": {"x": 3, "y": 0, "w": 2, "h": 3},
    "C": {"x": 5, "y": 0, "w": 2, "h": 2},
    "D": {"x": 0, "y": 2, "w": 3, "h": 1},
    "E": {"x": 5, "y": 0, "w": 2, "h": 2},
}

SOFT_A_PACK = {
    "A": {"x": 0, "y": 0, "w": 2, "h": 3},
    "B": {"x": 2, "y": 0, "w": 2, "h": 3},
    "C": {"x": 4, "y": 0, "w": 2, "h": 2},
    "D": {"x": 4, "y": 2, "w": 3, "h": 1},
    "E": {"x": 7, "y": 0, "w": 2, "h": 2},
}

MACRO_PACK = {
    "D": {"x": 0, "y": 0, "w": 3, "h": 1, "macro": True},
    "A": {"x": 0, "y": 1, "w": 3, "h": 2},
    "B": {"x": 3, "y": 0, "w": 2, "h": 3},
    "C": {"x": 5, "y": 0, "w": 2, "h": 2},
    "E": {"x": 7, "y": 0, "w": 2, "h": 2},
}

GOLDEN_POLISH = ["A", "D", "H", "B", "V", "C", "V", "E", "V"]

GOLDEN_BSTAR = {
    "id": "A",
    "left": {"id": "B", "left": {"id": "C", "left": {"id": "E"}}},
    "right": {"id": "D"},
}

GOLDEN_SP = {"pos": ["A", "B", "C", "E", "D"], "neg": ["D", "A", "B", "C", "E"]}

GOLDEN_PINS = [
    {"id": "P0", "side": "left", "offset": 2},
    {"id": "P1", "side": "bottom", "offset": 4},
    {"id": "P2", "side": "right", "offset": 3},
    {"id": "P3", "side": "top", "offset": 5},
]


def load_tiny_modules() -> Dict[str, Any]:
    return json.loads((ROOT / "tiny_modules.json").read_text(encoding="utf-8"))
