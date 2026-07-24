# Examples — Spread legalize lite

Track A (implement). Use `examples/tiny_place.json` and `../../common/solvers.py`.

## Algorithm

**push pairs to min distance**

## Pseudocode

```text
INPUT: positions, min_dist
OUTPUT: spread positions
while exists pair with dist < min_dist:
  push the pair apart along their vector
stop when all pairs clear min_dist
NOTE: not row/site legalization
GOLDEN min_dist=0.5 on overlap seed
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
