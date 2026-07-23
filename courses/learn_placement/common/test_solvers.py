#!/usr/bin/env python3
"""Golden checks for learn_placement common solvers."""
from __future__ import annotations

from pathlib import Path

from placementutil import (
    FORCE_HPWL_AFTER,
    GOLDEN_HPWL,
    GOLDEN_TIMING_HPWL,
    QUADRATIC_HPWL_AFTER,
    SA_HPWL_AFTER,
    STARTER_HPWL,
    STARTER_TIMING_HPWL,
    density_bins,
    load_place,
    near,
    round1,
    timing_weighted_hpwl,
    total_hpwl,
)
from solvers import force_directed_place, quadratic_place, sa_place

ROOT = Path(__file__).resolve().parent
g = load_place(ROOT / "tiny_place.json")


def main() -> None:
    starter = g["starter"]
    golden = g["golden"]
    nets = g["nets"]
    cells = g["cells"]
    weights = g["net_weights"]

    assert total_hpwl(nets, starter) == STARTER_HPWL
    assert total_hpwl(nets, golden) == GOLDEN_HPWL
    assert timing_weighted_hpwl(nets, starter, weights) == STARTER_TIMING_HPWL
    assert timing_weighted_hpwl(nets, golden, weights) == GOLDEN_TIMING_HPWL

    force = force_directed_place(starter, cells, nets)
    assert near(round1(total_hpwl(nets, force)), FORCE_HPWL_AFTER, 0.15), total_hpwl(nets, force)

    quad = quadratic_place(starter, cells, nets, fixed=g["fixed_pads"])
    assert near(total_hpwl(nets, quad), QUADRATIC_HPWL_AFTER, 0.15), total_hpwl(nets, quad)

    sa = sa_place(starter, cells, nets, seed=42)
    assert near(round1(sa["hpwl"]), SA_HPWL_AFTER, 0.15), sa["hpwl"]

    dens = density_bins(starter, capacity=1)
    assert dens["overflow"] == 2

    print(
        "ok goldens: HPWL 52->14, timing 116->30, "
        f"force~{round1(total_hpwl(nets, force))}, "
        f"quad={total_hpwl(nets, quad)}, "
        f"SA~{round1(sa['hpwl'])}"
    )


if __name__ == "__main__":
    main()
