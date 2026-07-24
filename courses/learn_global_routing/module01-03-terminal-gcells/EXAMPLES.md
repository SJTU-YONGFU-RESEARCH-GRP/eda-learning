# Examples — Pin terminals on GCells

Track A (implement). Use the tiny global routing instance first (`examples/tiny_gr.json`).

## Algorithm

**pin terminal GCell assignment**

## Pseudocode

```text
Input: placement pin (x,y), gcell nx×ny, cellW, cellH
(i,j) ← cell_gcell(x,y)   # clamp floor divide
terminals[cell_id] ← (i,j)
Output: map cell → GCell terminal
Golden: A at (1,1) → (0,0); D at (8,5) → (2,1)
```


## Track A API

```bash
# from courses/learn_global_routing/
python3 -c "from common.solvers import route_from_data; from common.grutil import load; d=load('common/tiny_gr.json'); print(route_from_data(d))"
```

Prefer helpers in `common/grutil.py` and `common/solvers.py` over ad-hoc scripts.

## Starter prompts

1. Load `placement` and `nets` from `tiny_gr.json`; print the 4×2 GCell layout and edge count.
2. Run the algorithm for this lab; print edge usage or overflow with two decimals.
3. Compare sequential L-HV vs maze on total edge overflow.
4. Change edge_capacity from 2 to 1 and report which edges flip congested.
5. Write one sentence: why this idea belongs before detailed routing.

## Expected artifacts

- Edge usage map or path listing for the lab algorithm
- Overflow summary (total, max, count) when relevant
- Short note tying the metric to rip-up or sequential order
