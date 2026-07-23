# Analytical / density-aware place

**Module id:** module02-05-analytical-place
**Lab:** analytical-place
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Analytical / density-aware place

Placement assigns cell coordinates to cut wirelength while keeping density under control. In this module you’ll implement **analytical lite (wirelength + density spread)** end to end—not a sketch. By the end, you’ll run it on a tiny instance, report HPWL, and know what the algorithm actually does.

## Slide 2 — The idea

analytical lite (wirelength + density spread). You’ll take a placement instance, apply the update rule until a stop condition, and emit coordinates. Watch HPWL every time—and density overflow when the lab uses bins.

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 3 — Browser lab track

In the browser lab track, open the **analytical-place** lab from the tools shelf. Load the starter placement, run the algorithm once, and read the metrics panel. Orient yourself, try one parameter change, then come back to implement the same loop yourself.

## Slide 4 — Implement track

In the implement track, open this module’s examples and build the full algorithm. Parse the tiny placement, run the core loop with clear stop rules, and print coordinates plus metrics. Prefer a deterministic seed so your golden answers stay stable.

## Slide 5 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads; mixing bbox and clique models in one report; and stopping before the best SA iterate is kept.

## Slide 6 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the expected range on the starter placement. When you’re ready, take the short quiz, then continue to the next module.
