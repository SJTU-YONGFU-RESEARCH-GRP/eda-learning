# Half-perimeter wirelength

**Module id:** module01-01-hpwl-metrics
**Lab:** hpwl-metrics
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Half-perimeter wirelength

Half-perimeter wirelength is the teaching yardstick for placement. For each net, take the bounding box of its pins and add width plus height. On the starter six-cell instance the spread-out seed scores total HPWL fifty-two. The compact golden placement drops that to fourteen. You will compute both numbers every time you look at a placement.

## Slide 2 — The idea

For every net, find min and max x and y among its pins, then add (maxX minus minX) plus (maxY minus minY). Sum over nets for total HPWL. Never celebrate a tiny total that piles every cell on one point—that is not a usable placement, only a collapsed metric.


## Slide 3 — Pseudocode

HPWL is one loop over nets: bounding-box width plus height, then sum. That sum is the teaching yardstick for every later placer.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Starter placement scores fifty-two. Compact golden scores fourteen. Never celebrate a tiny total that piles every cell on one point.

```text
INPUT: positions, nets
OUTPUT: total HPWL
for each net: bbox → (maxx−minx)+(maxy−miny)
total ← Σ net HPWL
GOLDEN starter=52; compact=14
NOTE: collapsed point ≠ usable place
```


<!-- algorithm-walkthrough -->

## Slide 5 — Starter placement is spread out

![Starter placement is spread out](assets/steps/01-starter-spread.png)

Six cells A–F sit on a rough eight-by-eight canvas. The spread-out seed pulls nets long: total half-perimeter wirelength is fifty-two. This is the shared starter for every placement lab.

## Slide 6 — One net: bbox width plus height

![One net: bbox width plus height](assets/steps/02-one-net.png)

Net A–B alone has pins at (0,0) and (8,0). Width is eight, height is zero, so HPWL is eight. Every net uses the same bbox rule before you sum.

## Slide 7 — Sum six nets to fifty-two

![Sum six nets to fifty-two](assets/steps/03-sum-nets.png)

Four two-pin nets at eight each, the four-pin ABCD net at sixteen, and E–F at four: eight times four plus sixteen plus four equals fifty-two. That is the starter golden.

## Slide 8 — Golden placement drops to fourteen

![Golden placement drops to fourteen](assets/steps/04-golden-compact.png)

The compact reference tucks A–D into a two-by-two block near the center. Same nets, shorter boxes: total HPWL falls from fifty-two to fourteen.

## Slide 9 — HPWL is the teaching yardstick

![HPWL is the teaching yardstick](assets/steps/05-takeaway.png)

Report total HPWL before and after every move. Fifty-two versus fourteen is the starter story—but a tiny total with stacked cells is not a usable placement.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **hpwl-metrics** lab from the tools shelf. Load the starter placement, run the algorithm once, and read HPWL—and density when the panel shows it. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse `tiny_place.json`, run the algorithm with a deterministic seed, and print coordinates plus HPWL. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads A and D; mixing bbox and clique models in one report; keeping only the final SA iterate instead of the best; and forgetting that timing weights change the objective, not just the label.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
