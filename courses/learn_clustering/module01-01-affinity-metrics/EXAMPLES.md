# Examples — Affinity metrics

Track A (implement). Shared helpers: `../common/graphutil.py`.

## Goal

Define at least **two** affinity scores and show they can change merge priority.

## API (target)

```text
affinity_edge_weight(edges) -> list[(u, v, score)]           # sorted desc
affinity_shared_neighbors(nodes, edges) -> list[(u, v, score)]
```

## Definitions (v1)

**Edge-weight affinity**

```text
score(u,v) = w(u,v)
```

**Shared-neighbor + edge affinity**

```text
score(u,v) = w(u,v) + sum_x min(w(u,x), w(v,x))
             over common neighbors x
```

## Starter prompts

1. Load `examples/tiny_graph.json`.
2. Implement (or call) both affinity functions.
3. Print both rankings; match the golden tables.
4. Explain in one sentence why A–C rises under shared-neighbor scoring.

## Golden — edge weight

| Pair | Score |
|------|-------|
| A–B | 5 |
| D–E | 5 |
| B–C | 4 |
| C–D | 2 |
| A–C | 1 |
| C–E | 1 |

## Golden — shared-neighbor + edge

| Pair | Score | Why |
|------|-------|-----|
| A–B | 6 | 5 + min(A–C,B–C)=1 |
| D–E | 6 | 5 + min(D–C,E–C)=1 |
| A–C | 5 | 1 + min(A–B,C–B)=4 |
| B–C | 5 | 4 + min(B–A,C–A)=1 |
| C–D | 3 | 2 + min(C–E,D–E)=1 |
| C–E | 3 | 1 + min(C–D,E–D)=2 |

## Try-these

From this module folder:

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode affinity
python -m unittest common.test_solvers -v
```

(Run the unittest from `courses/learn_clustering` with `PYTHONPATH=common`.)
