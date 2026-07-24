# Congestion-aware net weighting

**Module id:** module03-03-net-weighting
**Lab:** net-weighting
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Pull soft from hotspots

Net weighting raises the cost of nets that cross congested GCells so a weighted placer pulls those pins apart. Weight equals one plus beta times mean congestion under the net bbox.

## Slide 2 — The idea

For each net, average congestion over GCells under its bbox. Scale with beta—one point zero is a clear demo. The four-pin net on a clustered seed should outrank the short E–F net.

<!-- algorithm-walkthrough -->

## Slide 3 — Weight hot nets

![Weight hot nets](assets/steps/01-idea.png)

Nets through congested GCells get larger weights for weighted place.

## Slide 4 — Mean under bbox

![Mean under bbox](assets/steps/02-bbox.png)

Average congestion over GCells under the net bbox—not the whole chip.

## Slide 5 — 4-pin ranks high

![4-pin ranks high](assets/steps/03-rank.png)

On a cluster, the 4-pin net outranks short E–F.

## Slide 6 — Spread lowers weights

![Spread lowers weights](assets/steps/04-cool.png)

As congestion falls, weights ease back toward 1.

## Slide 7 — Use in placer

![Use in placer](assets/steps/05-use.png)

Weighted HPWL pulls soft from hotspots—pair with inflators.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Open **net-weighting**. Compare weights on spread versus congested seeds. Challenges check that a hot net’s weight exceeds a cool net’s weight on your map.

## Slide 9 — Implement track

Implement `net_weights_from_congestion`. Print the six weights for congested_seed. Confirm net index four is among the highest.

## Slide 10 — Pitfalls

Averaging over the whole chip instead of the net bbox. Using demand instead of congestion ratios. Updating weights but forgetting the placer still optimizes unweighted HPWL in the toy lab.

## Slide 11 — Your turn

Finish weighting. Next: one full placement feedback pass.
