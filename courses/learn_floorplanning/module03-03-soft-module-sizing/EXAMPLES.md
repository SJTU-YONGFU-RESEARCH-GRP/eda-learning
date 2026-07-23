# Examples — Soft module sizing

Track A (implement). Use `examples/tiny_modules.json` and `../../common/solvers.py`.

## Algorithm

**reshape soft A under area+aspect**

## Pseudocode

```text
INPUT: soft A area=6, aspect∈[0.5,2]
OUTPUT: (w,h) with w·h=area; pack rest
choose aspect; set w,h; re-pack / legalize
hard modules keep fixed w×h
GOLDEN hard A 3×2 vs soft A 2×3 pack
both area 6; whitespace shape differs
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
