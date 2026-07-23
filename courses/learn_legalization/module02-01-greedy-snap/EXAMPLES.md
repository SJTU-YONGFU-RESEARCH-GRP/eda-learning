# Examples — Greedy snap

Track A (implement). Use `examples/tiny_legal.json` and `../../common/` solvers.

## Algorithm

**greedy site/row snap from float coordinates**

## API

```text
# Python (courses/learn_legalization/common/)
load_legal / greedy_snap / overlap_remove / abacus_lite / tetris_lite
check_legality · total_displacement · total_hpwl
```

## Pseudocode

```text
INPUT: float positions, widths, rows Y[], chip W
OUTPUT: snapped positions (may still overlap)
for each movable cell c:
  x ← round(x) clamped to [0, W−w[c]]
  y ← nearest row in Y[]
fixed macros: keep locked (x,y)
NOTE: snap ≠ legal — A,B may share a site
GOLDEN float: A→(4,2), B→(4,2) still overlap
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
