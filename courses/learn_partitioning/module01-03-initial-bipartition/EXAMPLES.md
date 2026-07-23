# Examples — Initial bipartition

Track A (implement). Use `examples/tiny_graph.json` and `../../common/solvers.py`.

## Algorithm

**random / greedy / grow seed bipartition**

## Pseudocode

```text
INPUT: graph G, method ∈ {random,greedy,grow}
OUTPUT: legal side[v] ∈ {0,1}
random(seed): shuffle; split by half
greedy: keep heaviest edges internal when able
grow(seed): expand frontier until size budget
report cutsize + balance for every seed
GOLDEN: grow(D)→DE|ABC cut=3
random(7)→AE|BCD cut=12
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
