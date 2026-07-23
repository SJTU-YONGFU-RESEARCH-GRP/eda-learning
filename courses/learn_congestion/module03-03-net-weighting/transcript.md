# Congestion-aware net weighting

**Module id:** module03-03-net-weighting
**Lab:** net-weighting
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Pull soft from hotspots

Net weighting raises the cost of nets that cross congested GCells so a weighted placer pulls those pins apart. Weight equals one plus beta times mean congestion under the net bbox.

## Slide 2 — The idea

For each net, average congestion over GCells under its bbox. Scale with beta—one point zero is a clear demo. The four-pin net on a clustered seed should outrank the short E–F net.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **net-weighting**. Compare weights on spread versus congested seeds. Challenges check that a hot net’s weight exceeds a cool net’s weight on your map.

## Slide 4 — Implement track

Implement `net_weights_from_congestion`. Print the six weights for congested_seed. Confirm net index four is among the highest.

## Slide 5 — Pitfalls

Averaging over the whole chip instead of the net bbox. Using demand instead of congestion ratios. Updating weights but forgetting the placer still optimizes unweighted HPWL in the toy lab.

## Slide 6 — Your turn

Finish weighting. Next: one full placement feedback pass.
