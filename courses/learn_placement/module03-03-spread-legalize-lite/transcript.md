# Spreading / overlap relief

**Module id:** module03-03-spread-legalize-lite
**Lab:** spread-legalize-lite
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Spreading / overlap relief

Spreading pushes overlapping or near pairs apart until a minimum pairwise distance holds. Start from the triple-overlap demo at one point, run the lite spreader, and confirm every pair clears the threshold without sending HPWL to infinity.

## Slide 2 — The idea

While any pair sits closer than minDist, push them along their separation vector. Finish with a deterministic repair pass so the result is stable. Spreading is a legality proxy—not full row-site legalization.


## Slide 3 — Pseudocode

Spread lite pushes close pairs apart until every pairwise distance clears a minimum. It is overlap relief, not site legalization.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Start from the triple-overlap demo, run the spreader with minimum distance zero point five, and confirm pairs clear without exploding HPWL.

```text
INPUT: positions, min_dist
OUTPUT: spread positions
while exists pair with dist < min_dist:
  push the pair apart along their vector
stop when all pairs clear min_dist
NOTE: not row/site legalization
GOLDEN min_dist=0.5 on overlap seed
```


<!-- algorithm-walkthrough -->

## Slide 5 — Triple overlap at one point

![Triple overlap at one point](assets/steps/01-triple-overlap.png)

The overlap demo stacks A, B, and C on (4,4). Min pairwise distance is zero—illegal for any site-aware flow, perfect for a spreading lesson.

## Slide 6 — Push near pairs apart

![Push near pairs apart](assets/steps/02-push-apart.png)

While any pair sits closer than minDist, push them along their separation vector. Repeated passes peel the triple stack into distinct points.

## Slide 7 — After spread: min distance holds

![After spread: min distance holds](assets/steps/03-after-spread.png)

The lite spreader separates A, B, and C until every pair clears about zero point five. D, E, and F barely move.

## Slide 8 — Spreading is a legality proxy

![Spreading is a legality proxy](assets/steps/04-legality-proxy.png)

Clearing min distance is not row legalization or site snapping. It is a teaching stand-in so overlap stops hiding behind pretty HPWL.

## Slide 9 — Relieve overlap before celebrating WL

![Relieve overlap before celebrating WL](assets/steps/05-takeaway.png)

Start from the triple-overlap seed, spread to minDist zero point five, and confirm every pair clears the threshold. Then revisit wirelength.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **spread-legalize-lite** lab from the tools shelf. Load the starter placement, run the algorithm once, and read HPWL—and density when the panel shows it. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse `tiny_place.json`, run the algorithm with a deterministic seed, and print coordinates plus HPWL. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads A and D; mixing bbox and clique models in one report; keeping only the final SA iterate instead of the best; and forgetting that timing weights change the objective, not just the label.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
