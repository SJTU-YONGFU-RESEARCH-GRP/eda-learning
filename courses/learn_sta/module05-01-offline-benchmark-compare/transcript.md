# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none (offline)
**Tracks:** offline harness

## Slide 1 — Offline benchmark compare

Toy engines teach mechanism. Benchmarks teach honesty. In this offline module you’ll run the same tiny netlists through your STA and, when available, an open external timer—then compare WNS, TNS, and path delay without pretending the numbers are foundry sign-off.

## Slide 2 — Fair compare rules

Use identical input. Fix clocks and library delays. Report the same metrics on both sides. If the external tool is missing, still run your harness and document the install gap—don’t invent golden numbers. A clean I/O contract matters more than a flashy chart.

## Slide 3 — What good looks like

Expect your educational engine to be slower and sometimes less complete. That’s fine. You’re looking for the same qualitative behavior: matching worst paths, consistent slack signs, and no silent illegal tags. Huge unexplained wins usually mean a metric or exception mismatch, not genius.

## Slide 4 — Your turn

Follow the examples file, fill the comparison table, and finish the checklist. Bring one discrepancy and a short hypothesis into your notes. Then continue to the wrap module to close the course.
