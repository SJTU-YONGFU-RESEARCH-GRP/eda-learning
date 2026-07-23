# common — learn_partitioning

Track A reference helpers (Python) aligned with browser goldens in `platform/assets/partitioning-core.js`.

| File | Role |
|------|------|
| `tiny_graph.json` | Shared 5-node weighted starter |
| `graphutil.py` | load / cutsize / balance / parts_string |
| `solvers.py` | KL + FM bipartition + `summarize()` |
| `test_solvers.py` | Golden checks (cut 12 → 3) |

```bash
cd courses/learn_partitioning/common
python3 test_solvers.py
```
