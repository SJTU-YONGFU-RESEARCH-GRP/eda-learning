# Examples — Offline benchmark compare

## Harness

Compare engines on the same tiny graph:

| Engine | cutsize | notes |
|--------|---------|-------|
| greedy K=2 | 3 | `common/solvers.py` |
| spectral | 3 | |
| multilevel | 3 | |
| KL from bad seed | 12→3 | |
| FM from bad seed | 12→3 | |
| external tool (optional) | | document if missing |

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py ../module01-01-affinity-metrics/examples/tiny_graph.json --k 2
python ../common/solvers.py ../module01-01-affinity-metrics/examples/tiny_graph.json --mode spectral
python ../common/solvers.py ../module01-01-affinity-metrics/examples/tiny_graph.json --mode multilevel
```

Fill the table; if no external tool, still keep the harness rows.
