# Timing-driven placement

**Module id:** module04-01-timing-driven-place
**Lab:** timing-driven-place
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Timing-driven placement

Timing-driven place weights critical nets in the wirelength objective. On the starter, plain HPWL is fifty-two but timing-weighted HPWL is one hundred sixteen because the four-pin net carries weight five. The compact golden drops timing-weighted cost to thirty.

## Slide 2 — The idea

Multiply each net’s HPWL by its criticality weight and sum. Heavy weights pull critical nets shorter even when plain HPWL looks fine. Always report both plain and weighted totals so you can see what the objective actually optimized.

<!-- algorithm-walkthrough -->

## Slide 3 — Plain HPWL hides critical nets

![Plain HPWL hides critical nets](assets/steps/01-plain-vs-weighted.png)

On the starter, plain HPWL is fifty-two, but timing-weighted HPWL is one hundred sixteen because the four-pin net carries weight five.

## Slide 4 — Weighted sum of net HPWLs

![Weighted sum of net HPWLs](assets/steps/02-weight-math.png)

Multiply each net’s bbox HPWL by its criticality and sum. The critical ABCD net alone contributes five times sixteen equals eighty on the starter.

## Slide 5 — Golden timing cost drops to thirty

![Golden timing cost drops to thirty](assets/steps/03-golden-timing.png)

The compact golden cuts the critical bbox sharply. Timing-weighted HPWL falls from one hundred sixteen to thirty while plain HPWL hits fourteen.

## Slide 6 — Always quote plain and weighted

![Always quote plain and weighted](assets/steps/04-both-reports.png)

A placement can look fine on plain HPWL while the critical net stays long. Timing labs demand both numbers so the objective is visible.

## Slide 7 — Weights change what you optimize

![Weights change what you optimize](assets/steps/05-takeaway.png)

Timing-driven place is still wirelength—just weighted. Remember one hundred sixteen to thirty on this instance, and never drop the plain HPWL report.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **timing-driven-place** lab from the tools shelf. Load the starter placement, run the algorithm once, and read HPWL—and density when the panel shows it. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module’s examples and the course `common/` solvers. Parse `tiny_place.json`, run the algorithm with a deterministic seed, and print coordinates plus HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads A and D; mixing bbox and clique models in one report; keeping only the final SA iterate instead of the best; and forgetting that timing weights change the objective, not just the label.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
