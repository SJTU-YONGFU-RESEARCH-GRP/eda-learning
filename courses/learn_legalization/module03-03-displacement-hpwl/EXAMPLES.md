# Examples — Displacement versus HPWL

Track A (implement). Use `examples/tiny_legal.json` and `../../common/` solvers.

## Algorithm

**cost = HPWL + λ · displacement**

## API

```text
# Python (courses/learn_legalization/common/)
load_legal / greedy_snap / overlap_remove / abacus_lite / tetris_lite
check_legality · total_displacement · total_hpwl
```

## Pseudocode

```text
INPUT: legal positions, origin, nets, λ≥0
OUTPUT: cost, HPWL, disp
disp ← Σ|Δx|+|Δy| vs origin
HPWL ← Σ net bbox (cell centers)
cost ← HPWL + λ · disp
GOLDEN Abacus: HPWL=38 disp=4
  λ=1 → 42;  λ=5 → 58
```

## Starter prompts

1. Implement the pseudocode above (or call the matching `common/` solver).
2. Print legality, displacement, and HPWL; match the GOLDEN line.
3. Change one knob (macro lock, λ, or packer) and report the delta.

## Expected artifacts

- Legal (x, y) per cell (or intentional illegal before-state)
- Legality + displacement / HPWL (and cost when relevant)
- Note tying the run to the pseudocode phases

## Stretch

Lock macro D at (8,4) or sweep λ; keep the same metrics API.
