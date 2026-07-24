#!/usr/bin/env python3
"""Smoke tests for detailed routing solvers."""
from __future__ import annotations

import unittest
from pathlib import Path

from drutil import blockages, grid_size, load, pin_grid, terminals
from solvers import (
    astar_route,
    drc_spacing_lite,
    lee_maze,
    l_route_layers,
    path_track_usage,
    ripup_detailed,
    sequential_detailed,
    track_overflow,
)

ROOT = Path(__file__).resolve().parent
DATA = load(ROOT / "tiny_dr.json")


class TestDetailedRouting(unittest.TestCase):
    def test_pin_grid_clamped(self) -> None:
        nx, ny, _ = grid_size(DATA)
        self.assertEqual(pin_grid(1, 1, nx, ny), (1, 1))
        self.assertEqual(pin_grid(99, 99, nx, ny), (nx - 1, ny - 1))

    def test_lee_around_blockage(self) -> None:
        nx, ny, _ = grid_size(DATA)
        blocked = [(x, y) for x in range(5, 7) for y in range(2, 4)]
        path = lee_maze((4, 1), (7, 1), blocked=blocked, nx=nx, ny=ny)
        self.assertIsNotNone(path)
        assert path is not None
        self.assertEqual(path[0], (4, 1))
        self.assertEqual(path[-1], (7, 1))
        self.assertTrue(set(path).isdisjoint(set(blocked)))

    def test_astar_avoids_full_tracks(self) -> None:
        nx, ny, cap = grid_size(DATA)
        from drutil import h_edge

        hot = h_edge((1, 1), (2, 1))
        usage = {hot: 1}
        path = astar_route((1, 1), (3, 1), usage, cap, nx, ny)
        self.assertIsNotNone(path)
        assert path is not None
        keys = set()
        for k in range(len(path) - 1):
            a, b = path[k], path[k + 1]
            keys.add(h_edge(a, b) if a[1] == b[1] else ("M2", *__import__("drutil").v_edge(a, b)[1:]))
        self.assertNotIn(hot, keys)

    def test_l_route_layers_via(self) -> None:
        segs = l_route_layers((1, 1), (5, 4), "HV")
        self.assertTrue(any(s.get("via") for s in segs))
        self.assertEqual(segs[-1]["x"], 5)
        self.assertEqual(segs[-1]["y"], 4)

    def test_sequential_overflow_then_ripup(self) -> None:
        nx, ny, cap = grid_size(DATA)
        blocks = blockages(DATA)
        term = terminals(DATA["placement"], DATA)
        routes, usage = sequential_detailed(DATA["nets"], term, "l_hv", cap, nx, ny, blocks)
        before = track_overflow(usage, cap)["total"]
        self.assertGreater(before, 0.0)
        after_usage = ripup_detailed(routes, dict(usage), cap, term, DATA["nets"], nx, ny, blocks)
        after = track_overflow(after_usage, cap)["total"]
        self.assertLessEqual(after, before)

    def test_drc_spacing_catches_close_parallel(self) -> None:
        segs = [
            {"x": 1, "y": 2, "layer": "M1"},
            {"x": 2, "y": 2, "layer": "M1"},
            {"x": 1, "y": 3, "layer": "M1"},
            {"x": 2, "y": 3, "layer": "M1"},
        ]
        result = drc_spacing_lite(segs, min_dist=1)
        self.assertFalse(result["pass"])
        self.assertIsNotNone(result["violation"])

    def test_path_track_usage(self) -> None:
        segs = l_route_layers((1, 1), (4, 1), "HV")
        usage = path_track_usage(segs)
        self.assertGreater(len(usage), 0)


if __name__ == "__main__":
    unittest.main()
