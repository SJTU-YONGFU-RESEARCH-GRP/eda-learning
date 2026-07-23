# Examples — Area and deadspace

Track A (implement). Use `examples/tiny_modules.json` and `../../common/solvers.py`.

## Algorithm

**module area, density, deadspace**

## Pseudocode

```text
INPUT: outline W×H, modules areas
OUTPUT: area_sum, deadspace, density
area_sum ← Σ w[m]·h[m]
deadspace ← W·H − area_sum
density ← area_sum / (W·H)
only report density on legal packs
GOLDEN: area=23; outline=80; dead=57
density=0.2875
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
