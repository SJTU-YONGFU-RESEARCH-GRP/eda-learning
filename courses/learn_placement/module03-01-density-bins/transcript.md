# Density bins and overflow

**Module id:** module03-01-density-bins
**Lab:** density-bins
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Density bins and overflow

Density bins count cells on a grid and sum overflow above capacity. On a two-by-two grid with capacity one, both starter and golden still overflow by two—compact HPWL does not automatically mean legal density. Raise capacity to two on golden and overflow drops to one.

## Slide 2 — The idea

Assign each cell to a bin by coordinates, count occupants, then overflow equals sum of max(zero, count minus capacity). Report HPWL and overflow together. A pretty wirelength with piled bins fails the density half of placement.

<!-- algorithm-walkthrough -->

## Slide 3 — Partition the die into bins

![Partition the die into bins](assets/steps/01-grid-idea.png)

Density bins count cells on a regular grid. Default teaching grid is two-by-two over [0,8]×[0,8]. Capacity one means each bin may hold one cell before overflow.

## Slide 4 — Starter overflows by two

![Starter overflows by two](assets/steps/02-starter-overflow.png)

On the spread starter with capacity one, two bins hold two cells each. Overflow sums to two even though HPWL is already fifty-two.

## Slide 5 — Golden also overflows at cap one

![Golden also overflows at cap one](assets/steps/03-golden-still-overflow.png)

Compact HPWL fourteen still piles three cells into one bin. Overflow remains two at capacity one—pretty wirelength is not automatic legality.

## Slide 6 — Raise capacity to ease overflow

![Raise capacity to ease overflow](assets/steps/04-raise-capacity.png)

With capacity two on the golden placement, overflow drops to one. Capacity is part of the spec—quote it with the overflow number.

## Slide 7 — HPWL and density travel together

![HPWL and density travel together](assets/steps/05-takeaway.png)

Always report wirelength and bin overflow. A placement that wins HPWL while stacking bins fails the density half of the story.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **density-bins** lab from the tools shelf. Load the starter placement, run the algorithm once, and read HPWL—and density when the panel shows it. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module’s examples and the course `common/` solvers. Parse `tiny_place.json`, run the algorithm with a deterministic seed, and print coordinates plus HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads A and D; mixing bbox and clique models in one report; keeping only the final SA iterate instead of the best; and forgetting that timing weights change the objective, not just the label.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
