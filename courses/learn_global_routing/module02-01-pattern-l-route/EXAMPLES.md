# Examples — L-shape pattern routes

Track A (implement). Use the tiny global routing instance first (`examples/tiny_gr.json`).

## Algorithm

**L-shape pattern routing (HV / VH)**

## Pseudocode

```text
Input: terminals a=(i0,j0), b=(i1,j1), prefer HV or VH
path ← [a]
if HV: walk horizontal to (i1,j0), then vertical to b
if VH: walk vertical to (i0,j1), then horizontal to b
Output: GCell path; edges = consecutive pairs
Golden: (0,0)→(2,1) HV uses 3 edges
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
