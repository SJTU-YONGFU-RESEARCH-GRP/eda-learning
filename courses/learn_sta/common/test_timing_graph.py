#!/usr/bin/env python3
"""Golden checks for learn_sta timing-graph helpers."""
from __future__ import annotations

from pathlib import Path

from graph import (
    GOLDENS,
    arc_kind_counts,
    cell_delay_sum,
    levelize,
    path_delay_sum,
    sinks,
    sources,
    summarize,
    topo_order,
    with_cycle,
)
from timing_io import load_timing, pin_ids

ROOT = Path(__file__).resolve().parent
t = load_timing(ROOT / "tiny_timing.json")


def main() -> None:
    assert len(pin_ids(t)) == GOLDENS["pin_count"]
    assert len(t["arcs"]) == GOLDENS["arc_count"]
    kinds = arc_kind_counts(t)
    assert kinds.get("cell") == GOLDENS["cell_arcs"]
    assert kinds.get("net") == GOLDENS["net_arcs"]
    assert sources(t) == GOLDENS["sources"]
    assert sinks(t) == GOLDENS["sinks"]

    levels = levelize(t)
    assert levels is not None
    assert levels == GOLDENS["levels"]
    assert max(levels.values()) == GOLDENS["max_level"]
    assert topo_order(t) == GOLDENS["topo"]
    assert abs(path_delay_sum(t) - GOLDENS["path_delay"]) < 1e-9
    assert abs(cell_delay_sum(t) - GOLDENS["cell_delay_sum"]) < 1e-9

    cyclic = with_cycle(t)
    assert levelize(cyclic) is None
    assert summarize(cyclic)["acyclic"] is False

    print(
        "ok goldens: pins=6 arcs=5 levels 0..5 path_delay=3.2; "
        "cycle fails levelize"
    )


if __name__ == "__main__":
    main()
