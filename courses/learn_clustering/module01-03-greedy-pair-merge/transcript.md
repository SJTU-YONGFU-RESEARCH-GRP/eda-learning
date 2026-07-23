# Greedy pair merge

**Module id:** module01-03-greedy-pair-merge
**Lab:** greedy-pair-merge
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Greedy pair merge

Greedy pair merge is the simplest coarsening engine that still feels like CAD: repeatedly merge the most attractive pair, update the graph, and stop when you hit a cluster count. You’ll watch the full loop on the tiny graph—affinity, contraction, and cutsize moving together.

<!-- algorithm-walkthrough -->

## Slide 2 — Every node starts alone

![Every node starts alone](assets/steps/01-singletons.png)

Agglomerative clustering begins with five singletons. We repeatedly merge the highest-affinity legal pair until we hit target K—here, two clusters, with no capacity limit in the reference run.

## Slide 3 — Merge 1: contract A–B

![Merge 1: contract A–B](assets/steps/02-merge-ab.png)

Heaviest edge is A–B at weight five, so they merge first into a supernode. That protects the strongest connection immediately.

## Slide 4 — Merge 2: absorb C into AB

![Merge 2: absorb C into AB](assets/steps/03-absorb-c.png)

After contraction, C connects to A–B with combined weight five. That ties D–E; alphabetical order merges C next, forming A–B–C.

## Slide 5 — Merge 3: contract D–E

![Merge 3: contract D–E](assets/steps/04-merge-de.png)

Last merge joins D–E at weight five. We now have exactly two clusters: A–B–C versus D–E.

## Slide 6 — Result: cutsize 3

![Result: cutsize 3](assets/steps/05-final-cut.png)

Cut edges are C–D and C–E—total three. Greedy locked in the natural communities without backtracking. Capacity two would have blocked the size-three cluster.

<!-- /algorithm-walkthrough -->

## Slide 7 — Browser lab track

In the browser lab, load the starter, try the K and capacity presets, and run greedy merge. Work the challenges: unconstrained K equals two, then capacity two, then stop at K equals three.

## Slide 8 — Implement track

Run the reference greedy merge down to two clusters. You should land on A–B–C versus D–E with cutsize three. Re-implement contraction yourself and keep a deterministic tie-break so golden tests stay stable.

```bash
# pwd — print working directory
pwd

# ls examples — confirm tiny_graph.json is present
ls examples

# greedy merge to K=2 via reference solver
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --k 2
```

## Slide 9 — Pitfalls to watch

Greedy is myopic—a great first merge can strand you with a bad global cut. Watch illegal merges that violate a size cap. And updating affinities incorrectly after contraction creates silent wrong clusters until you check cutsize by hand.

## Slide 10 — Your turn

Implement greedy pair merge end to end, hit a chosen K, and record cutsize. Complete the checklist and quiz, then continue to size-constrained agglomerative clustering—where capacity becomes a hard rule.
