# Examples — SA placement

Track A (implement). Use `examples/tiny_place.json` and `../../common/solvers.py`.

## Algorithm

**random jogs; Metropolis on HPWL**

## Pseudocode

```text
INPUT: positions, seed, moves, T0
OUTPUT: best positions + best HPWL
for i in 1..moves:
  jog one cell on one axis
  accept if ΔHPWL<0 or rand<e^(−Δ/T)
  keep best; cool T
GOLDEN seed=42, 60 moves → best≈49.6
accepted≈44 rejected≈16
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
