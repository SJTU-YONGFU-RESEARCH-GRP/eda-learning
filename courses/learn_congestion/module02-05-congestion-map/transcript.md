# Congestion heat map

**Module id:** module02-05-congestion-map
**Lab:** congestion-map
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Demand over capacity

Congestion is a ratio: demand divided by capacity. A heat map paints that ratio per GCell so you can point at the hottest tile without reading a matrix of floats aloud.

## Slide 2 — The idea

cong[i][j] equals demand[i][j] over Cap. Values above one are oversubscribed. The hottest GCell is the argmax. On the congested seed, expect the center columns to light up first.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **congestion-map**. Read the heat legend. Move cells until a different GCell becomes hottest, then Check. Study reveal shows a reference map—do not rely on it to pass.

## Slide 4 — Implement track

Build `congestion_map(demand, capacity)` returning the ratio matrix and hottest index. Print hottest for both placement seeds.

## Slide 5 — Pitfalls

Dividing by zero capacity. Coloring by raw demand while labeling the plot “congestion.” Breaking ties in argmax nondeterministically—pick a fixed scan order.

## Slide 6 — Your turn

Finish the lab. Next: overflow metrics compress the map into totals you can regress.
