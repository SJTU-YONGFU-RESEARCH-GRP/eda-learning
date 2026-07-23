# common — learn_congestion

## Starter instance

[`tiny_cong.json`](tiny_cong.json) — chip 12×8, GCells 4×2 (cell 3×4), capacity 2.0.
Cells A–F; nets match placement. `placement` is spread; `congested_seed` clusters in the center.

## Modules

- `congestionutil.py` — load, GCell index, bbox, HPWL
- `solvers.py` — RUDY, probabilistic, congestion map, overflow, inflate, weights, feedback
- `test_solvers.py` — smoke goldens

Browser algorithms: `platform/tools/<lab-id>/` + `platform/assets/congestion-core.js`.
