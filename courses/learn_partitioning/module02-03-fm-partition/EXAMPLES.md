# Examples — Fiduccia–Mattheyses

Track A (implement). Use `examples/tiny_graph.json` and `../../common/solvers.py`.

## Algorithm

**FM single-vertex moves + balance**

## Pseudocode

```text
INPUT: side[], balance_tol, max_passes
OUTPUT: refined side[]
each pass: while unlocked legal moves exist:
  pick v with max gain among balance-ok flips
  lock v; flip on working copy
keep best positive-gain prefix; apply
stop when a pass cannot improve
GOLDEN BAD_SEED → flip D then A → cut 3
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
