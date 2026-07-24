# L-shape pattern routes

**Module id:** module02-01-pattern-l-route
**Lab:** pattern-l-route
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — The simplest global path

Two-pin global routing often starts with an L: travel along one axis, then the other. It is fast, deterministic, and good enough to teach edge usage before maze search or rip-up.

## Slide 2 — The idea

Given terminals a and b, prefer HV walks horizontal to align columns then vertical to the row; prefer VH swaps the order. Emit the list of GCells visited and convert consecutive pairs to edges with path_to_edges. A path from zero comma zero to two comma one in HV uses three edges.

<!-- algorithm-walkthrough -->

## Slide 3 — L-shape

![L-shape](assets/steps/01-idea.png)

Two-pin nets use one bend: HV (horizontal first) or VH.

## Slide 4 — Route L-HV

![Route L-HV](assets/steps/02-hv.png)

Spread placement L-HV yields documented overflow.

## Slide 5 — Route L-VH

![Route L-VH](assets/steps/03-vh.png)

Swapping bend order changes which edges saturate.

## Slide 6 — Edge usage

![Edge usage](assets/steps/04-edges.png)

Thicker edges show usage; red dash marks overflow.

## Slide 7 — Move pins

![Move pins](assets/steps/05-move.png)

Moving cells changes terminal GCells and L paths.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Open **pattern-l-route**. Route A to B with HV and read the highlighted edges. Toggle VH on the same pair and compare the bend GCell.

## Slide 9 — Implement track

Implement `l_route(a, b, prefer)` and `path_to_edges`. Route net A–B on tiny_gr and print the edge list. Match the browser overlay.

## Slide 10 — Pitfalls

Skipping duplicate GCells at the bend. Returning directed edges inconsistently—always normalize undirected keys. Forgetting that L routes ignore existing congestion until sequential routing.

## Slide 11 — Your turn

Ship Track A L-routes and clear browser challenges. Next: Z-shape patterns when you want a third segment.
