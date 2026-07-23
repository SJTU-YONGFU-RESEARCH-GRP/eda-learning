# Examples — Terminal propagation

Track A (implement). Use `examples/tiny_graph.json` and `../../common/solvers.py`.

## Algorithm

**fix terminals; partition free cells**

## Pseudocode

```text
INPUT: G, fixed terminals T with side
OUTPUT: side for free cells
lock every t∈T at its side
partition free nodes (KL/FM/spectral)
treat T as immovable during moves
report cutsize with terminals included
GOLDEN: fixed terminals steer free cells
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
