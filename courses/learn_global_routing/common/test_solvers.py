#!/usr/bin/env python3
"""Smoke tests for global routing solvers."""
from __future__ import annotations

import unittest
from pathlib import Path

from grutil import cell_gcell, edge_list, gcell_geom, load, terminals
from solvers import (
    edge_overflow,
    l_route,
    maze_route,
    multipin_star,
    path_to_edges,
    ripup_reroute,
    route_nets_with_routes,
    z_route,
)

ROOT = Path(__file__).resolve().parent
DATA = load(ROOT / "tiny_gr.json")


class TestGlobalRouting(unittest.TestCase):
    def test_gcell_index(self) -> None:
        nx, ny, cw, ch, _ = gcell_geom(DATA)
        self.assertEqual(cell_gcell(1, 1, nx, ny, cw, ch), (0, 0))
        self.assertEqual(cell_gcell(8, 5, nx, ny, cw, ch), (2, 1))

    def test_edge_list(self) -> None:
        nx, ny, _, _, _ = gcell_geom(DATA)
        edges = edge_list(nx, ny)
        self.assertEqual(len(edges), nx * (ny - 1) + ny * (nx - 1))
        self.assertIn(((0, 0), (1, 0)), edges)

    def test_l_route_hv(self) -> None:
        path = l_route((0, 0), (2, 1), "HV")
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 1))
        self.assertEqual(len(path_to_edges(path)), 3)

    def test_z_route(self) -> None:
        path = z_route((0, 0), (3, 1), "HZ")
        self.assertEqual(path[-1], (3, 1))
        self.assertGreaterEqual(len(path_to_edges(path)), 3)

    def test_sequential_l_overflow(self) -> None:
        nx, ny, _, _, cap = gcell_geom(DATA)
        term = terminals(DATA["placement"], DATA)
        usage = route_nets_with_routes(DATA["nets"], term, "l_hv", cap, nx, ny)[1]
        ov = edge_overflow(usage, cap)
        self.assertGreater(ov["total"], 0.0)
        self.assertGreater(ov["count"], 0)

    def test_maze_avoids_full_edges(self) -> None:
        nx, ny, _, _, cap = gcell_geom(DATA)
        blocked = {((0, 0), (1, 0)), ((1, 0), (2, 0))}
        usage = {e: 2 for e in blocked}
        path = maze_route((0, 0), (2, 0), usage, cap, nx, ny)
        self.assertIsNotNone(path)
        edges = set(path_to_edges(path))
        self.assertTrue(edges.isdisjoint(blocked))

    def test_maze_finds_detour(self) -> None:
        nx, ny, _, _, cap = gcell_geom(DATA)
        usage = {((0, 0), (1, 0)): 2}
        path = maze_route((0, 0), (1, 0), usage, cap, nx, ny)
        self.assertIsNotNone(path)
        self.assertNotIn(((0, 0), (1, 0)), set(path_to_edges(path)))

    def test_maze_blocked_returns_none(self) -> None:
        nx, ny, _, _, cap = gcell_geom(DATA)
        usage = {e: 2 for e in edge_list(nx, ny)}
        path = maze_route((0, 0), (3, 1), usage, cap, nx, ny)
        self.assertIsNone(path)

    def test_multipin_star(self) -> None:
        pins = [(0, 0), (2, 0), (0, 1), (2, 1)]
        cells = multipin_star(pins)
        self.assertIn((1, 0), cells)

    def test_ripup_reduces_overflow(self) -> None:
        nx, ny, _, _, cap = gcell_geom(DATA)
        term = terminals(DATA["placement"], DATA)
        routes, usage = route_nets_with_routes(DATA["nets"], term, "l_hv", cap, nx, ny)
        before = edge_overflow(usage, cap)["total"]
        after_usage = ripup_reroute(routes, dict(usage), cap, DATA["nets"], term, nx, ny)
        after = edge_overflow(after_usage, cap)["total"]
        self.assertLessEqual(after, before)


if __name__ == "__main__":
    unittest.main()
