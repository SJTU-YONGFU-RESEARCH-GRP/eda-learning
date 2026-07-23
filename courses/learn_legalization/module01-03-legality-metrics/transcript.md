# Legality metrics

**Module id:** module01-03-legality-metrics
**Lab:** legality-metrics
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Legality metrics

Before you celebrate wirelength, ask whether the placement is legal. On the overlap seed the checker fails with overlap A/B—three cells share the middle row at x four. The golden reference passes with reason ok.

## Slide 2 — The idea

Check on-row placement, site alignment, in-chip bounds, and pairwise overlap. Report displacement as L1 Manhattan distance from the origin layout—Abacus moves four total units on this instance, overlap removal moves six. Pair legality with HPWL after legalize.

<!-- algorithm-walkthrough -->

## Slide 3 — Overlap seed is illegal

![Overlap seed is illegal](assets/steps/01-overlap-illegal.png)

Starting from the overlap placement, the checker reports overlap A/B first—three cells share the middle row at x equals four. That single reason is enough to fail legality.

## Slide 4 — Four legality checks

![Four legality checks](assets/steps/02-checks.png)

A legal placement must be on-row, site-aligned, inside the chip, and overlap-free. Fixed macros add a fifth check later—did the macro move off its lock?

## Slide 5 — Golden placement passes

![Golden placement passes](assets/steps/03-golden-ok.png)

The golden reference satisfies every check: reason ok, legal true. Use it as the positive control when you unit-test your legality reporter.

## Slide 6 — Displacement: L1 from origin

![Displacement: L1 from origin](assets/steps/04-displacement.png)

Displacement sums Manhattan distance per cell from a reference layout—here the overlap seed. Abacus later moves cells only four total units; overlap removal moves six.

## Slide 7 — HPWL after legalize

![HPWL after legalize](assets/steps/05-hpwl-after.png)

Wirelength still matters: Abacus lands at HPWL thirty-eight with displacement four; Tetris-style packing hits HPWL thirty-two with displacement six. Always pair legality with both metrics.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **legality-metrics** lab from the tools shelf. Load the overlap or float starter, run the legalizer once, and read legality plus displacement and HPWL when the panel shows them. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module's examples and the course `common/` solvers. Parse `tiny_legal.json`, run the algorithm with deterministic coordinates, and print legality, displacement, and HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: assuming snap alone legalizes; forgetting site width when checking overlap; ignoring fixed macro D at (8, 4); reporting HPWL without legality; and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.
