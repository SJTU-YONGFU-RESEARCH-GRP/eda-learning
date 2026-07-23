# Examples — Incremental timing update

Track A (implement). Use tiny timing netlists first (handful of cells / pins).

## Algorithm

**incremental invalidate / recompute on a delay edit**

## Starter prompts

1. Restate the algorithm in five bullets (inputs → loop → stop → output).
2. Run it on the tiny netlist in `examples/tiny_timing.json` (create if missing).
3. Report the metrics this module cares about (levels, arrival, required, slack, path, …).
4. Change one input (clock period, arc delay, exception) and report what moved.
5. Name one failure mode (wrong levelization, missed endpoint, stale incremental cone, …).

## Expected artifacts

- Timing graph or tagged pin times (as applicable)
- Slack and/or critical path for the starter clocks
- Short note: why this step belongs on the STA shelf

## Stretch

Scale to ~50 cells; keep the same API as the tiny case.
