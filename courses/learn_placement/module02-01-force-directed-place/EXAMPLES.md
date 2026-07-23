# Examples — Force-directed place

Track A (implement). Use `examples/tiny_place.json` and `../../common/solvers.py`.

## Algorithm

**neighbor average pull + weak center**

## Pseudocode

```text
INPUT: positions, nets, α, iters, fixed pads
OUTPUT: updated positions + HPWL
each iter, for free cell c:
  tgt ← avg neighbor coords (+ weak center)
  pos[c] ← (1−α)·pos[c] + α·tgt
pads stay fixed
GOLDEN starter 52 → ≈18.7 after defaults
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
