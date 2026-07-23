# Examples — Label propagation

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
| clusters | {A,B,C} under label B, {D,E} under label E |
| cutsize | **3** |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode lp
```
