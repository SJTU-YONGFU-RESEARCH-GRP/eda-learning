# Examples — Probabilistic routing demand

Track A (implement). Use the tiny congestion instance first (`examples/tiny_cong.json`).

## Algorithm

**probabilistic L-shape routing demand**

## Pseudocode

```text
Input: nets, positions, GCell grid
demand ← zeros(nx, ny)
for each 2-pin net (u,v):
  add 0.5 demand along L-shape H-then-V through GCells
  add 0.5 demand along L-shape V-then-H through GCells
for each multi-pin net:
  c ← bbox center; star edges c→pin; deposit like 2-pin
Output: demand matrix (compare to RUDY on same placement)
```


## Track A API

```bash
# from courses/learn_congestion/
python3 -c "from common.solvers import *; from common.congestionutil import load; d=load('common/tiny_cong.json'); print(d['chip'])"
```

Prefer helpers in `common/congestionutil.py` and `common/solvers.py` over ad-hoc scripts.

## Starter prompts

1. Load `placement` and `congested_seed` from `tiny_cong.json`; print the 4×2 GCell layout.
2. Run the algorithm for this lab; print demand or congestion matrices with two decimals.
3. Compare spread `placement` vs `congested_seed` on total overflow.
4. Change capacity from 2.0 to 1.0 and report which GCells flip oversubscribed.
5. Write one sentence: why this idea belongs before detailed global routing.

## Expected artifacts

- Demand and/or congestion matrix for the 4×2 grid
- Overflow summary (total, max, count) when relevant
- Short note tying the metric to placement feedback
