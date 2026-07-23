# Examples — Spectral bisection

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
| partition | {A,B,C} vs {D,E} (side labels may flip) |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode spectral
```
