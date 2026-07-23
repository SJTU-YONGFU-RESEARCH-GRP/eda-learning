# Examples — Congestion-aware clustering

Uses FM on weights `w' = w + λ·congestion`.
Files: `examples/tiny_graph.json`, seed (cut 12), `examples/congestion.json`.

## Golden

| λ | plain_cut | congestion_penalty | combined |
|---|-----------|--------------------|----------|
| 0 | 3 | 9 | 3 |
| 5 | 5 | 0 | 5 |

High λ avoids cutting the congested C–D / C–E bridges.

## Try-these

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode cong --seed ../module02-05-kernighan-lin/examples/seed_partition.json --cong examples/congestion.json --lambda 0
python ../common/solvers.py examples/tiny_graph.json --mode cong --seed ../module02-05-kernighan-lin/examples/seed_partition.json --cong examples/congestion.json --lambda 5
```
