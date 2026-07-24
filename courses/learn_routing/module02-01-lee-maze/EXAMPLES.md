# Examples — Lee maze routing

Track A (implement). Use the tiny detailed routing instance first (`examples/tiny_dr.json`).

## Algorithm

**Lee maze routing (BFS on grid cells)**

## Pseudocode

```text
Input: start, goal, blocked cells, nx, ny
BFS queue ← (start, [start]);  visited ← {start}
while queue not empty:
  pop (cur, path)
  for each neighbor nb in neighbors4(cur) minus blocked:
    if nb == goal: return path + [nb]
    if nb not visited: enqueue (nb, path + [nb])
Output: shortest cell path or None
Golden: (4,1)→(7,1) detours around blockage 5,2,2,2
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
