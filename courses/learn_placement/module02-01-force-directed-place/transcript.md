# Force-directed placement

**Module id:** module02-01-force-directed-place
**Lab:** force-directed-place
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Force-directed placement

Force-directed place pulls each free cell toward the average of its net neighbors, plus a weak center pull. From the starter HPWL of fifty-two, a few lite iterations land near eighteen point seven—better wirelength, still above the golden fourteen.

## Slide 2 — The idea

Each iteration: for free cells, blend current position toward the neighbor average with a small alpha. Fixed pads stay put. Too much alpha collapses the design; too little barely moves. Report HPWL before and after with the same net model.

<!-- algorithm-walkthrough -->

## Slide 3 — Start from HPWL fifty-two

![Start from HPWL fifty-two](assets/steps/01-starter.png)

Force-directed place pulls free cells toward the average of their net neighbors, plus a weak center pull. Begin on the spread starter at HPWL fifty-two.

## Slide 4 — Neighbors pull cells inward

![Neighbors pull cells inward](assets/steps/02-mid-iters.png)

After a couple of lite iterations, A–D drift toward the center while E and F follow their neighbors. Wirelength is already dropping.

## Slide 5 — After force: about eighteen point seven

![After force: about eighteen point seven](assets/steps/03-after-force.png)

Default five iterations land near eighteen point seven—clearly better than fifty-two, still above the compact golden fourteen.

## Slide 6 — Force vs golden compact

![Force vs golden compact](assets/steps/04-vs-golden.png)

Golden fourteen is tighter still. Force is a cheap continuous move—good teaching progress without claiming the absolute minimum.

## Slide 7 — Alpha trades speed vs collapse

![Alpha trades speed vs collapse](assets/steps/05-takeaway.png)

Too much alpha stacks cells; too little barely moves. Lock the iteration count and alpha so your eighteen point seven golden stays stable.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **force-directed-place** lab from the tools shelf. Load the starter placement, run the algorithm once, and read HPWL—and density when the panel shows it. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module’s examples and the course `common/` solvers. Parse `tiny_place.json`, run the algorithm with a deterministic seed, and print coordinates plus HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads A and D; mixing bbox and clique models in one report; keeping only the final SA iterate instead of the best; and forgetting that timing weights change the objective, not just the label.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
