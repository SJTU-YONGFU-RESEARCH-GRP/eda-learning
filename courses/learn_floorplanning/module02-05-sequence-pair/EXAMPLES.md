# Examples — Sequence pair

Track A (implement). Use `examples/tiny_modules.json` and `../../common/solvers.py`.

## Algorithm

**longest-path pack from pos/neg**

## Pseudocode

```text
INPUT: pos[], neg[] permutations of modules
OUTPUT: (x,y) via constraint longest paths
pos/neg order ⇒ horizontal & vertical constraints
x ← longest path in H-graph; y ← V-graph
GOLDEN pos=A B C E D; neg=D A B C E
packs legally with non-negative coords
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
