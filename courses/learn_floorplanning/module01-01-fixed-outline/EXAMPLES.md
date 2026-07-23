# Examples — Fixed outline

Track A (implement). Use `examples/tiny_modules.json` and `../../common/solvers.py`.

## Algorithm

**containment + non-overlap legality**

## Pseudocode

```text
INPUT: outline W×H, modules (x,y,w,h)
OUTPUT: legal? / failure reason
for each m: fail if outside [0,W]×[0,H]
for each pair: fail if interior overlap
edge-touch OK; positive-area overlap not
GOLDEN pack legal; E@x=9 overflow illegal
outline 10×8 (area 80); modules A–E
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
