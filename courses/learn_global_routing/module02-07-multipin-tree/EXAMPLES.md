# Examples — Multi-pin tree (Steiner-lite)

Track A (implement). Use the tiny global routing instance first (`examples/tiny_gr.json`).

## Algorithm

**multipin star tree (bbox-center Steiner-lite)**

## Pseudocode

```text
Input: pin GCells pins[]
center ← bbox-center GCell of pins
for each pin p in pins:
  add L-route(center, p, HV) edges to tree
Output: union of L legs (Steiner-lite star)
Golden: 4-corner pins share hub near (1,0)
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
