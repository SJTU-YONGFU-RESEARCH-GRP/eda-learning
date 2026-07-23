#!/usr/bin/env python3
"""Smoke tests for learn_legalization common solvers (goldens pending JS alignment)."""
from __future__ import annotations

from pathlib import Path

from legalizationutil import check_legality, load_legal, total_displacement, total_hpwl
from solvers import abacus_lite, greedy_snap, overlap_remove, tetris_lite

ROOT = Path(__file__).resolve().parent
g = load_legal(ROOT / "tiny_legal.json")


def main() -> None:
    chip = g["chip"]
    cells = g["cells"]
    nets = g["nets"]
    fixed = g["fixed_macros"]
    starter_illegal = g["starter_illegal"]
    starter_float = g["starter_float"]

    ok0, _ = check_legality(starter_illegal, cells, chip, fixed)
    assert not ok0, "starter_illegal should be illegal"

    snapped = greedy_snap(starter_float, cells, chip, fixed_macros=fixed)
    for cid, p in snapped.items():
        assert abs(p["x"] - round(p["x"])) < 1e-6
        assert p["y"] in chip["rows"] or any(abs(p["y"] - r) < 1e-6 for r in chip["rows"])

    cleared = overlap_remove(starter_illegal, cells, chip, fixed_macros=fixed)
    ok1, reason1 = check_legality(cleared, cells, chip, fixed)
    assert ok1, reason1

    ab = abacus_lite(starter_illegal, cells, chip, fixed_macros=fixed)
    ok2, reason2 = check_legality(ab, cells, chip, fixed)
    assert ok2, reason2

    tr = tetris_lite(snapped, cells, chip, fixed_macros=fixed)
    ok3, reason3 = check_legality(tr, cells, chip, fixed)
    assert ok3, reason3

    disp = total_displacement(starter_float, snapped, fixed=fixed.keys())
    assert disp >= 0

    hpwl0 = total_hpwl(nets, starter_float)
    hpwl1 = total_hpwl(nets, tr)
    assert hpwl0 >= 0 and hpwl1 >= 0

    print(
        f"ok smoke: illegal starter fails; overlap_remove legal; "
        f"abacus legal; tetris legal; disp={disp:.2f}; hpwl float={hpwl0:.2f} tetris={hpwl1:.2f}"
    )


if __name__ == "__main__":
    main()
