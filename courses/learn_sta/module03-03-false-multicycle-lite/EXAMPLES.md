# Examples — False and multicycle lite

Track A (implement). Use `examples/tiny_timing.json` and `../../common/propagate.py + graph.py`.

## Algorithm

**disable arcs + setup_cycles×period**

## Pseudocode

```text
INPUT: G, disable set S, setup_cycles
OUTPUT: setup slack at sink
A ← prop_arrival using arcs ∉ S
R ← prop_required; R[sink]←period×cycles
slack ← R[sink] − A[sink]
GOLDEN default: slack(out)=6.8
cycles=2 → R[out]=20, slack=16.8
disable u1/Y→u2/A breaks that path
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
