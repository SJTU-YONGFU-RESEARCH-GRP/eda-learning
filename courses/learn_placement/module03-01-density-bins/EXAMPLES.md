# Examples — Density bins

Track A (implement). Use `examples/tiny_place.json` and `../../common/solvers.py`.

## Algorithm

**bin counts + overflow vs capacity**

## Pseudocode

```text
INPUT: positions, grid Gx×Gy, capacity C
OUTPUT: overflow, per-bin counts
assign each cell to a bin by (x,y)
overflow ← Σ max(0, count[b]−C)
report HPWL with overflow
GOLDEN 2×2 C=1: starter&golden overflow=2
C=2 on golden → overflow=1
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
