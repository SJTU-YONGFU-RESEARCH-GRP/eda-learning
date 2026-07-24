# Examples — Sequential detailed route

Track A (implement). Use the tiny detailed routing instance first (`examples/tiny_dr.json`).

## Algorithm

**sequential detailed routing (ordered net deposit on tracks)**

## Pseudocode

```text
Input: ordered nets[], terminals, mode (astar/l_hv/lee), Cap
usage ← empty;  routes ← empty
for each net N in order:
  route N with chosen mode respecting current usage + blockages
  deposit +1 on each directed track key in the route
Output: routes map + final usage; order affects congestion
Golden: all six nets in default order yields positive track overflow
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
