# Examples — Site and row model

Track A (implement). Use `examples/tiny_legal.json` and `../../common/` solvers.

## Algorithm

**site/row grid model and cell widths**

## API

```text
# Python (courses/learn_legalization/common/)
load_legal / greedy_snap / overlap_remove / abacus_lite / tetris_lite
check_legality · total_displacement · total_hpwl
```

## Pseudocode

```text
INPUT: chip W×H, siteW, rowH, rows Y[], widths w[c]
OUTPUT: legal coordinate rules
for each cell c:
  x multiple of siteW; y in Y[]
  occupies [x, x+w[c]) × [y, y+rowH)
GOLDEN: W=12 H=6 siteW=1 rowH=2 Y={0,2,4}
widths A–D=2 E–F=1 (total 10 ≤ 12)
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
