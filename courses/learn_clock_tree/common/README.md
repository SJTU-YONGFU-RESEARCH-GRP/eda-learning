# common — learn_clock_tree

## Starter instance

[`tiny_cts.json`](tiny_cts.json) — chip 12×8, clock source at (6,4), sinks A–F on spread placement.
Manhattan wire delay per unit; buffer delay 2.0; target skew 0.

## Modules

- `ctsutil.py` — load, sink_points, manhattan, bbox helpers
- `solvers.py` — H-tree, MMM, zero-skew merge, buffering, sequential CTS
- `test_solvers.py` — smoke goldens

Browser algorithms: `platform/tools/<lab-id>/` (when published).
