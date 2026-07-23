#!/usr/bin/env python3
"""Rewrite learn_partitioning lab transcripts with algorithm-specific speech (clustering depth)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SPECS = {
    "module01-01-cutsize-balance": {
        "title": "Cutsize and balance",
        "lab": "cutsize-balance",
        "open": (
            "Cutsize adds the weights of edges that cross the cut. Balance asks whether the two parts "
            "are roughly the same size. On the starter graph, the bad seed AE versus BCD cuts both "
            "heavy edges and scores cutsize twelve with sizes two and three. The golden ABC versus DE "
            "drops the cut to three with sizes three and two. You will compute both numbers every time "
            "you look at a bipartition."
        ),
        "idea": (
            "For every edge, if the endpoints sit in different parts, add its weight to the cut. "
            "Balance ratio is the smaller part size over the larger. Never celebrate a zero cut that "
            "parks every node on one side—that is not a usable partition."
        ),
    },
    "module01-03-initial-bipartition": {
        "title": "Initial bipartition",
        "lab": "initial-bipartition",
        "open": (
            "Refinement needs a legal starting cut. In this module you build an initial bipartition—"
            "random with a fixed seed, greedy by heaviest edges, or grow from a seed node—before KL or FM "
            "ever runs. On the tiny graph, seed seven’s random bipartition matches the familiar bad seed "
            "shape AE versus BCD with cutsize twelve."
        ),
        "idea": (
            "Random shuffles then splits by half. Greedy prefers keeping heavy edges internal when it can. "
            "Grow expands a frontier from a seed until the part hits its size budget. All three must report "
            "cutsize and balance so you can compare seeds fairly."
        ),
    },
    "module02-01-kl-partition": {
        "title": "Kernighan–Lin bipartition",
        "lab": "kl-partition",
        "open": (
            "Kernighan–Lin improves an existing bipartition by swapping pairs across the cut. You’ll watch "
            "a full pass—gains, locking, a swap sequence, and rollback to the best prefix. On the starter "
            "seed that cuts both heavy edges, KL drives the cut from twelve down to three."
        ),
        "idea": (
            "Score each unlocked pair by swap gain, lock pairs as you go, then keep only the prefix with "
            "best cumulative gain. Here the winning prefix is one swap: A with D, gain nine. Pass one then "
            "finds nothing and KL stops at a local optimum for swap moves."
        ),
    },
    "module02-03-fm-partition": {
        "title": "Fiduccia–Mattheyses bipartition",
        "lab": "fm-partition",
        "open": (
            "Fiduccia–Mattheyses moves one vertex at a time instead of swapping a pair. From the same "
            "cutsize-twelve seed, FM flips D then A, keeps the best prefix of two moves, and lands on the "
            "same ABC versus DE cut of three that KL found."
        ),
        "idea": (
            "Bucketed single-vertex gains, lock after each move, and enforce a balance tolerance so parts "
            "cannot empty. Two legal flips can equal one KL swap’s total gain on this instance—different "
            "move set, same destination quality."
        ),
    },
    "module02-05-spectral-partition": {
        "title": "Spectral bipartition",
        "lab": "spectral-partition",
        "open": (
            "Spectral bipartition reads connectivity from the graph Laplacian. The Fiedler vector gives a "
            "soft ordering of nodes; a balanced sweep of that order picks the cut. On the starter graph the "
            "winning split is DE versus ABC with cutsize three."
        ),
        "idea": (
            "Build L equals D minus A, take the second eigenvector, sort nodes, and try balanced prefixes. "
            "Reject lopsided splits. The continuous membership becomes a hard bipartition only after the "
            "sweep chooses the best legal cut."
        ),
    },
    "module02-07-recursive-bisection": {
        "title": "Recursive bisection",
        "lab": "recursive-bisection",
        "open": (
            "Recursive bisection builds a multiway partition by repeatedly bipartitioning the largest part "
            "until you reach k parts. Start from a bipartition, then cut again. On the tiny graph aiming for "
            "four parts you will see how early cuts constrain later ones."
        ),
        "idea": (
            "Each step is an ordinary bipartition on an induced subgraph. Quality compounds: a weak first "
            "cut leaves later bisectors fewer good options. Always report total cut across all part boundaries "
            "and the part-size vector."
        ),
    },
    "module03-01-multiway-partition": {
        "title": "Multiway partitioning",
        "lab": "multiway-partition",
        "open": (
            "Direct multiway partitioning assigns nodes to k parts without forcing a binary tree of cuts. "
            "Compare it to recursive bisection on the same graph and the same k. Round-robin or seed-based "
            "k-way starts are legal but often need refinement."
        ),
        "idea": (
            "Multiway objectives count every edge that leaves its part. Balance becomes a k-way size vector. "
            "Teaching point: recursive and direct multiway can disagree on cut even when both look balanced."
        ),
    },
    "module03-03-terminal-propagation": {
        "title": "Terminal propagation",
        "lab": "terminal-propagation",
        "open": (
            "Pads and fixed I/O pin nodes to sides before free cells move. Terminal propagation carries those "
            "constraints into the partition so the cut respects the chip boundary. Pin A to one side and E to "
            "the other and watch which free nodes follow."
        ),
        "idea": (
            "Fixed terminals never flip. Their neighbors inherit a pull toward the terminal’s part. Ignoring "
            "terminals produces pretty cuts that violate the floorplan interface—illegal in real flows."
        ),
    },
    "module03-05-hypergraph-partition": {
        "title": "Hypergraph partitioning",
        "lab": "hypergraph-partition",
        "open": (
            "Netlists are hypergraphs: one net can touch many cells. A hyperedge is cut if it spans more than "
            "one part. On the starter hypergraph the golden ABC versus DE leaves a single cut net—pairwise "
            "clique expansion would tell a different story."
        ),
        "idea": (
            "Optimize hyperedge cut, not only pairwise edge cut. Multi-pin nets dominate affinity in real "
            "designs. Use clique expansion only for drawing or as a heuristic substrate—not as the reported "
            "objective unless the lab says so."
        ),
    },
    "module04-01-multilevel-partition": {
        "title": "Multilevel partitioning",
        "lab": "multilevel-partition",
        "open": (
            "A multilevel V-cycle coarsens the graph, partitions the tiny problem, projects the assignment "
            "back, and refines at each finer level. You will walk coarsen, initial partition, project, and "
            "refine on the same starter instance."
        ),
        "idea": (
            "Coarsening shrinks the search space. The coarse partition is cheap. Projection gives a feasible "
            "fine assignment that FM or KL can polish. A bug in coarsening poisons every finer level—debug "
            "the hierarchy before tuning refine passes."
        ),
    },
}


def render(mid: str, spec: dict) -> str:
    title = spec["title"]
    lab = spec["lab"]
    return f"""# {title}

**Module id:** {mid}
**Lab:** {lab}
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — {title}

{spec["open"]}

## Slide 2 — The idea

{spec["idea"]}

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 3 — Browser lab track

In the browser lab track, open the **{lab}** lab from the tools shelf. Load the starter graph, run the algorithm once, and read cutsize and balance in the metrics panel. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 4 — Implement track

In the implement track, open this module’s examples and the course `common/` solvers. Parse the tiny graph, run the algorithm with a deterministic seed, and print the assignment plus cutsize and balance. Match the browser goldens before you claim the checklist.

## Slide 5 — Pitfalls

Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; flipping locked terminals; and stopping before rollback to the best KL or FM prefix. For multilevel flows, verify coarsening before you blame the refiner.

## Slide 6 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
"""


def main() -> None:
    for mid, spec in SPECS.items():
        path = ROOT / mid / "transcript.md"
        path.write_text(render(mid, spec), encoding="utf-8")
        print("ok", mid)


if __name__ == "__main__":
    main()
