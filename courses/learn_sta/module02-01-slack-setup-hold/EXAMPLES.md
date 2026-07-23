# Examples — Slack setup and hold

Track A (implement). Use `examples/tiny_timing.json` and `../../common/propagate.py + graph.py`.

## Algorithm

**setup slack R−A; hold lite A−Rhold**

## Pseudocode

```text
INPUT: A[], R_setup[], R_hold[] (lite)
OUTPUT: setup_slack, hold_slack, meet?
setup_slack(p) ← R_setup[p] − A[p]
hold_slack(p)  ← A[p] − R_hold[p]
R_hold[sink] ← 0 in this lite model
meet_setup if setup_slack(sink)≥0
meet_hold  if hold_slack(sink)≥0
GOLDEN: setup(out)=6.8; hold(out)=3.2
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
