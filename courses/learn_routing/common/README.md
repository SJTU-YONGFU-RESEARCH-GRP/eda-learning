# common — learn_routing

## Starter instance

[`tiny_dr.json`](tiny_dr.json) — chip 12×8, grid 12×8, track capacity 1, layers M1/M2.
Cells A–F; six nets on spread placement; blockage at (5,2) size 2×2. Detailed routes deposit +1 usage per traversed directed track.

## Modules

- `drutil.py` — load, grid index, pin access, track keys, blockages
- `solvers.py` — Lee/A*, L-layer routes, track overflow, DRC lite, rip-up, sequential
- `test_solvers.py` — smoke goldens

Browser algorithms: `platform/tools/<lab-id>/` (when published).
