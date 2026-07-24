# Examples — Net models

Track A (implement). Use `examples/tiny_place.json` and `../../common/solvers.py`.

## Algorithm

**bbox vs clique vs star HPWL**

## Pseudocode

```text
INPUT: net pins, positions, model
bbox: one HPWL on all pins
clique: Σ pairwise HPWL over pin pairs
star: Σ HPWL(hub, other pins)
GOLDEN 4-pin ABCD on golden place:
  clique=16; star from A=8
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
