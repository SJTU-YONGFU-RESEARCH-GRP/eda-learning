# Simulated annealing floorplan search

**Module id:** module03-01-simulated-annealing-fp
**Lab:** simulated-annealing-fp
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Simulated annealing floorplan search

Toy cost adds one thousand when a packing is illegal. The bad overflow seed sits near one thousand forty-four; the golden legal packing scores about thirty-six. Annealing should move toward legal, lower cost.


## Slide 2 — Pseudocode

Floorplan annealing uses a cost that heavily penalizes illegality. Pseudocode proposes neighbors, accepts by Metropolis, and keeps the best legal iterate.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 3 — Algorithm sketch

Bad overflow seed costs about one thousand forty-four. Golden legal packing is about thirty-six. One teaching improve step replaces bad with golden.

```text
INPUT: pack / representation, T schedule
OUTPUT: best legal low-cost pack
cost ← 1000·¬legal + deadspace + α·HPWL
propose neighbor (swap/move/perturb)
accept if Δ<0 or rand < e^(−Δ/T)
keep best; cool T
GOLDEN legal cost≈36; bad≈1044
```


<!-- algorithm-walkthrough -->

## Slide 4 — Illegal packs pay 1000

![Illegal packs pay 1000](assets/steps/01-bad-cost.png)

Our toy cost adds one thousand when the packing is illegal. The bad overflow seed therefore sits at cost about one thousand forty-four—dominated by the penalty.

## Slide 5 — Golden cost stays under 1000

![Golden cost stays under 1000](assets/steps/02-golden-cost.png)

The golden legal packing drops below the penalty floor. Cost is about thirty-six—deadspace and a small HPWL proxy, no illegality tax.

## Slide 6 — Neighbors swap module positions

![Neighbors swap module positions](assets/steps/03-neighbor.png)

A simple SA move swaps the lower-left corners of two modules while keeping sizes. Accept improving moves; accept worsening ones with temperature probability.

## Slide 7 — Improve: bad → golden

![Improve: bad → golden](assets/steps/04-improve.png)

One teaching “improve” step replaces the illegal seed with the golden packing. Cost falls below one thousand and legality flips to true—exactly what a cooling schedule should prefer.

## Slide 8 — SA needs a representation

![SA needs a representation](assets/steps/05-takeaway.png)

Annealing is only as good as the move set. Pair it with polish, B-star, or sequence-pair edits—plus soft sizing and macros—in the labs that follow.

<!-- /algorithm-walkthrough -->


## Slide 9 — Browser lab track

Open simulated-annealing-fp. Show bad, note cost at least one thousand. Show golden or Improve—cost drops below one thousand and legality becomes true.

## Slide 10 — Implement track

Implement cost with an illegality penalty, plus deadspace and HPWL terms. Assert cost(golden) is less than cost(bad), and saSwap only exchanges coordinates.

## Slide 11 — Pitfalls

Accepting illegal states without penalty; forgetting to rescore after a swap; cooling so fast you never escape the bad seed.

## Slide 12 — Your turn

Demonstrate one improve step from bad to golden. Next: soft module A reshaped from three by two to two by three.
