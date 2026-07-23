# Examples — Multilevel clustering

Solver: `../common/advanced.py::multilevel_cluster` (greedy coarsen → FM refine).

## Golden

| Metric | Value |
|--------|-------|
| cutsize | **3** |
| clusters | {A,B,C} vs {D,E} |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode multilevel
```
