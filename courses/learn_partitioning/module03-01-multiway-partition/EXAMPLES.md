# Examples — Multiway partitioning

Track A (implement). Use `examples/tiny_graph.json` and `../../common/solvers.py`.

## Algorithm

**recursive bisection vs round-robin k-way**

## Pseudocode

```text
INPUT: G, k
OUTPUT: k-way assignment + cutsize
method A: recursive_bisection(G,k)
method B: round-robin / block assign labels
cut ← Σ w where side[u]≠side[v]
GOLDEN k=3 recursive: AB|C|DE cut=8
round-robin alphabetic: cut≈18 (worse)
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
