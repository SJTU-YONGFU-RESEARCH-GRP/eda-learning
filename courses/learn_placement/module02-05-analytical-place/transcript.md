# Analytical / density-aware place

**Module id:** module02-05-analytical-place
**Lab:** analytical-place
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Analytical / density-aware place

Analytical lite first pulls for wirelength, then spreads for density with pads A and D fixed. From starter fifty-two you should land near forty-eight point one—close to quadratic, deliberately above free force, because spreading fights pure collapse.

## Slide 2 — The idea

Wirelength stage clusters; density stage pushes cells out of overloaded bins; a light reconnect keeps HPWL from exploding. Watch both HPWL and overflow—winning wirelength while overflowing every bin is not analytical success.

<!-- algorithm-walkthrough -->

## Slide 3 — Wirelength stage clusters first

![Wirelength stage clusters first](assets/steps/01-wl-stage.png)

Analytical lite starts like force/quadratic: pull for wirelength with pads A and D fixed. Clustering cuts HPWL but can overload bins.

## Slide 4 — Density stage pushes overloaded bins

![Density stage pushes overloaded bins](assets/steps/02-density-stage.png)

A density-repulsion stage pushes cells out of crowded two-by-two bins, then a light reconnect keeps HPWL from exploding.

## Slide 5 — After analytical: about forty-eight point one

![After analytical: about forty-eight point one](assets/steps/03-after-anal.png)

The combined solve lands near forty-eight point one—close to quadratic, deliberately above free force, because spreading fights pure collapse.

## Slide 6 — Report HPWL and overflow

![Report HPWL and overflow](assets/steps/04-both-metrics.png)

Winning wirelength while overflowing every bin is not analytical success. Quote both metrics after the density stage.

## Slide 7 — Wirelength then density

![Wirelength then density](assets/steps/05-takeaway.png)

Analytical lite is a two-act play: cluster for wirelength, spread for density. Lock pads and iteration knobs so forty-eight point one stays reproducible.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **analytical-place** lab from the tools shelf. Load the starter placement, run the algorithm once, and read HPWL—and density when the panel shows it. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module’s examples and the course `common/` solvers. Parse `tiny_place.json`, run the algorithm with a deterministic seed, and print coordinates plus HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads A and D; mixing bbox and clique models in one report; keeping only the final SA iterate instead of the best; and forgetting that timing weights change the objective, not just the label.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
