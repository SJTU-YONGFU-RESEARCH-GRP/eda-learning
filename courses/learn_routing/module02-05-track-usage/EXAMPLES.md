# Examples — Track usage and capacity

Track A (implement). Use the tiny detailed routing instance first (`examples/tiny_dr.json`).

## Algorithm

**track usage and overflow metrics (total, max, count)**

## Pseudocode

```text
Input: route segments [{x,y,layer}, …], capacity Cap
for each consecutive pair (a,b) in path:
  key ← h_edge(a,b) if horizontal else v_edge(a,b)
  usage[key] += 1
for each track t: ov[t] ← max(0, usage[t] − Cap)
Output: {total, max, count, perTrack} overflow summary
Golden: sequential L-HV on six nets overflows at Cap=1
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
