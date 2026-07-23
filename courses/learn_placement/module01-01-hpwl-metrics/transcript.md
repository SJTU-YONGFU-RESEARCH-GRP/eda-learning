# Half-perimeter wirelength

**Module id:** module01-01-hpwl-metrics
**Lab:** hpwl-metrics
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Half-perimeter wirelength

Half-perimeter wirelength is the teaching yardstick for placement. For each net, take the bounding box of its pins and add width plus height. On the starter six-cell instance the spread-out seed scores total HPWL fifty-two. The compact golden placement drops that to fourteen. You will compute both numbers every time you look at a placement.

## Slide 2 — The idea

For every net, find min and max x and y among its pins, then add (maxX minus minX) plus (maxY minus minY). Sum over nets for total HPWL. Never celebrate a tiny total that piles every cell on one point—that is not a usable placement, only a collapsed metric.

<!-- algorithm-walkthrough -->

## Slide 3 — Starter placement is spread out

![Starter placement is spread out](assets/steps/01-starter-spread.png)

Six cells A–F sit on a rough eight-by-eight canvas. The spread-out seed pulls nets long: total half-perimeter wirelength is fifty-two. This is the shared starter for every placement lab.

## Slide 4 — One net: bbox width plus height

![One net: bbox width plus height](assets/steps/02-one-net.png)

Net A–B alone has pins at (0,0) and (8,0). Width is eight, height is zero, so HPWL is eight. Every net uses the same bbox rule before you sum.

## Slide 5 — Sum six nets to fifty-two

![Sum six nets to fifty-two](assets/steps/03-sum-nets.png)

Four two-pin nets at eight each, the four-pin ABCD net at sixteen, and E–F at four: eight times four plus sixteen plus four equals fifty-two. That is the starter golden.

## Slide 6 — Golden placement drops to fourteen

![Golden placement drops to fourteen](assets/steps/04-golden-compact.png)

The compact reference tucks A–D into a two-by-two block near the center. Same nets, shorter boxes: total HPWL falls from fifty-two to fourteen.

## Slide 7 — HPWL is the teaching yardstick

![HPWL is the teaching yardstick](assets/steps/05-takeaway.png)

Report total HPWL before and after every move. Fifty-two versus fourteen is the starter story—but a tiny total with stacked cells is not a usable placement.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **hpwl-metrics** lab from the tools shelf. Load the starter placement, run the algorithm once, and read HPWL—and density when the panel shows it. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module’s examples and the course `common/` solvers. Parse `tiny_place.json`, run the algorithm with a deterministic seed, and print coordinates plus HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads A and D; mixing bbox and clique models in one report; keeping only the final SA iterate instead of the best; and forgetting that timing weights change the objective, not just the label.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
