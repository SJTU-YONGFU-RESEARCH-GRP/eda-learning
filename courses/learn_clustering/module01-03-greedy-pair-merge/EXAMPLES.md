# Examples — Greedy pair merge

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

## Golden (tiny_graph.json, target K=2)

Reference greedy heaviest-edge merge → clusters **{A,B,C}** and **{D,E}**.

| Metric | Value |
|--------|-------|
| cutsize | **3** (C–D weight 2 + C–E weight 1) |
| balance_ratio | 1.2 (sizes 3 vs 2) |

Merge order intuition: A–B, then D–E, then absorb C into {A,B} via B–C before crossing the weak bridge.

