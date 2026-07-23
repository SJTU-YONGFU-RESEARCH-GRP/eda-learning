# Examples — Fixed macros

Track A (implement). Use `examples/tiny_legal.json` and `../../common/` solvers.

## Algorithm

**Abacus with locked macro obstacles**

## API

```text
# Python (courses/learn_legalization/common/)
load_legal / greedy_snap / overlap_remove / abacus_lite / tetris_lite
check_legality · total_displacement · total_hpwl
```

## Pseudocode

```text
INPUT: positions, widths, fixed F (e.g. D@(8,4))
OUTPUT: legal pack; macros never move
place every f in F at locked (x,y)
run Abacus/Tetris on movables only
F intervals block try-place / left-pack
fail legality if any macro drifted
GOLDEN: D stays (8,4); Abacus disp=4; legal
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
