# Examples — A* detailed routing

Track A (implement). Use the tiny detailed routing instance first (`examples/tiny_dr.json`).

## Algorithm

**A* detailed routing (congestion-aware grid search)**

## Pseudocode

```text
Input: start, goal, track usage, capacity Cap, blockages
open ← min-heap by f = g + Manhattan(goal)
while open not empty:
  pop (g, cur, path)
  for each 4-neighbor nb on M1 or M2 layer step:
    if cell_blocked(nb): skip
    step_cost ← 1 + 10×overflow_penalty if usage[track] ≥ Cap
    if better g to nb: push (g+step_cost, nb, path+[nb])
Output: congestion-aware shortest path or None
Golden: hot M1 edge ((1,1),(2,1)) at Cap=1 forces detour
```


## Track A API

```bash
# from courses/learn_routing/
python3 -c "from common.solvers import route_from_data; from common.drutil import load; d=load('common/tiny_dr.json'); print(route_from_data(d))"
```

Prefer helpers in `common/drutil.py` and `common/solvers.py` over ad-hoc scripts.

## Starter prompts

1. Load `placement`, `blockages`, and `nets` from `tiny_dr.json`; print the 12×8 grid and track count.
2. Run the algorithm for this lab; print track usage or overflow with two decimals.
3. Compare sequential L-HV vs A* on total track overflow.
4. Change track_capacity from 1 to 2 and report which tracks flip congested.
5. Write one sentence: why this idea belongs after global routing.

## Expected artifacts

- Track usage map or segment listing for the lab algorithm
- Overflow summary (total, max, count) when relevant
- Short note tying the metric to rip-up or sequential order
