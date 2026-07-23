# Fixed-outline constraints

**Module id:** module01-01-fixed-outline
**Lab:** fixed-outline
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Fixed-outline constraints

Floorplanning on this course uses a fixed outline ten by eight. Modules A through E must pack inside—no growing the chip. In this lab you’ll reject illegal packings before you ever talk about density.

<!-- algorithm-walkthrough -->

## Slide 2 — Fixed outline is 10×8

![Fixed outline is 10×8](assets/steps/01-outline.png)

Modern floorplanning starts with a fixed outline. Ours is ten by eight—area eighty. Modules A through E must pack inside; growing the chip is not allowed.

## Slide 3 — Bad pack: E overflows

![Bad pack: E overflows](assets/steps/02-bad-overflow.png)

The bad seed places E at x equals nine with width two, so it sticks past the right edge. Legality fails immediately—E is outside the outline.

## Slide 4 — Overlap is also illegal

![Overlap is also illegal](assets/steps/03-overlap.png)

A second failure mode: E sits on top of C. Edge-touching is fine; positive-area interior overlap is not. The checker reports C overlaps E.

## Slide 5 — Golden pack is legal

![Golden pack is legal](assets/steps/04-golden.png)

The golden packing keeps every block inside ten by eight with no overlaps. A sits at the origin; B, C, and E march right; D stacks above A.

## Slide 6 — Legality is the gate

![Legality is the gate](assets/steps/05-takeaway.png)

Never optimize density or wirelength on an illegal packing. Fix containment and overlap first—then the metrics in the next lab mean something.

<!-- /algorithm-walkthrough -->


## Slide 7 — Browser lab track

Open the fixed-outline lab. Show the bad seed: E overflows past the right edge. Then show overlap, then golden. Watch legality flip from false to true when the golden packing loads.

## Slide 8 — Implement track

Parse tiny_modules.json, assign (x, y), and implement containment plus pairwise non-overlap. On the golden packing, legality must pass; on the bad seed with E at nine, it must fail with E outside the outline.

## Slide 9 — Pitfalls

Off-by-one edges, treating centers as rectangles, and celebrating density on illegal layouts. Edge-touching is allowed; interior overlap is not.

## Slide 10 — Your turn

Get a legal packing of A through E inside ten by eight. Quiz checks the overflow failure and the golden pass. Next: deadspace fifty-seven on this same instance.
