# Examples — Timing-aware clustering

FM on edges weighted by `w * criticality`.
Files: graph, seed, `examples/criticality.json`.

## Golden

| Metric | Value |
|--------|-------|
| plain_cut | **3** |
| weighted_cut | **7** |
| clusters | {A,B,C} vs {D,E} |

Critical edges A–B / B–C stay internal.

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode timing --seed ../module02-05-kernighan-lin/examples/seed_partition.json --crit examples/criticality.json
```
