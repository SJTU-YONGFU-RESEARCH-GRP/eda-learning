# Overflow metrics

**Module id:** module02-07-overflow-metrics
**Lab:** overflow-metrics
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Numbers that regress

Overflow is demand above capacity. Sum it, take the max, and count how many GCells overflow. Those three numbers become your regression bar for estimators and feedback loops.

## Slide 2 — The idea

ov equals max of zero and demand minus Cap, per tile. Total is the sum. Max is the worst tile. Count is how many tiles have positive overflow. Report all three every time you change placement.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **overflow-metrics**. Start from congested_seed. Move cells outward until total overflow drops below a challenge threshold. Check reads your positions through RUDY—not a mode flag.

## Slide 4 — Implement track

Implement `overflow_metrics`. Assert congested_seed has higher total overflow than spread placement at Cap equals two. Print the triple (total, max, count).

## Slide 5 — Pitfalls

Reporting negative “overflow.” Counting tiles with congestion greater than one while computing overflow from a different Cap. Comparing totals across estimators with incompatible demand units.

## Slide 6 — Your turn

Hit the overflow targets. Next: cell inflation—the first feedback knob.
