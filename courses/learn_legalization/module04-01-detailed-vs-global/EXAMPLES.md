# Examples — Detailed versus global legalize

Track A (implement). Use `examples/tiny_legal.json` and `../../common/` solvers.

## Algorithm

**global=Tetris, detailed=Abacus**

## API

```text
# Python (courses/learn_legalization/common/)
load_legal / greedy_snap / overlap_remove / abacus_lite / tetris_lite
check_legality · total_displacement · total_hpwl
```

## Pseudocode

```text
INPUT: illegal / global positions
global:   TetrisLite → disp=6 HPWL=32
detailed: AbacusLite → disp=4 HPWL=38
both must report legal=true
CHOOSE detailed when disp budget is tight
CHOOSE global when a fast shelf pack is enough
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
