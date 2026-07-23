# Examples — Cutsize and balance

Track A (implement). Use `examples/tiny_graph.json` and `../../common/solvers.py`.

## Algorithm

**cutsize + balance metrics**

## Pseudocode

```text
INPUT: assignment side[v], weighted edges
OUTPUT: cutsize, sizes, imbalance
cut ← Σ w(u,v) where side[u]≠side[v]
size[p] ← Σ node_size on side p
imbalance ← |s0−s1| / (s0+s1)
GOLDEN bad AE|BCD: cut=12, sizes 2|3
GOLDEN ABC|DE: cut=3, sizes 3|2
```

## Starter prompts

1. Implement the pseudocode above (or call the matching `common/` helper).
2. Print the metrics named in the GOLDEN line; match browser / Track A tests.
3. Change one knob and report what moved.

## Expected artifacts

- Outputs listed in the pseudocode OUTPUT line
- Note tying the run to the pseudocode phases

## Stretch

Scale the instance slightly; keep the same metrics API.
