# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none (offline)
**Tracks:** offline harness

## Slide 1 — Offline benchmark compare

Toy packers teach mechanism. Benchmarks teach honesty. In this offline module you’ll run the same tiny_modules instances through your floorplan code and, when available, a reference packing—then compare deadspace, density, wirelength proxy, and runtime without pretending the numbers are tape-out sign-off.

## Slide 2 — Fair compare rules

Use identical input and the same outline. Fix seeds when search is randomized. Report the same metrics on both sides. If a reference engine is missing, still run your harness and document the gap—don’t invent golden deadspace. A clean I/O contract matters more than a flashy chart.

## Slide 3 — What good looks like

Expect your educational engine to be slower and sometimes lower quality. That’s fine. You’re looking for legal packings, non-negative deadspace consistent with areas, and improving cost under SA. Huge unexplained wins usually mean a metric mismatch—or an illegal packing you failed to reject.

## Slide 4 — Your turn

Follow the examples file, fill the comparison table, and finish the checklist. Bring one discrepancy and a short hypothesis into your notes. Then continue to the wrap module to close the course.
