# Simulated annealing floorplan search

**Module id:** module03-01-simulated-annealing-fp
**Lab:** simulated-annealing-fp
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Simulated annealing floorplan search

Toy cost adds one thousand when a packing is illegal. The bad overflow seed sits near one thousand forty-four; the golden legal packing scores about thirty-six. Annealing should move toward legal, lower cost.

<!-- algorithm-walkthrough -->

## Slide 2 — Illegal packs pay 1000

![Illegal packs pay 1000](assets/steps/01-bad-cost.png)

Our toy cost adds one thousand when the packing is illegal. The bad overflow seed therefore sits at cost about one thousand forty-four—dominated by the penalty.

## Slide 3 — Golden cost stays under 1000

![Golden cost stays under 1000](assets/steps/02-golden-cost.png)

The golden legal packing drops below the penalty floor. Cost is about thirty-six—deadspace and a small HPWL proxy, no illegality tax.

## Slide 4 — Neighbors swap module positions

![Neighbors swap module positions](assets/steps/03-neighbor.png)

A simple SA move swaps the lower-left corners of two modules while keeping sizes. Accept improving moves; accept worsening ones with temperature probability.

## Slide 5 — Improve: bad → golden

![Improve: bad → golden](assets/steps/04-improve.png)

One teaching “improve” step replaces the illegal seed with the golden packing. Cost falls below one thousand and legality flips to true—exactly what a cooling schedule should prefer.

## Slide 6 — SA needs a representation

![SA needs a representation](assets/steps/05-takeaway.png)

Annealing is only as good as the move set. Pair it with polish, B-star, or sequence-pair edits—plus soft sizing and macros—in the labs that follow.

<!-- /algorithm-walkthrough -->


## Slide 7 — Browser lab track

Open simulated-annealing-fp. Show bad, note cost at least one thousand. Show golden or Improve—cost drops below one thousand and legality becomes true.

## Slide 8 — Implement track

Implement cost with an illegality penalty, plus deadspace and HPWL terms. Assert cost(golden) is less than cost(bad), and saSwap only exchanges coordinates.

## Slide 9 — Pitfalls

Accepting illegal states without penalty; forgetting to rescore after a swap; cooling so fast you never escape the bad seed.

## Slide 10 — Your turn

Demonstrate one improve step from bad to golden. Next: soft module A reshaped from three by two to two by three.
