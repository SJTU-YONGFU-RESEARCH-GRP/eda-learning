# Examples — Analytical place

Track A (implement). Use `examples/tiny_place.json` and `../../common/solvers.py`.

## Algorithm

**wirelength stage + density spread**

## Pseudocode

```text
INPUT: positions, bins, pads
OUTPUT: positions, HPWL, overflow
stage1: wirelength pull (force/quad style)
stage2: push out of overloaded bins
stage3: light reconnect for HPWL
report HPWL and overflow together
GOLDEN lite ≈48.1 HPWL after defaults
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
