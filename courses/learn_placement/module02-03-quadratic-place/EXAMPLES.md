# Examples — Quadratic place

Track A (implement). Use `examples/tiny_place.json` and `../../common/solvers.py`.

## Algorithm

**Gauss–Seidel neighbor solve w/ pads**

## Pseudocode

```text
INPUT: positions, nets, fixed pads {A,D}
OUTPUT: free-cell coords + HPWL
repeat: for free c:
  blend toward neighbor average (damped)
pads A,D remain pinned
GOLDEN starter 52 → HPWL 48
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
