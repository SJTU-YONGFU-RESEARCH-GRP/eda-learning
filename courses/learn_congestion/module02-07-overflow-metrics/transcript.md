# Overflow metrics

**Module id:** module02-07-overflow-metrics
**Lab:** overflow-metrics
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Numbers that regress

Overflow is demand above capacity. Sum it, take the max, and count how many GCells overflow. Those three numbers become your regression bar for estimators and feedback loops.

## Slide 2 — The idea

ov equals max of zero and demand minus Cap, per tile. Total is the sum. Max is the worst tile. Count is how many tiles have positive overflow. Report all three every time you change placement.

<!-- algorithm-walkthrough -->

## Slide 3 — Define overflow

![Define overflow](assets/steps/01-def.png)

ov = max(0, demand−Cap) per tile.

## Slide 4 — Total overflow

![Total overflow](assets/steps/02-total.png)

Sum of per-tile overflow—primary regression number.

## Slide 5 — Max overflow

![Max overflow](assets/steps/03-max.png)

Worst tile—catches hotspots even when total is moderate.

## Slide 6 — Congested count

![Congested count](assets/steps/04-count.png)

How many tiles overflow—useful for “how widespread”.

## Slide 7 — Hit a target

![Hit a target](assets/steps/05-target.png)

Move cells until total/max/count clear challenge thresholds.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Open **overflow-metrics**. Start from congested_seed. Move cells outward until total overflow drops below a challenge threshold. Check reads your positions through RUDY—not a mode flag.

## Slide 9 — Implement track

Implement `overflow_metrics`. Assert congested_seed has higher total overflow than spread placement at Cap equals two. Print the triple (total, max, count).

## Slide 10 — Pitfalls

Reporting negative “overflow.” Counting tiles with congestion greater than one while computing overflow from a different Cap. Comparing totals across estimators with incompatible demand units.

## Slide 11 — Your turn

Hit the overflow targets. Next: cell inflation—the first feedback knob.
