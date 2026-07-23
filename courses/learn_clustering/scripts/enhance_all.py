#!/usr/bin/env python3
"""Enhance remaining learn_clustering modules to reference depth."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "module02-05-kernighan-lin" / "examples" / "seed_partition.json"
GRAPH = "examples/tiny_graph.json"


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def demo(mid: str, cmd: str) -> str:
    return f"""#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
{cmd}
"""


MODULES = {}

# --- capacity already ref; deepen EXAMPLES slightly via rewrite ---
MODULES["module01-05-size-constrained-agglomerative"] = {
    "examples": f"""# Examples — Size-constrained agglomerative

Track A. Solver: `../common/solvers.py` greedy with `--capacity`.

## API

```text
greedy_pair_merge(..., target_k, capacity) -> assignment
# skip merge if sizes[u]+sizes[v] > capacity
```

## Golden

| Run | Result |
|-----|--------|
| K=2, capacity=3 | same as unconstrained: {{A,B,C}}/{{D,E}}, cutsize **3** |
| K=2, capacity=2 | cannot form size-3 cluster; stops with more than 2 clusters or different cut |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py {GRAPH} --k 2 --capacity 3
python ../common/solvers.py {GRAPH} --k 2 --capacity 2
```
""",
    "status": "ref",
}

MODULES["module02-01-label-propagation"] = {
    "examples": f"""# Examples — Label propagation

Solver: `../common/advanced.py::label_propagation` (async, deterministic ties).

## API

```text
label_propagation(nodes, edges, max_iters=50, order=None) -> (labels, iters)
```

## Pseudocode

```text
label[v] = v
repeat:
  for v in fixed order:
    label[v] = argmax_weight neighbor labels (tie -> min label id)
until no changes
```

## Golden (default order A..E)

| Metric | Value |
|--------|-------|
| iters_to_stable | **2** |
| clusters | {{A,B,C}} under label B, {{D,E}} under label E |
| cutsize | **3** |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py {GRAPH} --mode lp
```
""",
    "transcript": """# Label propagation clustering

**Module id:** module02-01-label-propagation
**Lab:** label-propagation
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Label propagation clustering

Label propagation grows communities by letting each node adopt the strongest neighbor label. You’ll implement the asynchronous update with a deterministic tie-break, then measure iterations-to-stable and cutsize on the tiny graph.

## Slide 2 — The algorithm

Start with a unique label per node. In a fixed order, each node tallies weighted neighbor labels and switches to the winner—ties go to the lexicographically smallest label. Repeat rounds until nothing changes. On the starter graph with order A through E, the run stabilizes in two iterations with cutsize three.

## Slide 3 — Browser lab track

In the browser lab, step rounds and watch labels flood dense pockets. Reset and change update order to see that communities can flip labels while cutsize stays similar. Orient on the round counter, then code the async loop yourself.

## Slide 4 — Implement track

Load the tiny graph and run the reference label-propagation mode. Confirm two iterations, labels grouping A B C versus D E, and cutsize three. Re-implement the vote and tie-break until the unit test passes.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode lp
```

## Slide 5 — Pitfalls to watch

Order dependence is real—document your sweep order. Without a tie-break, goldens flake. And stopping only on max iterations without checking “changed==0” hides non-convergence.

## Slide 6 — Your turn

Match the golden table, finish the checklist and quiz, then continue to spectral bisection.
""",
    "quiz": {
        "module": "module02-01-label-propagation",
        "title": "Label propagation check",
        "passing_score": 0.67,
        "items": [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Async label propagation updates a node’s label immediately within a sweep.",
                "answer": True,
                "explain": "That is the asynchronous variant used in this course.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "On the starter graph (order A..E), cutsize after LP is…",
                "choices": ["0", "3", "12", "18"],
                "answer": 1,
                "explain": "Natural clusters give cutsize 3.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "Tie-breaking can change which label name a community keeps even if the partition is similar.",
                "answer": True,
                "explain": "Label ids are arbitrary; the partition matter more than the name.",
            },
        ],
    },
    "demo": demo(
        "module02-01-label-propagation",
        'python common/solvers.py module02-01-label-propagation/examples/tiny_graph.json --mode lp',
    ),
    "checklist": """# Checklist — Label propagation

## Track A
- [ ] Implemented async LP with deterministic tie-break
- [ ] Matched golden: iters **2**, cutsize **3**
- [ ] Unit test for LP passes

## Track B
- [ ] Opened lab or noted Coming soon

## Done when
- [ ] I can explain order dependence and why ties need a rule
""",
    "status": "ref",
}

MODULES["module02-03-spectral-bisection"] = {
    "examples": f"""# Examples — Spectral bisection

Solver: `../common/advanced.py::spectral_bisection`.

## API

```text
spectral_bisection(nodes, edges, sizes) -> (assignment, fiedler_order)
```

## Pseudocode

```text
build Laplacian L = D - A
approximate Fiedler vector (2nd-smallest eigenvector)
sort nodes by Fiedler value
sweep balanced splits; pick minimum cutsize
```

## Golden

| Metric | Value |
|--------|-------|
| cutsize | **3** |
| partition | {{A,B,C}} vs {{D,E}} (side labels may flip) |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py {GRAPH} --mode spectral
```
""",
    "transcript": """# Spectral bisection

**Module id:** module02-03-spectral-bisection
**Lab:** spectral-bisection
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Spectral bisection

Spectral bisection uses the graph Laplacian and its Fiedler vector to propose a balanced cut. You’ll build L, approximate the Fiedler coordinates, sweep splits, and pick the minimum balanced cut—landing on cutsize three for the starter graph.

## Slide 2 — The algorithm

Form L equals D minus A. The Fiedler vector is the eigenvector for the second-smallest eigenvalue. Sort nodes by that coordinate and try splits that keep size fractions reasonable. Choose the split with the best cutsize. On the starter graph that recovers {{A,B,C}} versus {{D,E}}.

## Slide 3 — Browser lab track

In the browser lab, visualize the Fiedler order and the chosen split. Toggle balance windows and watch the cut move. Orient on the spectrum plot, then reproduce the pipeline in code.

## Slide 4 — Implement track

Run the spectral mode on the tiny graph. Confirm cutsize three and the natural clusters. Re-implement the sweep yourself; a dense tiny eigensolve is acceptable at course scale.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode spectral
```

## Slide 5 — Pitfalls to watch

Ignoring balance can isolate one node. Numerical noise can scramble near-ties—use a stable sort. And disconnected graphs need explicit component handling.

## Slide 6 — Your turn

Match cutsize three, finish the checklist and quiz, then continue to Kernighan–Lin refinement.
""",
    "quiz": {
        "module": "module02-03-spectral-bisection",
        "title": "Spectral bisection check",
        "passing_score": 0.67,
        "items": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "The Fiedler vector corresponds to…",
                "choices": [
                    "The largest eigenvalue of A",
                    "The second-smallest eigenvalue of L",
                    "Random projection only",
                    "Prim’s MST",
                ],
                "answer": 1,
                "explain": "Fiedler = eigenvector for λ₂ of the Laplacian.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "On the starter graph, spectral bisection achieves cutsize 3.",
                "answer": True,
                "explain": "Matches the natural clusters.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "You should sweep candidate splits under a balance constraint, not only take the median blindly.",
                "answer": True,
                "explain": "The course solver searches balanced cuts along the order.",
            },
        ],
    },
    "demo": demo(
        "module02-03-spectral-bisection",
        "python common/solvers.py module02-03-spectral-bisection/examples/tiny_graph.json --mode spectral",
    ),
    "checklist": """# Checklist — Spectral bisection

## Track A
- [ ] Built / used Laplacian + Fiedler ordering
- [ ] Matched cutsize **3** on tiny_graph
- [ ] Unit test passes

## Track B
- [ ] Opened lab or noted Coming soon

## Done when
- [ ] I can explain why λ₂ / Fiedler relates to a balanced cut
""",
    "status": "ref",
}

MODULES["module02-07-fiduccia-mattheyses"] = {
    "examples": f"""# Examples — Fiduccia–Mattheyses

Solver: `../common/advanced.py::fiduccia_mattheyses`.
Seed: `../module02-05-kernighan-lin/examples/seed_partition.json` (cut 12).

## API

```text
fiduccia_mattheyses(nodes, edges, initial) -> (assignment, history)
# single-vertex moves + lock + rollback + balance
```

## Golden

| Step | Value |
|------|-------|
| Seed cut | **12** |
| Pass 0 moves | D (gain 3), then A (gain 6); best_cum **9** |
| Cut after | **3** |
| Final | {{A,B,C}} vs {{D,E}} |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py {GRAPH} --mode fm --seed ../module02-05-kernighan-lin/examples/seed_partition.json
```
""",
    "transcript": """# Fiduccia–Mattheyses refinement

**Module id:** module02-07-fiduccia-mattheyses
**Lab:** fiduccia-mattheyses
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Fiduccia–Mattheyses refinement

FM refines a bipartition with single-vertex moves, locking, and rollback—cousin to KL, but one cell at a time. On the same bad seed that starts at cutsize twelve, FM reaches cutsize three.

## Slide 2 — The algorithm

Compute move gains from D-values. Repeatedly pick a legal unlocked move that respects balance, move and lock it, accumulate gain, then roll back to the best prefix. Repeat passes until no positive cumulative gain remains. Buckets matter for speed later; on tiny graphs a linear scan is fine.

## Slide 3 — Browser lab track

In the browser lab, step moves and watch the cumulative gain curve. Compare with KL on the same seed. Orient on buckets when they ship, then implement moves and rollback.

## Slide 4 — Implement track

Run FM on the shared bad seed. Confirm moves D then A in the accepted prefix, cut twelve to three. Re-implement selection and rollback until tests pass.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode fm --seed ../module02-05-kernighan-lin/examples/seed_partition.json
```

## Slide 5 — Pitfalls to watch

Skipping rollback keeps a worse locked state. Ignoring balance lets one side empty. Stale gains after a move pick the wrong cell next.

## Slide 6 — Your turn

Reproduce twelve to three, finish the checklist and quiz, then continue to multilevel clustering.
""",
    "quiz": {
        "module": "module02-07-fiduccia-mattheyses",
        "title": "FM check",
        "passing_score": 0.67,
        "items": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "FM differs from KL mainly by…",
                "choices": [
                    "Never using gains",
                    "Moving one vertex at a time instead of swapping a pair",
                    "Only working on hypergraphs",
                    "Forbidding rollback",
                ],
                "answer": 1,
                "explain": "FM uses single-vertex moves.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "On the course seed, FM reduces cutsize from 12 to 3.",
                "answer": True,
                "explain": "Matches the reference run.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "Rollback to the best cumulative-gain prefix is part of a full FM pass.",
                "answer": True,
                "explain": "Same prefix idea as KL.",
            },
        ],
    },
    "demo": demo(
        "module02-07-fiduccia-mattheyses",
        "python common/solvers.py module02-07-fiduccia-mattheyses/examples/tiny_graph.json --mode fm --seed module02-05-kernighan-lin/examples/seed_partition.json",
    ),
    "checklist": """# Checklist — Fiduccia–Mattheyses

## Track A
- [ ] Implemented single-vertex moves + lock + rollback
- [ ] Matched 12→3 golden on the shared seed
- [ ] Unit test passes

## Track B
- [ ] Opened lab or noted Coming soon

## Done when
- [ ] I can contrast FM vs KL in one sentence
""",
    "status": "ref",
}

MODULES["module03-01-multilevel-clustering"] = {
    "examples": f"""# Examples — Multilevel clustering

Solver: `../common/advanced.py::multilevel_cluster` (greedy coarsen → FM refine).

## Golden

| Metric | Value |
|--------|-------|
| cutsize | **3** |
| clusters | {{A,B,C}} vs {{D,E}} |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py {GRAPH} --mode multilevel
```
""",
    "transcript": """# Multilevel clustering

**Module id:** module03-01-multilevel-clustering
**Lab:** multilevel-clustering
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Multilevel clustering

Multilevel methods coarsen, solve cheaply, then refine. On the tiny graph you’ll wire greedy coarsening into an FM refine step and land on cutsize three—the same natural clusters, now as a V-cycle habit.

## Slide 2 — The algorithm

Coarsen with greedy pair merge to two supernodes. Project that bipartition to the fine graph. Refine with FM. Log cutsize at the fine level. Later you can add more levels; the interface stays the same.

## Slide 3 — Browser lab track

In the browser lab, scrub coarse-to-fine levels when shipped. Orient on the V-cycle slider, then assemble the pipeline in code.

## Slide 4 — Implement track

Run multilevel mode and confirm cutsize three. Then call coarsen and FM yourself as separate steps so you see the handoff.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode multilevel
```

## Slide 5 — Pitfalls to watch

A bad coarsening map corrupts projection. Refining only at the finest level wastes hierarchy. Comparing cuts across levels without projecting to the same nodes confuses metrics.

## Slide 6 — Your turn

Match the golden, finish checklist and quiz, then continue to hypergraph clustering.
""",
    "quiz": {
        "module": "module03-01-multilevel-clustering",
        "title": "Multilevel check",
        "passing_score": 0.67,
        "items": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "A multilevel V-cycle typically…",
                "choices": [
                    "Only refines, never coarsens",
                    "Coarsens, solves, projects, and refines",
                    "Deletes timing arcs",
                    "Requires a foundry PDK",
                ],
                "answer": 1,
                "explain": "Coarsen → initial → uncoarsen/refine.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "On the starter graph, multilevel clustering achieves cutsize 3.",
                "answer": True,
                "explain": "Reference run.",
            },
        ],
    },
    "demo": demo(
        "module03-01-multilevel-clustering",
        "python common/solvers.py module03-01-multilevel-clustering/examples/tiny_graph.json --mode multilevel",
    ),
    "checklist": """# Checklist — Multilevel

## Track A
- [ ] Ran coarsen + refine pipeline
- [ ] Matched cutsize **3**
- [ ] Unit test passes

## Done when
- [ ] I can draw a V-cycle and name each stage
""",
    "status": "ref",
}

MODULES["module03-03-hypergraph-clustering"] = {
    "examples": """# Examples — Hypergraph clustering

Input: `examples/tiny_hypergraph.json`  
Solver: `hypergraph_greedy_cluster` + `hyperedge_cut`.

## Golden

| Metric | Value |
|--------|-------|
| clusters | {{A,B,C}} vs {{D,E}} |
| hyperedge_cut | **1** (only net n3 = C–D crosses) |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_hypergraph.json --mode hyper
```
""",
    "transcript": """# Hypergraph clustering

**Module id:** module03-03-hypergraph-clustering
**Lab:** hypergraph-clustering
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Hypergraph clustering

Real nets are hyperedges. You’ll cluster a tiny hypergraph with a cut-net objective and see hyperedge cut one—only the bridge net crosses—where a pairwise model can mislead.

## Slide 2 — The algorithm

Represent each net as a pin set with weight. Affinity for merging two nodes sums weights of hyperedges containing both. Contract, update hyperedges, stop at K clusters. Score with hyperedge cut: a net costs its weight if it spans more than one cluster.

## Slide 3 — Browser lab track

In the browser lab, highlight multi-pin nets and watch cut versus internal. Orient on the net list, then implement contraction carefully.

## Slide 4 — Implement track

Run hyper mode on the tiny hypergraph. Confirm clusters A B C versus D E and hyperedge cut one. Compare mentally to clique expansion—document why the metrics differ.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_hypergraph.json --mode hyper
```

## Slide 5 — Pitfalls to watch

Mixing graph cutsize with hyperedge cut in one table. Forgetting to dedupe pins after contraction. Expanding every net to a clique silently changes the problem.

## Slide 6 — Your turn

Match hyperedge cut one, finish checklist and quiz, then continue to congestion-aware clustering.
""",
    "quiz": {
        "module": "module03-03-hypergraph-clustering",
        "title": "Hypergraph check",
        "passing_score": 0.67,
        "items": [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "A hyperedge can connect more than two nodes.",
                "answer": True,
                "explain": "That is the point of hypergraphs for netlists.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "On the course hypergraph, greedy clustering to K=2 yields hyperedge cut…",
                "choices": ["0", "1", "3", "12"],
                "answer": 1,
                "explain": "Only the C–D bridge net is cut.",
            },
        ],
    },
    "demo": demo(
        "module03-03-hypergraph-clustering",
        "python common/solvers.py module03-03-hypergraph-clustering/examples/tiny_hypergraph.json --mode hyper",
    ),
    "checklist": """# Checklist — Hypergraph

## Track A
- [ ] Loaded tiny_hypergraph.json
- [ ] Matched hyperedge_cut **1**
- [ ] Unit test passes

## Done when
- [ ] I can explain cut-net vs pairwise edge cut
""",
    "status": "ref",
}

MODULES["module04-01-congestion-aware-clustering"] = {
    "examples": f"""# Examples — Congestion-aware clustering

Uses FM on weights `w' = w + λ·congestion`.
Files: `{GRAPH}`, seed (cut 12), `examples/congestion.json`.

## Golden

| λ | plain_cut | congestion_penalty | combined |
|---|-----------|--------------------|----------|
| 0 | 3 | 9 | 3 |
| 5 | 5 | 0 | 5 |

High λ avoids cutting the congested C–D / C–E bridges.

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py {GRAPH} --mode cong --seed ../module02-05-kernighan-lin/examples/seed_partition.json --cong examples/congestion.json --lambda 0
python ../common/solvers.py {GRAPH} --mode cong --seed ../module02-05-kernighan-lin/examples/seed_partition.json --cong examples/congestion.json --lambda 5
```
""",
    "transcript": """# Congestion-aware clustering

**Module id:** module04-01-congestion-aware-clustering
**Lab:** congestion-aware-clustering
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Congestion-aware clustering

Cutsize alone ignores routing hotspots. You’ll boost edge weights by lambda times congestion, re-run FM, and compare lambda zero versus five—watching the partition avoid the congested bridge.

## Slide 2 — The algorithm

Define w prime equals w plus lambda times congestion on each edge. Run FM on the boosted graph from a shared seed. Report plain cut, congestion penalty on the cut, and the combined score. Sweep lambda to see the trade-off.

## Slide 3 — Browser lab track

In the browser lab, toggle lambda and watch the heatmap. Orient on the objective breakdown, then reproduce both lambda runs in code.

## Slide 4 — Implement track

Run congestion mode at lambda zero and five. Confirm lambda zero prefers cut three with penalty nine, while lambda five pays a larger plain cut to drive congestion penalty to zero.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode cong --seed ../module02-05-kernighan-lin/examples/seed_partition.json --cong examples/congestion.json --lambda 5
```

## Slide 5 — Pitfalls to watch

An unscaled lambda makes the penalty dominate or vanish. Always log plain cut and penalty separately. Don’t compare combined scores across different lambda without saying so.

## Slide 6 — Your turn

Fill the lambda table, finish checklist and quiz, then continue to timing-aware clustering.
""",
    "quiz": {
        "module": "module04-01-congestion-aware-clustering",
        "title": "Congestion-aware check",
        "passing_score": 0.67,
        "items": [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Increasing lambda can raise plain cutsize while lowering congestion penalty.",
                "answer": True,
                "explain": "That is the trade-off on the course instance.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "At lambda=5 on the course data, congestion_penalty becomes…",
                "choices": ["9", "5", "0", "12"],
                "answer": 2,
                "explain": "The partition avoids congested cut edges.",
            },
        ],
    },
    "demo": demo(
        "module04-01-congestion-aware-clustering",
        "python common/solvers.py module04-01-congestion-aware-clustering/examples/tiny_graph.json --mode cong --seed module02-05-kernighan-lin/examples/seed_partition.json --cong module04-01-congestion-aware-clustering/examples/congestion.json --lambda 5",
    ),
    "checklist": """# Checklist — Congestion-aware

## Track A
- [ ] Ran λ=0 and λ=5
- [ ] Matched golden table
- [ ] Unit test passes

## Done when
- [ ] I can explain the cut vs congestion trade-off
""",
    "status": "ref",
}

MODULES["module04-03-timing-aware-clustering"] = {
    "examples": f"""# Examples — Timing-aware clustering

FM on edges weighted by `w * criticality`.
Files: graph, seed, `examples/criticality.json`.

## Golden

| Metric | Value |
|--------|-------|
| plain_cut | **3** |
| weighted_cut | **7** |
| clusters | {{A,B,C}} vs {{D,E}} |

Critical edges A–B / B–C stay internal.

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py {GRAPH} --mode timing --seed ../module02-05-kernighan-lin/examples/seed_partition.json --crit examples/criticality.json
```
""",
    "transcript": """# Timing-aware clustering

**Module id:** module04-03-timing-aware-clustering
**Lab:** timing-aware-clustering
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Timing-aware clustering

Timing-critical edges should resist being cut. You’ll weight edges by criticality, refine with FM, and report both plain and weighted cut—protecting the A–B–C path on the starter instance.

## Slide 2 — The algorithm

Multiply each edge weight by its criticality. Run FM from the shared seed on that weighted graph. Report plain cutsize on original weights and weighted cut on the criticality-scaled weights. Compare to an unweighted refine when you have time.

## Slide 3 — Browser lab track

In the browser lab, highlight critical edges and toggle weighting. Orient on the slack or criticality legend, then implement weights in the scorer.

## Slide 4 — Implement track

Run timing mode. Confirm plain cut three, weighted cut seven, and clusters that keep the critical chain together.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode timing --seed ../module02-05-kernighan-lin/examples/seed_partition.json --crit examples/criticality.json
```

## Slide 5 — Pitfalls to watch

Criticality must sit on the same objects you cut. Enormous weights can freeze the partition—clamp or normalize. Stale annotations after contraction need a documented rule.

## Slide 6 — Your turn

Match the golden metrics, finish checklist and quiz, then continue to the offline benchmark module.
""",
    "quiz": {
        "module": "module04-03-timing-aware-clustering",
        "title": "Timing-aware check",
        "passing_score": 0.67,
        "items": [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Timing-aware clustering increases the cost of cutting critical edges.",
                "answer": True,
                "explain": "Criticality scales edge weights in the objective.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "On the course instance, weighted_cut is…",
                "choices": ["3", "7", "12", "0"],
                "answer": 1,
                "explain": "Reference timing run.",
            },
        ],
    },
    "demo": demo(
        "module04-03-timing-aware-clustering",
        "python common/solvers.py module04-03-timing-aware-clustering/examples/tiny_graph.json --mode timing --seed module02-05-kernighan-lin/examples/seed_partition.json --crit module04-03-timing-aware-clustering/examples/criticality.json",
    ),
    "checklist": """# Checklist — Timing-aware

## Track A
- [ ] Ran timing mode with criticality file
- [ ] Matched plain_cut 3 / weighted_cut 7
- [ ] Unit test passes

## Done when
- [ ] I can explain plain vs weighted cut
""",
    "status": "ref",
}

MODULES["module05-01-offline-benchmark-compare"] = {
    "examples": """# Examples — Offline benchmark compare

## Harness

Compare engines on the same tiny graph:

| Engine | cutsize | notes |
|--------|---------|-------|
| greedy K=2 | 3 | `common/solvers.py` |
| spectral | 3 | |
| multilevel | 3 | |
| KL from bad seed | 12→3 | |
| FM from bad seed | 12→3 | |
| external tool (optional) | | document if missing |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py ../module01-01-affinity-metrics/examples/tiny_graph.json --k 2
python ../common/solvers.py ../module01-01-affinity-metrics/examples/tiny_graph.json --mode spectral
python ../common/solvers.py ../module01-01-affinity-metrics/examples/tiny_graph.json --mode multilevel
```

Fill the table; if no external tool, still keep the harness rows.
""",
    "transcript": """# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none (offline)
**Tracks:** offline harness

## Slide 1 — Offline benchmark compare

Toy engines teach mechanism; tables teach honesty. You’ll run the same tiny instance through greedy, spectral, multilevel, and refinement from a bad seed—then optionally an external tool.

## Slide 2 — Fair compare rules

Identical input. Fixed seeds when randomized. Same metrics. If an external tool is missing, document the gap—don’t invent goldens.

## Slide 3 — What good looks like

On this instance, several engines agree on cutsize three for the natural clusters. Refinement shows twelve to three from a bad seed. Huge unexplained wins usually mean a metric mismatch.

## Slide 4 — Your turn

Fill the comparison table from EXAMPLES, finish the checklist, then continue to the wrap module.
""",
    "quiz": {
        "module": "module05-01-offline-benchmark-compare",
        "title": "Offline compare check",
        "passing_score": 0.67,
        "items": [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Fair compares require the same input instance and comparable metrics.",
                "answer": True,
                "explain": "Otherwise you compare different problems.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "If an external tool is missing, you should still record your harness results and document the gap.",
                "answer": True,
                "explain": "Honesty beats fake goldens.",
            },
        ],
    },
    "checklist": """# Checklist — Offline compare

- [ ] Filled the engine comparison table on tiny_graph
- [ ] Recorded KL/FM 12→3 from the bad seed
- [ ] Noted external tool present or missing

## Done when
- [ ] I can judge clustering quality across engines without mixing metrics
""",
    "status": "ref",
}


def main() -> None:
    for mid, spec in MODULES.items():
        mod = ROOT / mid
        if "examples" in spec:
            w(mod / "EXAMPLES.md", spec["examples"])
        if "transcript" in spec:
            w(mod / "transcript.md", spec["transcript"])
        if "quiz" in spec:
            w(mod / "quiz.json", json.dumps(spec["quiz"], indent=2))
        if "checklist" in spec:
            w(mod / "CHECKLIST.md", spec["checklist"])
        if "demo" in spec:
            w(mod / "assets" / "_demo.sh", spec["demo"])

    # MODULES.md status: mark all labs ref
    modules_md = ROOT / "docs" / "MODULES.md"
    text = modules_md.read_text(encoding="utf-8")
    for mid in MODULES:
        text = text.replace(f"| `{mid}` | `lab` |", f"| `{mid}` | `lab` |")  # noop structure
        # replace trailing | P | for these ids
        import re

        text = re.sub(
            rf"(\| `{mid}` \| `(?:lab|offline)` \|.*?\| )P( \|)",
            r"\1**ref**\2",
            text,
        )
    modules_md.write_text(text, encoding="utf-8")
    print(f"Enhanced {len(MODULES)} modules")


if __name__ == "__main__":
    main()
