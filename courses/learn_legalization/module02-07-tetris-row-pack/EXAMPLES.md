# Examples — Tetris row packing

Track A (implement). Use `examples/tiny_legal.json` and `../../common/` solvers.

## Algorithm

**nearest-row assign then left pack**

## API

```text
# Python (courses/learn_legalization/common/)
load_legal / greedy_snap / overlap_remove / abacus_lite / tetris_lite
check_legality · total_displacement · total_hpwl
```

## Pseudocode

```text
INPUT: positions, widths, rows Y[], fixed macros
OUTPUT: legal packing (shelf / Tetris-lite)
for each movable c: y ← nearest row (freeze)
then per-row left pack (see overlap removal)
GOLDEN: A@4 B@6 C@8 on y=2; disp=6; HPWL=32
COMPARE: Abacus disp=4 (more search)
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
