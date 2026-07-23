# Examples — Incremental update

Track A (implement). Use `examples/tiny_timing.json` and `../../common/propagate.py + graph.py`.

## Algorithm

**invalidate fanout cone; recompute A**

## Pseudocode

```text
INPUT: G, edit u→v delay:=d', A_old
OUTPUT: A_new, invalidated cone
set delay(u,v)←d'
inv ← BFS successors from v (incl. v)
delete A[p] for p in inv
recompute A in topo order for missing pins
GOLDEN edit 1.2→2.0 on u1 cell:
  inv={u1/Y,u2/A,u2/Y,out}; A[out]=4.0
```

## Starter prompts

1. Implement the pseudocode above (or call the matching `common/` helper).
2. Print the metrics named in the GOLDEN line; match browser / Track A tests.
3. Change one knob and report what moved.

## Expected artifacts

- Outputs listed in the pseudocode OUTPUT line
- Note tying the run to the pseudocode phases

## Stretch

Scale the instance slightly; keep the same metrics API.
