# Placement feedback loop

**Module id:** module04-01-placement-feedback
**Lab:** placement-feedback
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Close the loop

Congestion estimation matters when it changes placement. One toy pass: RUDY → congestion → inflate → push cells from overflowing GCells toward quieter neighbors → remeasure overflow.

## Slide 2 — The idea

After inflation, each movable cell in an overflowing tile takes a step toward the neighbor GCell with least overflow. Clamp to the chip. Recompute RUDY. On congested_seed you should see total overflow drop after one pass—not to zero, but clearly down.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **placement-feedback**. Run the feedback helper, then nudge further if needed to clear challenges. Check scores post-feedback overflow from your positions.

## Slide 4 — Implement track

Implement `placement_feedback_lite`. Print overflow before and after on congested_seed. Assert after is strictly less than before at Cap equals two.

## Slide 5 — Pitfalls

Pushing macros that should stay fixed. Infinite oscillation from oversized steps—use a fraction of GCell size. Declaring victory without recomputing demand after the move.

## Slide 6 — Your turn

Complete the feedback lab and offline compare next. Then the wrap points you to global routing.
