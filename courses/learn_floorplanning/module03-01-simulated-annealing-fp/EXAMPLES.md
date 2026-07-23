# Examples — SA floorplan

Track A (implement). Use `examples/tiny_modules.json` and `../../common/solvers.py`.

## Algorithm

**anneal with illegality penalty cost**

## Pseudocode

```text
INPUT: pack / representation, T schedule
OUTPUT: best legal low-cost pack
cost ← 1000·¬legal + deadspace + α·HPWL
propose neighbor (swap/move/perturb)
accept if Δ<0 or rand < e^(−Δ/T)
keep best; cool T
GOLDEN legal cost≈36; bad≈1044
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
