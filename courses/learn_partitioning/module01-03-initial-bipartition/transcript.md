# Initial bipartition

**Module id:** module01-03-initial-bipartition
**Lab:** initial-bipartition
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Initial bipartition

Refinement needs a legal starting cut. In this module you build an initial bipartition—random with a fixed seed, greedy by heaviest edges, or grow from a seed node—before KL or FM ever runs. On the tiny graph, seed seven’s random bipartition matches the familiar bad seed shape AE versus BCD with cutsize twelve.

## Slide 2 — The idea

Random shuffles then splits by half. Greedy prefers keeping heavy edges internal when it can. Grow expands a frontier from a seed until the part hits its size budget. All three must report cutsize and balance so you can compare seeds fairly.


## Slide 3 — Pseudocode

Initial bipartition is three named constructors in pseudocode: random split, greedy heavy-edge keep, and grow from a seed until the size budget.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Grow from D yields DE versus ABC at cut three. Random seed seven recovers the bad AE versus BCD cut of twelve. Always print cutsize and balance before KL or FM.

```text
INPUT: graph G, method ∈ {random,greedy,grow}
OUTPUT: legal side[v] ∈ {0,1}
random(seed): shuffle; split by half
greedy: keep heaviest edges internal when able
grow(seed): expand frontier until size budget
report cutsize + balance for every seed
GOLDEN: grow(D)→DE|ABC cut=3
random(7)→AE|BCD cut=12
```


<!-- algorithm-walkthrough -->

## Slide 5 — Need a legal starting split

![Need a legal starting split](assets/steps/01-empty.png)

Refinement (KL/FM) needs a bipartition seed. Common builders: random, greedy heaviest-edge, or grow-from-node BFS. All must end with exactly two sides.

## Slide 6 — Random seed=1: lucky ABC|DE

![Random seed=1: lucky ABC|DE](assets/steps/02-random-lucky.png)

Random (seed=1) lands on ABC|DE with cutsize 3 — the golden communities by luck. Random seeds can also be terrible (seed=4 → cut 13).

## Slide 7 — Greedy initial: AB|CDE cut 5

![Greedy initial: AB|CDE cut 5](assets/steps/03-greedy.png)

Greedy anchors heaviest edge A–B on side 0, then places remaining nodes to minimize added cut. Result AB|CDE has cutsize 5 — legal but worse than grow.

## Slide 8 — Grow from D: ABC|DE cut 3

![Grow from D: ABC|DE cut 3](assets/steps/04-grow-d.png)

Grow from D pulls E first (w=5), then A and B via heavy edges. Side 0 = {D,E}, side 1 = {A,B,C} — cutsize 3, matching golden.

## Slide 9 — Seed quality sets the ceiling

![Seed quality sets the ceiling](assets/steps/05-takeaway.png)

All three methods produce legal bipartitions, but cutsize ranges 3–13 on the same graph. Better seeds mean less work for KL/FM downstream.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **initial-bipartition** lab from the tools shelf. Load the starter graph, run the algorithm once, and read cutsize and balance in the metrics panel. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse the tiny graph, run the algorithm with a deterministic seed, and print the assignment plus cutsize and balance. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; flipping locked terminals; and stopping before rollback to the best KL or FM prefix. For multilevel flows, verify coarsening before you blame the refiner.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
