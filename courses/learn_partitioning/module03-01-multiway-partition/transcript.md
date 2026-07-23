# Multiway partitioning

**Module id:** module03-01-multiway-partition
**Lab:** multiway-partition
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Multiway partitioning

Direct multiway partitioning assigns nodes to k parts without forcing a binary tree of cuts. Compare it to recursive bisection on the same graph and the same k. Round-robin or seed-based k-way starts are legal but often need refinement.

## Slide 2 — The idea

Multiway objectives count every edge that leaves its part. Balance becomes a k-way size vector. Teaching point: recursive and direct multiway can disagree on cut even when both look balanced.


## Slide 3 — Pseudocode

Multiway compares two constructors in pseudocode: recursive bisection to k, versus a naive round-robin labeling. Both must report the same cutsize metric.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Recursive k equals three lands A B, C, and D E with cut eight. Alphabetical round-robin shreds heavy edges and scores about eighteen.

```text
INPUT: G, k
OUTPUT: k-way assignment + cutsize
method A: recursive_bisection(G,k)
method B: round-robin / block assign labels
cut ← Σ w where side[u]≠side[v]
GOLDEN k=3 recursive: AB|C|DE cut=8
round-robin alphabetic: cut≈18 (worse)
```


<!-- algorithm-walkthrough -->

## Slide 5 — k-way vs naive assignment

![k-way vs naive assignment](assets/steps/01-problem.png)

Real placers need k>2 parts. Recursive bisection respects graph structure; naive round-robin assigns nodes by index mod k — often catastrophic cut.

## Slide 6 — Recursive: AB|C|DE cut 8

![Recursive: AB|C|DE cut 8](assets/steps/02-recursive.png)

Recursive bisection to k=3 first splits ABC|DE (cut 3), then bisects ABC → AB|C|DE. A–B and D–E stay uncut; total cutsize is 8.

## Slide 7 — Round-robin: AD|BE|C cut 18

![Round-robin: AD|BE|C cut 18](assets/steps/03-roundrobin.png)

Alphabetical round-robin puts A,D on part 0; B,E on part 1; C alone on part 2. Almost every edge crosses — cutsize 18.

## Slide 8 — Structure beats indexing

![Structure beats indexing](assets/steps/04-compare.png)

Round-robin cuts A–B(5) and D–E(5) — the two strongest edges. Recursive keeps them internal and pays only bridge cuts through C.

## Slide 9 — Multiway literacy

![Multiway literacy](assets/steps/05-takeaway.png)

Direct k-way FM exists in production tools, but recursive bisection is the teaching baseline: global structure emerges from local 2-way splits.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **multiway-partition** lab from the tools shelf. Load the starter graph, run the algorithm once, and read cutsize and balance in the metrics panel. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse the tiny graph, run the algorithm with a deterministic seed, and print the assignment plus cutsize and balance. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; flipping locked terminals; and stopping before rollback to the best KL or FM prefix. For multilevel flows, verify coarsening before you blame the refiner.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
