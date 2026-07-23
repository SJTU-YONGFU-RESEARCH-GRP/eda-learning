# common — learn_floorplanning

Shared Track A helpers for tiny floorplan instances (same goldens as browser labs).

## Starter instance

[`tiny_modules.json`](tiny_modules.json) — modules **A–E**, outline **10×8**.
Module areas sum to **23**; deadspace **57**; density **0.2875**. Module **A** is soft.

## Python API

| Module | Role |
|--------|------|
| [`goldens.py`](goldens.py) | OUTLINE, MODULES, GOLDEN_PACK, BAD_PACK, polish/B*/SP/macros/pins |
| [`metrics.py`](metrics.py) | legality, deadspace, density |
| [`pack.py`](pack.py) | eval_polish, pack_bstar, pack_sequence_pair, hierarchical |
| [`solvers.py`](solvers.py) | HPWL / cost helpers + golden runners |
| [`test_solvers.py`](test_solvers.py) | Assert teaching goldens |

```bash
cd courses/learn_floorplanning/common
python test_solvers.py
```

Browser algorithms: `platform/assets/floorplanning-core.js` (must stay in sync with these goldens).
