# Examples — Kernighan–Lin refinement

Track A (implement). Shared solver: `../common/solvers.py::kernighan_lin`.

## Goal

Implement a **full KL pass**: D-values, pair gains, locking, cumulative gain, rollback to the best prefix, then repeat passes until no improvement.

## Inputs

- Graph: `examples/tiny_graph.json`
- Seed bipartition: `examples/seed_partition.json` (intentionally bad)

Seed sides:

| Side 0 | Side 1 |
|--------|--------|
| A, E | B, C, D |

This seed **cuts both heavy edges** A–B and D–E.

## API (target)

```text
kernighan_lin(nodes, edges, initial) -> (assignment, history)
# initial / assignment: node -> '0' | '1'
# history: per-pass best_k, best_cum, cut_before, cut_after, swaps
```

## Pseudocode

```text
D(v) = external(v) - internal(v)
gain(a,b) = D(a) + D(b) - 2*w(a,b)   # w=0 if no edge

for pass in 1..max:
  unlock all
  while free nodes on both sides:
    pick unlocked pair (a in 0, b in 1) with max gain
    swap a,b; lock both; record gain; update D
  find prefix k with max cumulative gain
  if best cumulative <= 0: stop
  else apply first k swaps from pass start; continue
```

## Starter prompts

1. Load graph + seed; compute cutsize **before** (golden: **12**).
2. Run one KL pass with rollback; list the accepted swaps.
3. Confirm cutsize **after** is **3** and sides are {A,B,C} vs {D,E} (labels may flip).
4. Break rollback on purpose once—see why the final locked state can be worse.

## Golden

| Step | Value |
|------|-------|
| Seed cutsize | **12** |
| Pass 0 accepted swaps | **(A, D)** with gain **9** |
| Cut after pass 0 | **3** |
| Pass 1 | no improving prefix (`best_k=0`) → stop |
| Final clusters | {A,B,C} and {D,E} |

## Try-these

From this module folder:

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode kl --seed examples/seed_partition.json
```

From `courses/learn_clustering`:

```bash
export PYTHONPATH=common
python -m unittest common.test_solvers.TestKL -v
```
