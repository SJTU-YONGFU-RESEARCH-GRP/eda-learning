"""Reference solvers for learn_clustering Track A."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from graphutil import (
    Edge,
    adjacency,
    affinity_edge_weight,
    affinity_shared_neighbors,
    balance_ratio,
    contract_pair,
    cutsize,
    load_graph,
)


def greedy_pair_merge(
    nodes: List[str],
    edges: List[Edge],
    sizes: Dict[str, float],
    target_k: int,
    capacity: Optional[float] = None,
) -> Dict[str, str]:
    """
    Greedy heaviest-edge agglomerative merge down to target_k clusters.
    If capacity is set, skip merges that would exceed it.
    Returns assignment: original_node -> cluster_id (final supernode name).
    """
    members: Dict[str, set[str]] = {n: {n} for n in nodes}
    cur_nodes = list(nodes)
    cur_edges = list(edges)
    cur_sizes = dict(sizes)
    next_id = 0

    while len(cur_nodes) > target_k:
        ranked = affinity_edge_weight(cur_edges)
        picked = None
        for u, v, w in ranked:
            if capacity is not None and cur_sizes[u] + cur_sizes[v] > capacity + 1e-12:
                continue
            picked = (u, v, w)
            break
        if picked is None:
            break
        u, v, _ = picked
        new_id = f"C{next_id}"
        next_id += 1
        members[new_id] = members[u] | members[v]
        del members[u]
        del members[v]
        cur_nodes, cur_edges, cur_sizes = contract_pair(
            cur_nodes, cur_edges, cur_sizes, u, v, new_id
        )

    assignment: Dict[str, str] = {}
    for cid, origs in members.items():
        for n in origs:
            assignment[n] = cid
    return assignment


def _d_values(
    side: Dict[str, str], adj: Dict[str, Dict[str, float]], side_a: str, side_b: str
) -> Dict[str, float]:
    """D(v) = external - internal connectivity."""
    d: Dict[str, float] = {}
    for v, s in side.items():
        ext = 0.0
        inn = 0.0
        for nbr, w in adj.get(v, {}).items():
            if side[nbr] == s:
                inn += w
            else:
                ext += w
        d[v] = ext - inn
    return d


def kernighan_lin(
    nodes: List[str],
    edges: List[Edge],
    initial: Dict[str, str],
    max_passes: int = 10,
) -> Tuple[Dict[str, str], List[dict]]:
    """
    Full KL bipartition refinement with pair swaps, locking, and rollback.

    `initial` maps node -> '0' or '1'. Sizes need not be equal (e.g. 3 vs 2),
    but each swap keeps the same cardinality on each side.
    """
    sides = {n: str(initial[n]) for n in nodes}
    if set(sides.values()) - {"0", "1"}:
        raise ValueError("KL requires bipartition labels '0' and '1'")
    adj = adjacency(edges)
    history: List[dict] = []

    for pass_i in range(max_passes):
        locked: set[str] = set()
        work = dict(sides)
        d = _d_values(work, adj, "0", "1")
        sequence: List[Tuple[str, str, float]] = []
        cum = 0.0
        best_cum = 0.0
        best_k = 0

        while True:
            a_free = [n for n, s in work.items() if s == "0" and n not in locked]
            b_free = [n for n, s in work.items() if s == "1" and n not in locked]
            if not a_free or not b_free:
                break

            best_pair: Optional[Tuple[str, str, float]] = None
            for a in a_free:
                for b in b_free:
                    cab = adj.get(a, {}).get(b, 0.0)
                    g = d[a] + d[b] - 2.0 * cab
                    cand = (a, b, g)
                    if best_pair is None or (g, a, b) > (best_pair[2], best_pair[0], best_pair[1]):
                        best_pair = cand
            assert best_pair is not None
            a, b, g = best_pair
            cum += g
            sequence.append((a, b, g))
            if cum > best_cum + 1e-12:
                best_cum = cum
                best_k = len(sequence)

            # swap + lock
            work[a], work[b] = work[b], work[a]
            locked.add(a)
            locked.add(b)
            d = _d_values(work, adj, "0", "1")

        if best_k <= 0 or best_cum <= 1e-12:
            history.append(
                {
                    "pass": pass_i,
                    "best_k": best_k,
                    "best_cum": best_cum,
                    "cut_before": cutsize(sides, edges),
                    "cut_after": cutsize(sides, edges),
                    "improved": False,
                }
            )
            break

        # apply first best_k swaps from the pass start
        applied = dict(sides)
        for a, b, _ in sequence[:best_k]:
            applied[a], applied[b] = applied[b], applied[a]
        cut_before = cutsize(sides, edges)
        cut_after = cutsize(applied, edges)
        history.append(
            {
                "pass": pass_i,
                "best_k": best_k,
                "best_cum": best_cum,
                "cut_before": cut_before,
                "cut_after": cut_after,
                "swaps": [(a, b, g) for a, b, g in sequence[:best_k]],
                "improved": cut_after + 1e-12 < cut_before,
            }
        )
        sides = applied
        if not history[-1]["improved"]:
            break

    return sides, history


def run_affinity_report(graph_path: str) -> None:
    g = load_graph(graph_path)
    print("affinity edge-weight (desc):")
    for u, v, w in affinity_edge_weight(g["edges"]):
        print(f"  {u}-{v}: {w}")
    print("affinity shared-neighbors+edge (desc):")
    for u, v, w in affinity_shared_neighbors(g["nodes"], g["edges"]):
        print(f"  {u}-{v}: {w}")


def run_greedy_report(
    graph_path: str, target_k: int = 2, capacity: Optional[float] = None
) -> None:
    g = load_graph(graph_path)
    run_affinity_report(graph_path)
    assignment = greedy_pair_merge(
        g["nodes"], g["edges"], g["sizes"], target_k=target_k, capacity=capacity
    )
    cut = cutsize(assignment, g["edges"])
    bal = balance_ratio(assignment, g["sizes"])
    print(f"assignment: {dict(sorted(assignment.items()))}")
    print(f"cutsize: {cut}")
    print(f"balance_ratio: {bal:.4f}")
    print(f"clusters: {sorted(set(assignment.values()))}")


def run_kl_report(graph_path: str, seed_path: str) -> None:
    g = load_graph(graph_path)
    seed = json.loads(Path(seed_path).read_text(encoding="utf-8"))
    initial = {n: str(seed["assignment"][n]) for n in g["nodes"]}
    before = cutsize(initial, g["edges"])
    final, history = kernighan_lin(g["nodes"], g["edges"], initial)
    after = cutsize(final, g["edges"])
    print(f"seed assignment: {dict(sorted(initial.items()))}")
    print(f"cutsize before: {before}")
    for h in history:
        print(
            f"  pass {h['pass']}: best_k={h['best_k']} best_cum={h['best_cum']:.4f} "
            f"cut {h['cut_before']} -> {h['cut_after']}"
        )
        if h.get("swaps"):
            print(f"    swaps: {h['swaps']}")
    print(f"final assignment: {dict(sorted(final.items()))}")
    print(f"cutsize after: {after}")
    print(f"balance_ratio: {balance_ratio(final, g['sizes']):.4f}")


if __name__ == "__main__":
    import argparse

    from advanced import (
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

    p = argparse.ArgumentParser()
    p.add_argument("graph", type=Path)
    p.add_argument(
        "--mode",
        choices=[
            "greedy",
            "affinity",
            "kl",
            "fm",
            "lp",
            "spectral",
            "multilevel",
            "hyper",
            "cong",
            "timing",
        ],
        default="greedy",
    )
    p.add_argument("--k", type=int, default=2)
    p.add_argument("--capacity", type=float, default=None)
    p.add_argument("--seed", type=Path, default=None)
    p.add_argument("--cong", type=Path, default=None)
    p.add_argument("--crit", type=Path, default=None)
    p.add_argument("--lambda", dest="lam", type=float, default=1.0)
    args = p.parse_args()
    gpath = str(args.graph)

    if args.mode == "affinity":
        run_affinity_report(gpath)
    elif args.mode == "kl":
        if args.seed is None:
            raise SystemExit("--seed is required for --mode kl")
        run_kl_report(gpath, str(args.seed))
    elif args.mode == "lp":
        g = load_graph(gpath)
        asn, iters = label_propagation(g["nodes"], g["edges"])
        print(f"iters_to_stable: {iters}")
        print(f"labels: {dict(sorted(asn.items()))}")
        print(f"cutsize: {cutsize(asn, g['edges'])}")
        print(f"num_clusters: {len(set(asn.values()))}")
    elif args.mode == "spectral":
        g = load_graph(gpath)
        asn, order = spectral_bisection(g["nodes"], g["edges"], g["sizes"])
        print("fiedler_order:")
        for n, val in order:
            print(f"  {n}: {val:.6f}")
        print(f"assignment: {dict(sorted(asn.items()))}")
        print(f"cutsize: {cutsize(asn, g['edges'])}")
    elif args.mode == "fm":
        if args.seed is None:
            raise SystemExit("--seed is required for --mode fm")
        g = load_graph(gpath)
        seed = json.loads(Path(args.seed).read_text(encoding="utf-8"))["assignment"]
        initial = {n: str(seed[n]) for n in g["nodes"]}
        before = cutsize(initial, g["edges"])
        final, history = fiduccia_mattheyses(g["nodes"], g["edges"], initial)
        print(f"cutsize before: {before}")
        for h in history:
            print(
                f"  pass {h['pass']}: best_k={h['best_k']} best_cum={h['best_cum']:.4f} "
                f"cut {h['cut_before']} -> {h['cut_after']}"
            )
            if h.get("moves"):
                print(f"    moves: {h['moves']}")
        print(f"final assignment: {dict(sorted(final.items()))}")
        print(f"cutsize after: {cutsize(final, g['edges'])}")
    elif args.mode == "multilevel":
        g = load_graph(gpath)
        asn = multilevel_cluster(g["nodes"], g["edges"], g["sizes"], coarse_k=2)
        print(f"assignment: {dict(sorted(asn.items()))}")
        print(f"cutsize: {cutsize(asn, g['edges'])}")
    elif args.mode == "hyper":
        h = load_hypergraph(gpath)
        asn = hypergraph_greedy_cluster(h["nodes"], h["hyperedges"], h["sizes"], target_k=2)
        print(f"assignment: {dict(sorted(asn.items()))}")
        print(f"hyperedge_cut: {hyperedge_cut(asn, h['hyperedges'])}")
    elif args.mode == "cong":
        if not args.seed or not args.cong:
            raise SystemExit("--seed and --cong required for --mode cong")
        g = load_graph(gpath)
        seed = json.loads(Path(args.seed).read_text(encoding="utf-8"))["assignment"]
        cong_raw = json.loads(Path(args.cong).read_text(encoding="utf-8"))
        cong = {}
        for e in cong_raw["edges"]:
            a, b = e["u"], e["v"]
            if a > b:
                a, b = b, a
            cong[(a, b)] = float(e["congestion"])
        initial = {n: str(seed[n]) for n in g["nodes"]}
        asn, plain, pen, comb = congestion_aware_partition(
            g["nodes"], g["edges"], initial, cong, args.lam
        )
        print(f"lambda: {args.lam}")
        print(f"assignment: {dict(sorted(asn.items()))}")
        print(f"plain_cut: {plain}")
        print(f"congestion_penalty: {pen}")
        print(f"combined: {comb}")
    elif args.mode == "timing":
        if not args.seed or not args.crit:
            raise SystemExit("--seed and --crit required for --mode timing")
        g = load_graph(gpath)
        seed = json.loads(Path(args.seed).read_text(encoding="utf-8"))["assignment"]
        crit_raw = json.loads(Path(args.crit).read_text(encoding="utf-8"))
        crit = {}
        for e in crit_raw["edges"]:
            a, b = e["u"], e["v"]
            if a > b:
                a, b = b, a
            crit[(a, b)] = float(e["criticality"])
        initial = {n: str(seed[n]) for n in g["nodes"]}
        asn, plain, wcut = timing_aware_partition(g["nodes"], g["edges"], initial, crit)
        print(f"assignment: {dict(sorted(asn.items()))}")
        print(f"plain_cut: {plain}")
        print(f"weighted_cut: {wcut}")
    else:
        run_greedy_report(gpath, target_k=args.k, capacity=args.capacity)
