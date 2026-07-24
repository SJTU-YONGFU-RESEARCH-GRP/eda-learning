# Examples — Timing-driven place

Track A (implement). Use `examples/tiny_place.json` and `../../common/solvers.py`.

## Algorithm

**weighted HPWL with net criticality**

## Pseudocode

```text
INPUT: positions, nets, weights w[net]
OUTPUT: plain HPWL, timing HPWL
plain ← Σ HPWL(net)
timing ← Σ w[net]·HPWL(net)
optimize timing (or report both)
GOLDEN starter: plain=52 timing=116
compact: plain=14 timing=30
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
