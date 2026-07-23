# Examples — Arrival and required

Track A (implement). Use `examples/tiny_timing.json` and `../../common/propagate.py + graph.py`.

## Algorithm

**forward arrival + backward setup required**

## Pseudocode

```text
INPUT: DAG G, period, arrival seeds
OUTPUT: A[], R_setup[]
for p in topo(G):
  A[p]← max over u→p of A[u]+delay   (sources: seed/0)
for sinks: R[p]←period×cycles
for p in reverse_topo:
  R[p]← min over p→v of R[v]−delay
GOLDEN: A[out]=3.2; R[out]=10; R[in]=6.8
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
