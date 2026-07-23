# Fiduccia–Mattheyses bipartition

**Module id:** module02-03-fm-partition
**Lab:** fm-partition
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Fiduccia–Mattheyses bipartition

Fiduccia–Mattheyses moves one vertex at a time instead of swapping a pair. From the same cutsize-twelve seed, FM flips D then A, keeps the best prefix of two moves, and lands on the same ABC versus DE cut of three that KL found.

## Slide 2 — The idea

Bucketed single-vertex gains, lock after each move, and enforce a balance tolerance so parts cannot empty. Two legal flips can equal one KL swap’s total gain on this instance—different move set, same destination quality.

<!-- algorithm-walkthrough -->

## Slide 3 — Same bad seed, different move set

![Same bad seed, different move set](assets/steps/01-bad-seed.png)

FM starts from the same cutsize-12 seed, but moves one vertex at a time instead of swapping a pair. That suits hypergraph / cell-move implementations.

## Slide 4 — Move 1: flip D (gain 3)

![Move 1: flip D (gain 3)](assets/steps/02-move-d.png)

Highest legal move sends D to the other side with gain 3. Partial progress: D joins E's side early.

## Slide 5 — Move 2: flip A (gain 6)

![Move 2: flip A (gain 6)](assets/steps/03-move-a.png)

Next, A flips with gain 6. Cumulative gain is 3+6=9 — the same total improvement KL found with one swap.

## Slide 6 — Final ABC|DE, cutsize 3

![Final ABC|DE, cutsize 3](assets/steps/04-final.png)

FM lands on the same refined bipartition as KL. Teaching point: move style differs, destination quality matches on this instance.

## Slide 7 — Pass 1 confirms local optimum

![Pass 1 confirms local optimum](assets/steps/05-pass1-stop.png)

A second FM pass finds no improving move prefix. Stop. In real tools, FM often runs inside multilevel V-cycles with tighter balance and hyperedges.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **fm-partition** lab from the tools shelf. Load the starter graph, run the algorithm once, and read cutsize and balance in the metrics panel. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module’s examples and the course `common/` solvers. Parse the tiny graph, run the algorithm with a deterministic seed, and print the assignment plus cutsize and balance. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; flipping locked terminals; and stopping before rollback to the best KL or FM prefix. For multilevel flows, verify coarsening before you blame the refiner.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
