# Examples — Hypergraph clustering

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
