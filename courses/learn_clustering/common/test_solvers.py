"""Smoke tests for learn_clustering common solvers."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "common"))

from advanced import (  # noqa: E402
    congestion_aware_partition,
    fiduccia_mattheyses,
    hyperedge_cut,
    hypergraph_greedy_cluster,
    label_propagation,
    load_hypergraph,
    multilevel_cluster,
    spectral_bisection,
    timing_aware_partition,
)
from graphutil import (  # noqa: E402
    affinity_edge_weight,
    affinity_shared_neighbors,
    cutsize,
    load_graph,
)
from solvers import greedy_pair_merge, kernighan_lin  # noqa: E402

GRAPH = ROOT / "module01-01-affinity-metrics" / "examples" / "tiny_graph.json"
SEED = ROOT / "module02-05-kernighan-lin" / "examples" / "seed_partition.json"
HYPER = ROOT / "module03-03-hypergraph-clustering" / "examples" / "tiny_hypergraph.json"
CONG = ROOT / "module04-01-congestion-aware-clustering" / "examples" / "congestion.json"
CRIT = ROOT / "module04-03-timing-aware-clustering" / "examples" / "criticality.json"


def _parts(asn):
    groups = {}
    for n, c in asn.items():
        groups.setdefault(c, set()).add(n)
    return sorted(map(frozenset, groups.values()))


class TestFoundations(unittest.TestCase):
    def test_affinity_edge_weight_order(self):
        g = load_graph(GRAPH)
        ranked = affinity_edge_weight(g["edges"])
        self.assertEqual(ranked[0][:2], ("A", "B"))
        self.assertEqual(ranked[0][2], 5.0)

    def test_affinity_shared_neighbors_boosts_dense_pairs(self):
        g = load_graph(GRAPH)
        top = {(u, v): w for u, v, w in affinity_shared_neighbors(g["nodes"], g["edges"])}
        self.assertAlmostEqual(top[("A", "B")], 6.0)

    def test_greedy_k2_golden(self):
        g = load_graph(GRAPH)
        asn = greedy_pair_merge(g["nodes"], g["edges"], g["sizes"], target_k=2)
        self.assertEqual(_parts(asn), [frozenset({"A", "B", "C"}), frozenset({"D", "E"})])
        self.assertAlmostEqual(cutsize(asn, g["edges"]), 3.0)


class TestClassic(unittest.TestCase):
    def test_lp(self):
        g = load_graph(GRAPH)
        asn, iters = label_propagation(g["nodes"], g["edges"])
        self.assertEqual(iters, 2)
        self.assertAlmostEqual(cutsize(asn, g["edges"]), 3.0)
        self.assertEqual(len(set(asn.values())), 2)

    def test_spectral(self):
        g = load_graph(GRAPH)
        asn, _order = spectral_bisection(g["nodes"], g["edges"], g["sizes"])
        self.assertAlmostEqual(cutsize(asn, g["edges"]), 3.0)
        self.assertEqual(_parts(asn), [frozenset({"A", "B", "C"}), frozenset({"D", "E"})])

    def test_kl(self):
        g = load_graph(GRAPH)
        seed = json.loads(SEED.read_text(encoding="utf-8"))["assignment"]
        self.assertAlmostEqual(cutsize(seed, g["edges"]), 12.0)
        final, history = kernighan_lin(g["nodes"], g["edges"], seed)
        self.assertAlmostEqual(cutsize(final, g["edges"]), 3.0)
        self.assertTrue(any(h.get("improved") for h in history))

    def test_fm(self):
        g = load_graph(GRAPH)
        seed = json.loads(SEED.read_text(encoding="utf-8"))["assignment"]
        final, history = fiduccia_mattheyses(g["nodes"], g["edges"], seed)
        self.assertAlmostEqual(cutsize(final, g["edges"]), 3.0)
        self.assertEqual(history[0]["cut_before"], 12.0)


class TestAdvanced(unittest.TestCase):
    def test_multilevel(self):
        g = load_graph(GRAPH)
        asn = multilevel_cluster(g["nodes"], g["edges"], g["sizes"], coarse_k=2)
        self.assertAlmostEqual(cutsize(asn, g["edges"]), 3.0)

    def test_hypergraph(self):
        h = load_hypergraph(HYPER)
        asn = hypergraph_greedy_cluster(h["nodes"], h["hyperedges"], h["sizes"], target_k=2)
        self.assertEqual(_parts(asn), [frozenset({"A", "B", "C"}), frozenset({"D", "E"})])
        self.assertAlmostEqual(hyperedge_cut(asn, h["hyperedges"]), 1.0)

    def test_congestion(self):
        g = load_graph(GRAPH)
        seed = json.loads(SEED.read_text(encoding="utf-8"))["assignment"]
        cong_raw = json.loads(CONG.read_text(encoding="utf-8"))
        cong = {}
        for e in cong_raw["edges"]:
            a, b = (e["u"], e["v"]) if e["u"] < e["v"] else (e["v"], e["u"])
            cong[(a, b)] = float(e["congestion"])
        _a0, plain0, pen0, _c0 = congestion_aware_partition(
            g["nodes"], g["edges"], seed, cong, 0.0
        )
        _a5, plain5, pen5, _c5 = congestion_aware_partition(
            g["nodes"], g["edges"], seed, cong, 5.0
        )
        self.assertAlmostEqual(plain0, 3.0)
        self.assertAlmostEqual(pen0, 9.0)
        self.assertAlmostEqual(plain5, 5.0)
        self.assertAlmostEqual(pen5, 0.0)

    def test_timing(self):
        g = load_graph(GRAPH)
        seed = json.loads(SEED.read_text(encoding="utf-8"))["assignment"]
        crit_raw = json.loads(CRIT.read_text(encoding="utf-8"))
        crit = {}
        for e in crit_raw["edges"]:
            a, b = (e["u"], e["v"]) if e["u"] < e["v"] else (e["v"], e["u"])
            crit[(a, b)] = float(e["criticality"])
        asn, plain, wcut = timing_aware_partition(g["nodes"], g["edges"], seed, crit)
        self.assertAlmostEqual(plain, 3.0)
        self.assertAlmostEqual(wcut, 7.0)
        self.assertEqual(_parts(asn), [frozenset({"A", "B", "C"}), frozenset({"D", "E"})])


if __name__ == "__main__":
    unittest.main()
