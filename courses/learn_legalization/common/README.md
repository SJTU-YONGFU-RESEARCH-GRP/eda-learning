# common — learn_legalization

Shared Track A helpers for tiny legalization instances.

## Starter instance

[`tiny_legal.json`](tiny_legal.json) — W=12 sites, H=6 (3 rows), siteW=1, rowH=2, row bottoms y=0,2,4.
Cells A–D width 2 sites; E,F width 1. Nets match learn_placement. Macro D fixed at (8,4).

Starters:
- `starter_illegal` — A,B,C overlap on middle row (integer coords)
- `starter_float` — global-place floats for greedy snap

Suggested layout as reference solvers mature:

- `legalizationutil.py` — load JSON, legality, displacement, HPWL helpers
- `solvers.py` — greedy_snap, overlap_remove, abacus_lite, tetris_lite
- `test_solvers.py` — smoke tests (goldens pending platform JS alignment)

Browser algorithms will live under `platform/tools/<lab-id>/` when published.
