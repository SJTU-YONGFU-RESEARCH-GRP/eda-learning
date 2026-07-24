# common — learn_global_routing

## Starter instance

[`tiny_gr.json`](tiny_gr.json) — chip 12×8, GCells 4×2 (cell 3×4), edge capacity 2.
Cells A–F; six nets on spread placement. Global routes deposit +1 usage per traversed edge.

## Modules

- `grutil.py` — load, GCell index, edge list, terminals
- `solvers.py` — L/Z/maze/star, route_nets, overflow, rip-up
- `test_solvers.py` — smoke goldens

Browser algorithms: `platform/tools/<lab-id>/` (when published).
