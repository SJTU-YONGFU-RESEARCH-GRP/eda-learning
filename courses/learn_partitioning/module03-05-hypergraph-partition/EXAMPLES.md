# Examples — Hypergraph partitioning

Track A (implement). Use `examples/tiny_graph.json` and `../../common/solvers.py`.

## Algorithm

**hyperedge cut (span >1 part)**

## Pseudocode

```text
INPUT: hyperedges e={pins…}, side[]
OUTPUT: hyperedge_cut
cut ← count edges with |{side[p]:p∈e}| > 1
(optional) expand to pairwise clique for KL/FM
GOLDEN ABC|DE: one cut net on starter H
pairwise clique expansion can differ
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
