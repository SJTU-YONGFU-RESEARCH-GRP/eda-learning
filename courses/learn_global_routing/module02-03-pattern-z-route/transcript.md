# Z-shape pattern routes

**Module id:** module02-03-pattern-z-route
**Lab:** pattern-z-route
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Three segments

When pins are not on the same row or column, an L is not your only pattern. A Z bends twice: horizontal to a midpoint column, vertical, then horizontal to the destination—or the vertical-first variant.

## Slide 2 — The idea

If a and b share a row or column, fall back to L-route. Otherwise with prefer HZ pick mid column as the average of the two columns, walk H–V–H. path_to_edges should show at least three edges for off-axis pairs like zero comma zero to three comma one.

<!-- algorithm-walkthrough -->

## Slide 3 — Two bends

![Two bends](assets/steps/01-z.png)

Z-route uses a midpoint column (or row) with two corners.

## Slide 4 — A–D Z path

![A–D Z path](assets/steps/02-ab.png)

On spread, Z from A to D shows the mid-column bend.

## Slide 5 — L reference

![L reference](assets/steps/03-l.png)

L-HV is the fast pattern route baseline.

## Slide 6 — Overflow tradeoff

![Overflow tradeoff](assets/steps/04-ov.png)

Extra bends can spread or concentrate edge usage.

## Slide 7 — Maze escape

![Maze escape](assets/steps/05-next.png)

When L/Z overflow, maze search detours.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Open **pattern-z-route**. Compare Z versus L on B to D. Note the extra bend GCell and how edge usage shifts.

## Slide 9 — Implement track

Implement `z_route(a, b, prefer)`. Print Z and L paths for the same terminal pair; explain one edge difference.

## Slide 10 — Pitfalls

Using a midpoint that leaves zero-length segments. Not falling back to L on aligned pins. Confusing Z prefer HZ with L prefer HV naming.

## Slide 11 — Your turn

Finish Z routing on two-pin nets. Next: maze routing that respects congested edges.
