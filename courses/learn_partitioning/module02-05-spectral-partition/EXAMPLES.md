# Examples — Spectral bipartition

Track A (implement). Use `examples/tiny_graph.json` and `../../common/solvers.py`.

## Algorithm

**Fiedler order + balanced cut sweep**

## Pseudocode

```text
INPUT: weighted undirected G
OUTPUT: side[] bipartition
L ← Laplacian; take Fiedler eigenvector
order ← nodes sorted by Fiedler value
sweep balanced prefixes; pick min cutsize
GOLDEN: DE|ABC (or ABC|DE) cut=3
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
