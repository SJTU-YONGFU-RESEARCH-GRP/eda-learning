#!/usr/bin/env python3
"""Smoke tests aligned to legalization-core.js goldens."""
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
    ill = g["starter_illegal"]
    flo = g["starter_float"]
    rh = float(chip["rowH"])

    ok0, reason0 = check_legality(ill, cells, chip, {})
    assert not ok0 and "overlap" in reason0, reason0

    snapped = greedy_snap(flo, cells, chip, fixed_macros={})
    assert snapped["A"] == {"x": 4.0, "y": 2.0}
    assert snapped["B"] == {"x": 4.0, "y": 2.0}
    ok_s, _ = check_legality(snapped, cells, chip, {})
    assert not ok_s, "float snap should still overlap A/B"

    cleared = overlap_remove(ill, cells, chip, fixed_macros={})
    ok1, reason1 = check_legality(cleared, cells, chip, {})
    assert ok1, reason1
    assert total_displacement(ill, cleared) == 6
    assert total_hpwl(nets, cleared, cells=cells, row_h=rh) == 32
    assert cleared["B"] == {"x": 6.0, "y": 2.0}
    assert cleared["C"] == {"x": 8.0, "y": 2.0}

    ab = abacus_lite(ill, cells, chip, fixed_macros={})
    ok2, reason2 = check_legality(ab, cells, chip, {})
    assert ok2, reason2
    assert total_displacement(ill, ab) == 4
    assert total_hpwl(nets, ab, cells=cells, row_h=rh) == 38
    assert ab["B"]["y"] == 0 and ab["C"]["y"] == 4

    tr = tetris_lite(ill, cells, chip, fixed_macros={})
    ok3, reason3 = check_legality(tr, cells, chip, {})
    assert ok3, reason3
    assert total_displacement(ill, tr) == 6
    assert total_hpwl(nets, tr, cells=cells, row_h=rh) == 32

    ab_m = abacus_lite(ill, cells, chip, fixed_macros=g["fixed_macros"])
    ok4, reason4 = check_legality(ab_m, cells, chip, g["fixed_macros"])
    assert ok4, reason4
    assert ab_m["D"] == {"x": 8.0, "y": 4.0}
    assert total_displacement(ill, ab_m) == 4

    cost1 = 38 + 1 * 4
    cost5 = 38 + 5 * 4
    assert cost1 == 42 and cost5 == 58

    print(
        "ok goldens: snap still illegal; overlap/tetris disp=6 hpwl=32; "
        "abacus disp=4 hpwl=38; macro D locked; cost 42/58"
    )


if __name__ == "__main__":
    main()
