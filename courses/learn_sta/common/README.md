# common — learn_sta

Shared Track A helpers (Python) for tiny timing netlists and metrics.

| File | Role |
|------|------|
| `tiny_timing.json` | Starter chain (6 pins, 5 arcs) |
| `timing_io.py` | Load / clone timing JSON |
| `graph.py` | Levelize, sources/sinks, arc counts, goldens |
| `test_timing_graph.py` | Golden self-check |

```bash
cd courses/learn_sta/common
python3 test_timing_graph.py
```

Browser algorithms: `platform/assets/sta-core.js` (must stay in sync with `GOLDENS` here).
