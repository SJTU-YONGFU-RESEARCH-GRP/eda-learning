# common — learn_placement

Track A reference helpers (Python) aligned with browser goldens in `platform/assets/placement-core.js`.

| File | Role |
|------|------|
| `tiny_place.json` | Shared 6-cell starter / golden / overlap (matches placement-core.js) |
| `placementutil.py` | load / HPWL / clique / star / timing / density bins |
| `solvers.py` | force-directed + quadratic + SA lite ports |
| `test_solvers.py` | Golden checks (HPWL 52→14, force≈18.7, quad 48, SA≈49.6, …) |

```bash
cd courses/learn_placement/common
python3 test_solvers.py
```
