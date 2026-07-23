# Examples — Fiduccia–Mattheyses

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
| Final | {A,B,C} vs {D,E} |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode fm --seed ../module02-05-kernighan-lin/examples/seed_partition.json
```
