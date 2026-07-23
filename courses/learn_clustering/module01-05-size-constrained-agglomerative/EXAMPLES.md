# Examples — Size-constrained agglomerative

Track A. Solver: `../common/solvers.py` greedy with `--capacity`.

## API

```text
greedy_pair_merge(..., target_k, capacity) -> assignment
# skip merge if sizes[u]+sizes[v] > capacity
```

## Golden

| Run | Result |
|-----|--------|
| K=2, capacity=3 | same as unconstrained: {A,B,C}/{D,E}, cutsize **3** |
| K=2, capacity=2 | cannot form size-3 cluster; stops with more than 2 clusters or different cut |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --k 2 --capacity 3
python ../common/solvers.py examples/tiny_graph.json --k 2 --capacity 2
```
