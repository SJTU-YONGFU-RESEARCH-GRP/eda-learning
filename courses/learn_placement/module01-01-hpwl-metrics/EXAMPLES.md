# Examples — HPWL metrics

Track A (implement). Use `examples/tiny_place.json` and `../../common/solvers.py`.

## Algorithm

**half-perimeter wirelength sum**

## Pseudocode

```text
INPUT: positions, nets
OUTPUT: total HPWL
for each net: bbox → (maxx−minx)+(maxy−miny)
total ← Σ net HPWL
GOLDEN starter=52; compact=14
NOTE: collapsed point ≠ usable place
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
