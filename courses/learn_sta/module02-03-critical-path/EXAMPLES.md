# Examples — Critical path

Track A (implement). Use `examples/tiny_timing.json` and `../../common/propagate.py + graph.py`.

## Algorithm

**backtrace worst path using arrivals**

## Pseudocode

```text
INPUT: G, A[], sink
OUTPUT: pin path (source→…→sink)
path←[sink]; cur←sink
while cur has preds:
  pick u→cur with A[u]+delay == A[cur]
  (tie-break: largest A[u])
  prepend u; cur←u
return path
GOLDEN: in→u1/A→u1/Y→u2/A→u2/Y→out
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
