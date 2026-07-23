# Examples — Multilevel partitioning

Track A (implement). Use `examples/tiny_graph.json` and `../../common/solvers.py`.

## Algorithm

**coarsen → partition → project → refine**

## Pseudocode

```text
INPUT: G, coarsen until tiny
OUTPUT: fine side[]
coarsen: match/cluster heavy edges
partition coarse (spectral/KL/FM)
project labels to finer level
refine with FM/KL at each uncoarsen
GOLDEN project ABC|DE cut=3; refine keeps 3
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
