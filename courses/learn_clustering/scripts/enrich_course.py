#!/usr/bin/env python3
"""Enrich learn_clustering: demos, EXAMPLES, transcript Track A try-these."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LABS = [
    ("module01-01-affinity-metrics", "affinity", "01-01"),
    ("module01-03-greedy-pair-merge", "greedy", "01-03"),
    ("module01-05-size-constrained-agglomerative", "capacity", "01-05"),
    ("module02-01-label-propagation", "skeleton", "02-01"),
    ("module02-03-spectral-bisection", "skeleton", "02-03"),
    ("module02-05-kernighan-lin", "skeleton", "02-05"),
    ("module02-07-fiduccia-mattheyses", "skeleton", "02-07"),
    ("module03-01-multilevel-clustering", "skeleton", "03-01"),
    ("module03-03-hypergraph-clustering", "skeleton", "03-03"),
    ("module04-01-congestion-aware-clustering", "skeleton", "04-01"),
    ("module04-03-timing-aware-clustering", "skeleton", "04-03"),
]

GOLDEN_AFFINITY = """## Golden (tiny_graph.json)

Affinity ranking by edge weight (desc):

| Pair | Weight |
|------|--------|
| A–B | 5 |
| D–E | 5 |
| B–C | 4 |
| C–D | 2 |
| A–C | 1 |
| C–E | 1 |

Top merge candidate under pure edge-weight affinity: **A–B** (tie with D–E; break ties by sorted pair id → A–B first in reference solver).
"""

GOLDEN_GREEDY = """## Golden (tiny_graph.json, target K=2)

Reference greedy heaviest-edge merge → clusters **{A,B,C}** and **{D,E}**.

| Metric | Value |
|--------|-------|
| cutsize | **3** (C–D weight 2 + C–E weight 1) |
| balance_ratio | 1.2 (sizes 3 vs 2) |

Merge order intuition: A–B, then D–E, then absorb C into {A,B} via B–C before crossing the weak bridge.
"""

GOLDEN_CAP = """## Golden (tiny_graph.json, K=2, capacity=3)

With per-node size 1 and capacity 3, the unconstrained K=2 solution still fits ({A,B,C} size 3, {D,E} size 2).

Try **capacity=2**: merges that would create size 3 become illegal—expect more than 2 clusters or a different cut. Record both runs in your notes.
"""

SPECS = {
    "module01-01-affinity-metrics": f"""# Examples — Affinity metrics

Track A (implement). Shared helpers: `../common/graphutil.py`.

## API (target)

```text
affinity_edge_weight(edges) -> list[(u, v, score)]  # sorted desc by score
```

## Pseudocode

```text
for each undirected edge (u, v, w):
    score(u, v) = w          # v1 definition
rank pairs by score descending
```

## Starter prompts

1. Load `examples/tiny_graph.json` with `graphutil.load_graph`.
2. Implement `affinity_edge_weight` (or call the common helper).
3. Print the ranked pairs; match the golden table below.
4. Add a second affinity mode (e.g. shared-neighbor count) and compare top-1.

{GOLDEN_AFFINITY}

## Try-these (shell)

From `courses/learn_clustering`:

```bash
export PYTHONPATH=common
python common/solvers.py module01-01-affinity-metrics/examples/tiny_graph.json --k 5
```

(Use `--k 5` to skip merging and mainly inspect affinity ranking printed first.)
""",
    "module01-03-greedy-pair-merge": f"""# Examples — Greedy pair merge

Track A (implement). Shared: `../common/solvers.py::greedy_pair_merge`.

## API (target)

```text
greedy_pair_merge(nodes, edges, sizes, target_k, capacity=None) -> assignment
cutsize(assignment, edges) -> float
```

## Pseudocode

```text
clusters = each node alone
while |clusters| > K:
    pick heaviest legal affinity edge (u, v)
    contract u,v into supernode; update edges
return assignment of original nodes → cluster id
```

## Starter prompts

1. Run reference solver; match golden cutsize **3**.
2. Re-implement contraction without peeking; compare assignment.
3. Change K to 3; report new cutsize.

{GOLDEN_GREEDY}
""",
    "module01-05-size-constrained-agglomerative": f"""# Examples — Size-constrained agglomerative

## API

Same as greedy, with `capacity` set.

## Pseudocode

```text
when picking (u, v):
    skip if sizes[u] + sizes[v] > capacity
if no legal pair: stop early
```

## Starter prompts

1. Run K=2, capacity=3 (should match unconstrained golden).
2. Run K=2, capacity=2; list final clusters and cutsize.
3. Assert your code never emits a cluster larger than capacity.

{GOLDEN_CAP}
""",
}


def demo_script(mid: str, mode: str, key: str) -> str:
    local = f"{mid}/examples/tiny_graph.json"
    header = f"""#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/common"
"""
    if mode == "affinity":
        return (
            header
            + f"""echo "== affinity ranking =="
python - <<'PY'
from pathlib import Path
from graphutil import load_graph, affinity_edge_weight
g = load_graph(Path("{local}"))
for u, v, w in affinity_edge_weight(g["edges"]):
    print(f"{{u}}-{{v}}: {{w}}")
PY
"""
        )
    if mode == "greedy":
        return header + f'python common/solvers.py "{local}" --k 2\n'
    if mode == "capacity":
        return (
            header
            + f"""echo "== capacity 3 =="
python common/solvers.py "{local}" --k 2 --capacity 3
echo "== capacity 2 =="
python common/solvers.py "{local}" --k 2 --capacity 2
"""
        )
    return (
        header
        + f"""echo "Skeleton: load tiny graph and report singleton cutsize."
python - <<'PY'
from pathlib import Path
from graphutil import load_graph, cutsize
g = load_graph(Path("{local}"))
asn = {{n: n for n in g["nodes"]}}
print("nodes:", g["nodes"])
print("edges:", len(g["edges"]))
print("singleton cutsize (all edges cut):", cutsize(asn, g["edges"]))
print("Implement this module's algorithm; replace this skeleton demo.")
PY
"""
    )

TRACK_A_BLOCKS = {
    "module01-01-affinity-metrics": """## Slide 4 — Implement track

In the implement track, open this module’s examples folder and load the tiny weighted graph. Print the working directory so you know where you are, then list the example files. Run the shared affinity helper so you see the ranked pairs—A B should sit at the top with weight five, tied with D E. That ranking is the input every later merge policy will consume.

```bash
# pwd — print working directory (where am I?)
pwd

# ls -la examples — list the starter graph files
ls -la examples

# run affinity ranking via common solvers (from this module folder)
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --k 5
```
""",
    "module01-03-greedy-pair-merge": """## Slide 4 — Implement track

In the implement track, run the reference greedy merge down to two clusters. You should land on A B C versus D E with cutsize three. Then re-implement contraction yourself and check that your cutsize matches. Keep a deterministic tie-break so golden tests stay stable.

```bash
# pwd — print working directory
pwd

# ls examples — confirm tiny_graph.json is present
ls examples

# greedy merge to K=2 via reference solver
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --k 2
```
""",
    "module01-05-size-constrained-agglomerative": """## Slide 4 — Implement track

In the implement track, run the same greedy engine twice: once with capacity three, once with capacity two. Capacity three should still match the unconstrained two-cluster golden. Capacity two should refuse some heavy merges—read the cluster list and cutsize, and confirm no cluster exceeds the cap.

```bash
# capacity 3 — still allows {A,B,C}
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --k 2 --capacity 3

# capacity 2 — rejects size-3 merges
python ../common/solvers.py examples/tiny_graph.json --k 2 --capacity 2
```
""",
}


def patch_transcript(path: Path, mid: str) -> None:
    text = path.read_text(encoding="utf-8")
    # Soften pitfall openings
    text = text.replace("## Slide 5 — Pitfalls\n\nDo not ", "## Slide 5 — Pitfalls to watch\n\nWatch for this: ")
    text = text.replace("## Slide 5 — Pitfalls\n\nCommon traps:", "## Slide 5 — Pitfalls to watch\n\nCommon traps:")
    text = text.replace("## Slide 5 — Pitfalls\n\n", "## Slide 5 — Pitfalls to watch\n\n")

    block = TRACK_A_BLOCKS.get(mid)
    if block and "## Slide 4 — Implement track" in text:
        # replace slide 4 through just before slide 5
        import re
        text = re.sub(
            r"## Slide 4 — Implement track\n\n.*?(?=\n## Slide 5)",
            block.rstrip() + "\n\n",
            text,
            count=1,
            flags=re.S,
        )
    elif mid.startswith("module02") or mid.startswith("module03") or mid.startswith("module04"):
        # inject try-these into skeleton implement slides if no code fence yet
        if "```bash" not in text and "## Slide 4 — Implement track" in text:
            inject = """

```bash
# pwd — print working directory
pwd

# ls examples — confirm the starter graph is here
ls examples

# skeleton demo: load graph + singleton cutsize (replace with your algorithm)
bash assets/_demo.sh
```
"""
            text = text.replace(
                "## Slide 5 — Pitfalls to watch",
                inject + "\n## Slide 5 — Pitfalls to watch",
            )
            if "## Slide 5 — Pitfalls to watch" not in text:
                text = text.replace(
                    "## Slide 5 — Pitfalls",
                    inject + "\n## Slide 5 — Pitfalls",
                )

    path.write_text(text, encoding="utf-8")


def examples_for(mid: str, title_from_readme: str) -> str:
    if mid in SPECS:
        return SPECS[mid]
    return f"""# Examples — {title_from_readme}

Track A (implement). Shared I/O: `../common/graphutil.py`.

## Implementation status

Skeleton harness only — load the tiny graph, compute singleton cutsize, then replace with this module’s full algorithm.

## API sketch

```text
run(graph) -> assignment, metrics{{cutsize, balance, objective}}
```

## Starter prompts

1. Run `bash assets/_demo.sh` from this module folder (via course-root demo).
2. Restate the algorithm in five bullets.
3. Implement end-to-end; keep the same `tiny_graph.json` I/O.
4. Add one regression test with a fixed seed / tie-break.

## Shared golden graph

Same five-node graph as foundations. Unconstrained greedy K=2 cutsize reference: **3** with clusters {{A,B,C}} vs {{D,E}}. Use that as a sanity baseline before claiming your new objective is better.
"""


def main() -> None:
    for mid, mode, key in LABS:
        mod = ROOT / mid
        assets = mod / "assets"
        assets.mkdir(exist_ok=True)
        demo = assets / "_demo.sh"
        demo.write_text(demo_script(mid, mode, key), encoding="utf-8", newline="\n")

        # EXAMPLES
        readme = (mod / "README.md").read_text(encoding="utf-8")
        title = readme.splitlines()[0].lstrip("# ").strip()
        (mod / "EXAMPLES.md").write_text(examples_for(mid, title), encoding="utf-8")

        # transcript polish
        patch_transcript(mod / "transcript.md", mid)

    # offline examples enrich
    (ROOT / "module05-01-offline-benchmark-compare" / "EXAMPLES.md").write_text(
        """# Examples — Offline benchmark compare

## Offline harness

1. Export the same `tiny_graph.json` used in foundations.
2. Run reference greedy K=2; record cutsize **3**, balance **1.2**.
3. If an external tool is available, run it on an equivalent instance and fill the table.
4. If missing, document the install gap; still keep your harness I/O stable.

## Comparison table

| Engine | cutsize | balance | runtime | notes |
|--------|---------|---------|---------|-------|
| learn_clustering greedy K=2 | 3 | 1.2 | | reference |
| external (optional) | | | | |
""",
        encoding="utf-8",
    )

    print(f"Course content enriched under {ROOT}")


if __name__ == "__main__":
    main()
