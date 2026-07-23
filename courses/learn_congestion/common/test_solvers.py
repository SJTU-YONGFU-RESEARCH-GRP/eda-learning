#!/usr/bin/env python3
"""Smoke tests for congestion solvers."""
from __future__ import annotations

import unittest
from pathlib import Path

from congestionutil import cell_gcell, gcell_geom, load
from solvers import (
    congestion_map,
    overflow_metrics,
    placement_feedback_lite,
    probabilistic_demand,
    rudy_demand,
)

ROOT = Path(__file__).resolve().parent
DATA = load(ROOT / "tiny_cong.json")


class TestCongestion(unittest.TestCase):
    def test_gcell_index(self):
        nx, ny, cw, ch, _ = gcell_geom(DATA)
        self.assertEqual(cell_gcell(1, 1, nx, ny, cw, ch), (0, 0))
        self.assertEqual(cell_gcell(8, 5, nx, ny, cw, ch), (2, 1))

    def test_congested_max_overflow_higher(self):
        # Spread nets paint many tiles (high total); cluster spikes max overflow.
        _, _, _, _, cap = gcell_geom(DATA)
        a = overflow_metrics(rudy_demand(DATA["placement"], DATA), cap)["max"]
        b = overflow_metrics(rudy_demand(DATA["congested_seed"], DATA), cap)["max"]
        self.assertGreaterEqual(b, a)
        self.assertGreater(b, 0)

    def test_feedback_reduces(self):
        _, _, _, _, cap = gcell_geom(DATA)
        seed = DATA["congested_seed"]
        before = overflow_metrics(rudy_demand(seed, DATA), cap)["total"]
        after_pos = placement_feedback_lite(seed, DATA)
        after = overflow_metrics(rudy_demand(after_pos, DATA), cap)["total"]
        self.assertLess(after, before)

    def test_prob_runs(self):
        d = probabilistic_demand(DATA["placement"], DATA)
        self.assertEqual(len(d), 4)
        self.assertEqual(len(d[0]), 2)
        self.assertGreater(sum(sum(col) for col in d), 0)

    def test_cong_ratio(self):
        demand = rudy_demand(DATA["placement"], DATA)
        cong = congestion_map(demand, 2.0)
        self.assertAlmostEqual(cong[0][0], demand[0][0] / 2.0)


if __name__ == "__main__":
    unittest.main()
