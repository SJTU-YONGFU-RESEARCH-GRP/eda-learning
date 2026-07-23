# Kernighan–Lin bipartition

**Module id:** module02-01-kl-partition
**Lab:** kl-partition
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Kernighan–Lin bipartition

Kernighan–Lin improves an existing bipartition by swapping pairs across the cut. You’ll watch a full pass—gains, locking, a swap sequence, and rollback to the best prefix. On the starter seed that cuts both heavy edges, KL drives the cut from twelve down to three.

## Slide 2 — The idea

Score each unlocked pair by swap gain, lock pairs as you go, then keep only the prefix with best cumulative gain. Here the winning prefix is one swap: A with D, gain nine. Pass one then finds nothing and KL stops at a local optimum for swap moves.

<!-- algorithm-walkthrough -->

## Slide 3 — Bad seed: cutsize 12

![Bad seed: cutsize 12](assets/steps/01-bad-seed.png)

Start from a terrible bipartition AE|BCD. Both heavy edges A–B and D–E are cut, so cutsize is 12. KL will search improving swaps.

## Slide 4 — Score pairwise swaps by gain

![Score pairwise swaps by gain](assets/steps/02-gain-idea.png)

KL considers swapping one vertex from each side. Gain estimates how much the cut shrinks. The best unlocked pair here is A↔D with gain 9.

## Slide 5 — Accept prefix: only A↔D

![Accept prefix: only A↔D](assets/steps/03-accept-swap.png)

Pass 0 builds a sequence of candidate swaps, then keeps the prefix with best cumulative gain. Here best_k=1: perform A↔D once.

## Slide 6 — Refined partition ABC|DE

![Refined partition ABC|DE](assets/steps/04-final.png)

After the swap, A joins B,C and D joins E. Heavy edges are internal; only the weak C–D/C–E bridge remains cut.

## Slide 7 — Next pass finds nothing

![Next pass finds nothing](assets/steps/05-pass1-stop.png)

Pass 1 reports improved=false. KL stops when a full pass cannot improve — local optimum for swap moves from this seed.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **kl-partition** lab from the tools shelf. Load the starter graph, run the algorithm once, and read cutsize and balance in the metrics panel. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module’s examples and the course `common/` solvers. Parse the tiny graph, run the algorithm with a deterministic seed, and print the assignment plus cutsize and balance. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; flipping locked terminals; and stopping before rollback to the best KL or FM prefix. For multilevel flows, verify coarsening before you blame the refiner.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
