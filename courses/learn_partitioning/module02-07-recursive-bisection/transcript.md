# Recursive bisection

**Module id:** module02-07-recursive-bisection
**Lab:** recursive-bisection
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Recursive bisection

Recursive bisection builds a multiway partition by repeatedly bipartitioning the largest part until you reach k parts. Start from a bipartition, then cut again. On the tiny graph aiming for four parts you will see how early cuts constrain later ones.

## Slide 2 — The idea

Each step is an ordinary bipartition on an induced subgraph. Quality compounds: a weak first cut leaves later bisectors fewer good options. Always report total cut across all part boundaries and the part-size vector.


## Slide 3 — Pseudocode

Recursive bisection is a loop over parts: while you have fewer than k parts, split the largest with a bipartitioner and replace it by the two halves.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

First split yields ABC versus DE at cut three. For k equals three the sketch bisects ABC next into A B versus C with D E untouched.

```text
INPUT: G, target k parts
OUTPUT: side[v] ∈ {0..k−1}
parts ← {all nodes}
while |parts| < k:
  pick largest part P
  bipartition P (spectral/KL/FM)
  replace P with the two halves
GOLDEN k=2: ABC|DE cut=3
k=3 continues on ABC → AB|C|DE
```


<!-- algorithm-walkthrough -->

## Slide 5 — Start: one part, k=4 target

![Start: one part, k=4 target](assets/steps/01-start.png)

Recursive bisection builds k-way partitions by repeated 2-way splits. Target k=4 on TINY_GRAPH: bisect the largest part until four labels exist.

## Slide 6 — Bisect 1: ABC|DE cut 3

![Bisect 1: ABC|DE cut 3](assets/steps/02-split-1.png)

First spectral split on the whole graph yields ABC|DE — same golden bipartition with cutsize 3. Two parts remain; need two more splits.

## Slide 7 — Bisect 2: split ABC → AB|C

![Bisect 2: split ABC → AB|C](assets/steps/03-split-2.png)

Largest part ABC (size 3) is bisected next. A and B stay together (w=5); C becomes its own part. Three parts: AB, C, DE.

## Slide 8 — Bisect 3: split DE → D|E

![Bisect 3: split DE → D|E](assets/steps/04-split-3.png)

Largest remaining part DE is bisected, cutting the weight-5 D–E edge. Final four parts: AB, C, D, E singleton aside from AB pair.

## Slide 9 — Recursive bisection tradeoff

![Recursive bisection tradeoff](assets/steps/05-takeaway.png)

k=4 costs cut 13 because splitting DE destroys the weight-5 edge. k=3 stops earlier at AB|C|DE cut 8 — fewer splits can mean lower total cut.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **recursive-bisection** lab from the tools shelf. Load the starter graph, run the algorithm once, and read cutsize and balance in the metrics panel. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse the tiny graph, run the algorithm with a deterministic seed, and print the assignment plus cutsize and balance. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; flipping locked terminals; and stopping before rollback to the best KL or FM prefix. For multilevel flows, verify coarsening before you blame the refiner.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
