# Examples — Pin assignment

Track A (implement). Use `examples/tiny_modules.json` and `../../common/solvers.py`.

## Algorithm

**boundary pins on outline sides**

## Pseudocode

```text
INPUT: outline, pin list {side, offset}
OUTPUT: pinsValid?
each pin on left|right|top|bottom edge
offset in range for that side
require all four sides represented
GOLDEN 4 pins (one/side) → valid true
empty list → valid false
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
