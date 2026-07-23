# Multilevel partitioning

**Module id:** module04-01-multilevel-partition
**Lab:** multilevel-partition
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Multilevel partitioning

A multilevel V-cycle coarsens the graph, partitions the tiny problem, projects the assignment back, and refines at each finer level. You will walk coarsen, initial partition, project, and refine on the same starter instance.

## Slide 2 — The idea

Coarsening shrinks the search space. The coarse partition is cheap. Projection gives a feasible fine assignment that FM or KL can polish. A bug in coarsening poisons every finer level—debug the hierarchy before tuning refine passes.

<!-- algorithm-walkthrough -->

## Slide 3 — Coarsen with greedy merge

![Coarsen with greedy merge](assets/steps/01-coarsen.png)

Multilevel V-cycle contracts the graph via greedy pair merge to coarseK=2. Supernodes C1={A,B,C} and C2={D,E} capture community structure.

## Slide 4 — Project to fine bipartition

![Project to fine bipartition](assets/steps/02-project.png)

Map coarse clusters to sides 0/1: ABC→0, DE→1. Projected seed ABC|DE already has cutsize 3 — unlike BAD_SEED's cut of 12.

## Slide 5 — FM refine on fine graph

![FM refine on fine graph](assets/steps/03-refine.png)

FM polishes the projected seed. On TINY_GRAPH the projection is already optimal — refine keeps ABC|DE at cutsize 3.

## Slide 6 — Final P0/P1 labels

![Final P0/P1 labels](assets/steps/04-final.png)

Output renames sides to P0/P1 for placers. Final communities ABC|DE with cutsize 3 — multilevel beats refining a random bad seed alone.

## Slide 7 — Multilevel V-cycle mindset

![Multilevel V-cycle mindset](assets/steps/05-takeaway.png)

Coarsen for global structure, project, refine locally. Real placers nest this in repeated V-cycles with hyperedges and balance — this lab is the skeleton.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **multilevel-partition** lab from the tools shelf. Load the starter graph, run the algorithm once, and read cutsize and balance in the metrics panel. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module’s examples and the course `common/` solvers. Parse the tiny graph, run the algorithm with a deterministic seed, and print the assignment plus cutsize and balance. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; flipping locked terminals; and stopping before rollback to the best KL or FM prefix. For multilevel flows, verify coarsening before you blame the refiner.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
