# Arrival and required times

**Module id:** module01-03-arrival-required
**Lab:** arrival-required
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Arrival and required times

Static timing analysis answers a hard question without simulation waveforms: given clocks and delays, which paths meet setup and hold? In this module you’ll implement **forward arrival and backward required propagation** end to end—not a sketch. By the end, you’ll run it on a tiny netlist, report the metrics that matter here, and know what the algorithm actually does.

## Slide 2 — The idea

Here’s the core idea in one breath: forward arrival and backward required propagation. You’ll take a timing graph or tagged pin times, apply the update rule until a stop condition, and emit arrivals, required times, slack, or a path—depending on the lab. Watch three habits every time: levelize before you propagate, keep setup and hold separate, and never trust a path you cannot trace.

## Slide 3 — Browser lab track

In the browser lab track, open the **arrival-required** lab from the tools shelf when it ships. Load the starter netlist, run the analysis once, and read the metrics panel—arrivals, required times, slack, or the critical path. Orient yourself, try one parameter change, then come back to implement the same loop yourself.

## Slide 4 — Implement track

In the implement track, open this module’s examples and build the full algorithm. Parse the tiny timing JSON, run the core loop with clear stop rules, and print the tags plus metrics. Prefer a deterministic netlist so your golden answers stay stable. If something looks wrong, dump levels or pin times—debugging the graph is part of the learning.

## Slide 5 — Pitfalls

Common traps: propagating before the graph is levelized; mixing setup and hold in one number; treating false paths as free without updating endpoints; and full-chip rebuilds when only a cone changed. For incremental work, remember invalidate then recompute—not silent stale tags.

## Slide 6 — Your turn

Complete the checklist for at least one track—preferably both. Implement the algorithm until your metrics match the expected range on the starter netlist. When you’re ready, take the short quiz, then continue to the next module in this section.
