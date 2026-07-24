# Examples — Routing grid graph

Track A (implement). Use the tiny detailed routing instance first (`examples/tiny_dr.json`).

## Algorithm

**routing grid graph (M1 horizontal + M2 vertical tracks)**

## Pseudocode

```text
Input: nx, ny grid, layers M1 (horizontal), M2 (vertical)
h_edges ← empty;  v_edges ← empty
for each grid point (x,y):
  if x+1 < nx: add directed M1 edge ((x,y)→(x+1,y))
  if y+1 < ny: add directed M2 edge ((x,y)→(x,y+1))
Output: track graph with canonical directed keys
Golden: 12×8 yields 11×8 M1 edges and 12×7 M2 edges
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
