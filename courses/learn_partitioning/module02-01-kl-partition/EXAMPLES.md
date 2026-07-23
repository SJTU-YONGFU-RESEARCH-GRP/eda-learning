# Examples — Kernighan–Lin

Track A (implement). Use `examples/tiny_graph.json` and `../../common/solvers.py`.

## Algorithm

**KL pair-swap with prefix rollback**

## Pseudocode

```text
INPUT: bipartition side[], max_passes
OUTPUT: refined side[]
each pass: unlock all; compute D-values
repeat |V|/2: pick unlocked pair max swap gain
  lock pair; update working sides + D
keep prefix with best cumulative gain (>0)
apply prefix; stop if no improving pass
GOLDEN BAD_SEED cut 12 → ABC|DE cut 3
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
