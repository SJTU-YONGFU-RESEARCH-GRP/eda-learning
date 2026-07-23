#!/usr/bin/env python3
"""Golden checks for learn_partitioning common solvers."""
from __future__ import annotations

from pathlib import Path

from graphutil import BAD_SEED, GOLDEN_BIPART, cutsize, load_graph, parts_string
from solvers import fiduccia_mattheyses, kernighan_lin, summarize

ROOT = Path(__file__).resolve().parent
g = load_graph(ROOT / "tiny_graph.json")


def main() -> None:
    assert cutsize(BAD_SEED, g["edges"]) == 12
    assert parts_string(BAD_SEED) == "AE|BCD"
    assert cutsize(GOLDEN_BIPART, g["edges"]) == 3

    kl = kernighan_lin(g["nodes"], g["edges"], BAD_SEED)
    assert cutsize(kl, g["edges"]) == 3, summarize(kl, g["edges"])

    fm = fiduccia_mattheyses(g["nodes"], g["edges"], BAD_SEED)
    assert cutsize(fm, g["edges"]) == 3, summarize(fm, g["edges"])
    print("ok goldens: seed=12, KL/FM -> cut=3")


if __name__ == "__main__":
    main()
