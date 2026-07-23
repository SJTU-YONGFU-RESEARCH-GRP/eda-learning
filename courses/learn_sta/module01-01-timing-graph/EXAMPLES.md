# Examples — Timing graph

Track A (implement). Use `examples/tiny_timing.json` and `../../common/propagate.py + graph.py`.

## Algorithm

**build pin/arc graph + Kahn levelize**

## Pseudocode

```text
INPUT: pins, arcs (delay, kind cell|net)
OUTPUT: levels[] or FAIL(cycle)
indeg[v]←|preds|; Q←{v|indeg=0}; level[Q]=0
while Q:
  u←pop; for v in succ(u):
    indeg[v]−=1; level[v]←max(level[v],level[u]+1)
    if indeg[v]=0: push v
FAIL if not all visited else return levels
GOLDEN: 6 pins, 5 arcs; in:0 … out:5
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
