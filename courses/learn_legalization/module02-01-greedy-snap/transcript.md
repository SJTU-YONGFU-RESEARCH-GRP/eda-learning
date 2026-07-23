# Greedy snap

**Module id:** module02-01-greedy-snap
**Lab:** greedy-snap
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Greedy snap

Global placement leaves fractional coordinates—the float seed puts A near (3.7, 1.2) and B near (4.1, 1.4). Greedy snap rounds x to the nearest site and y to the nearest row. A lands at (4, 2)—the same site as B.

## Slide 2 — The idea

Snap quantizes coordinates but does not remove overlap. After snap, A and B still fail with overlap A/B. Teaching point: snap is necessary, not sufficient—you need overlap removal or Abacus packing next.

<!-- algorithm-walkthrough -->

## Slide 3 — Float placement from global place

![Float placement from global place](assets/steps/01-float-seed.png)

After global placement, cells sit at fractional coordinates—A near (3.7, 1.2), B near (4.1, 1.4). Nothing is site-aligned yet; that is the float seed for greedy snap.

## Slide 4 — Snap every cell to nearest site

![Snap every cell to nearest site](assets/steps/02-snap-all.png)

Greedy snap rounds x to the nearest site and y to the nearest row. A lands at (4, 2)—same as B. C snaps to (5, 2). D, E, and F snap to their row neighbors.

## Slide 5 — Still illegal: A/B overlap

![Still illegal: A/B overlap](assets/steps/03-still-overlap.png)

After snap, A and B still share (4, 2). The legality report again says overlap A/B. Snap alone does not legalize—it only quantizes coordinates.

## Slide 6 — Teaching point: snap ≠ legal

![Teaching point: snap ≠ legal](assets/steps/04-snap-not-legal.png)

Students often assume rounding fixes everything. On this instance greedy snap creates the same middle-row pile as the integer overlap seed. Legalization needs a second phase.

## Slide 7 — Next: overlap removal / Abacus

![Next: overlap removal / Abacus](assets/steps/05-next-phase.png)

Follow snap with per-row packing or Abacus row assignment. Overlap removal spreads A, B, C along row two; Abacus spreads them across rows with lower displacement.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **greedy-snap** lab from the tools shelf. Load the overlap or float starter, run the legalizer once, and read legality plus displacement and HPWL when the panel shows them. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module's examples and the course `common/` solvers. Parse `tiny_legal.json`, run the algorithm with deterministic coordinates, and print legality, displacement, and HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: assuming snap alone legalizes; forgetting site width when checking overlap; ignoring fixed macro D at (8, 4); reporting HPWL without legality; and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.
