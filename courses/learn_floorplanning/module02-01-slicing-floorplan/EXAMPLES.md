# Examples — Slicing / polish

Track A (implement). Use `examples/tiny_modules.json` and `../../common/solvers.py`.

## Algorithm

**postfix H/V polish evaluation**

## Pseudocode

```text
INPUT: polish tokens (modules + H/V)
OUTPUT: packing (x,y,w,h) per module
stack-eval postfix:
  module → push rect
  H: pop a,b; stack vertically
  V: pop a,b; place side by side
GOLDEN: A D H B V C V E V
bbox 9×3; legal in 10×8
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
