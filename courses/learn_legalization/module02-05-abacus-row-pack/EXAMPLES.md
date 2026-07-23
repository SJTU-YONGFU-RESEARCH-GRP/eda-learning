# Examples — Abacus row packing

Track A (implement). Use `examples/tiny_legal.json` and `../../common/` solvers.

## Algorithm

**Abacus-lite: try each row, min L1 displacement**

## API

```text
# Python (courses/learn_legalization/common/)
load_legal / greedy_snap / overlap_remove / abacus_lite / tetris_lite
check_legality · total_displacement · total_hpwl
```

## Pseudocode

```text
INPUT: origin, widths, rows Y[], fixed macros
OUTPUT: legal pack minimizing Σ L1 move
place fixed macros first
order ← movables by origin.x
for each cell c in order:
  for each row y: trial leftmost legal x
  keep (x,y) with min |Δx|+|Δy| to origin
  place c at best
GOLDEN: A(4,2) B(4,0) C(4,4); disp=4; HPWL=38
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
