# Placement feedback loop

**Module id:** module04-01-placement-feedback
**Lab:** placement-feedback
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Close the loop

Congestion estimation matters when it changes placement. One toy pass: RUDY → congestion → inflate → push cells from overflowing GCells toward quieter neighbors → remeasure overflow.

## Slide 2 — The idea

After inflation, each movable cell in an overflowing tile takes a step toward the neighbor GCell with least overflow. Clamp to the chip. Recompute RUDY. On congested_seed you should see total overflow drop after one pass—not to zero, but clearly down.

<!-- algorithm-walkthrough -->

## Slide 3 — Hot starter

![Hot starter](assets/steps/01-seed.png)

Congested seed starts with total overflow 5 at Cap=2.

## Slide 4 — Estimate

![Estimate](assets/steps/02-estimate.png)

Run RUDY → congestion → overflow per tile.

## Slide 5 — Push outward

![Push outward](assets/steps/03-push.png)

Cells in overflowing tiles step toward the quietest neighbor GCell.

## Slide 6 — Overflow drops

![Overflow drops](assets/steps/04-after.png)

After one feedback pass, total overflow falls (often to ~0 on this toy).

## Slide 7 — Toward routing

![Toward routing](assets/steps/05-next.png)

Real flows iterate with global routing; next course deepens GCell edges.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Open **placement-feedback**. Run the feedback helper, then nudge further if needed to clear challenges. Check scores post-feedback overflow from your positions.

## Slide 9 — Implement track

Implement `placement_feedback_lite`. Print overflow before and after on congested_seed. Assert after is strictly less than before at Cap equals two.

## Slide 10 — Pitfalls

Pushing macros that should stay fixed. Infinite oscillation from oversized steps—use a fraction of GCell size. Declaring victory without recomputing demand after the move.

## Slide 11 — Your turn

Complete the feedback lab and offline compare next. Then the wrap points you to global routing.
