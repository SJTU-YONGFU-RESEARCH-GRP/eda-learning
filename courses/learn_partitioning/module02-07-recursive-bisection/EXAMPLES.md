# Examples — Recursive bisection

Track A (implement). Use `examples/tiny_graph.json` and `../../common/solvers.py`.

## Algorithm

**repeat bipartition until k parts**

## Pseudocode

```text
INPUT: G, target k parts
OUTPUT: side[v] ∈ {0..k−1}
parts ← {all nodes}
while |parts| < k:
  pick largest part P
  bipartition P (spectral/KL/FM)
  replace P with the two halves
GOLDEN k=2: ABC|DE cut=3
k=3 continues on ABC → AB|C|DE
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
