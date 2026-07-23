# Multilevel clustering

**Module id:** module03-01-multilevel-clustering
**Lab:** multilevel-clustering
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Multilevel clustering

Multilevel clustering coarsens, partitions, then refines. You’ll watch greedy coarsening to two clusters followed by FM polish—landing on cutsize three.

<!-- algorithm-walkthrough -->

## Slide 2 — Coarsen with greedy merge

![Coarsen with greedy merge](assets/steps/01-coarsen.png)

Multilevel starts by contracting the graph. Greedy pair merge to coarseK=2 builds a projected bipartition of the original nodes.

## Slide 3 — Project to a bipartition

![Project to a bipartition](assets/steps/02-project.png)

Map the two coarse clusters onto sides 0 and 1. This seed is already near-optimal on TINY_GRAPH — unlike BAD_SEED’s cut of 12.

## Slide 4 — FM-refine on the fine graph

![FM-refine on the fine graph](assets/steps/03-fm-refine.png)

Run Fiduccia–Mattheyses on the projected seed. On this instance refinement keeps ABC vs DE and renames sides to P0/P1.

## Slide 5 — Golden: cutsize 3

![Golden: cutsize 3](assets/steps/04-final.png)

Final communities ABC|DE with P0/P1 labels. Multilevel’s value shows more on larger graphs; here it demonstrates the V-cycle shape.

## Slide 6 — Multilevel mindset

![Multilevel mindset](assets/steps/05-takeaway.png)

Coarsen for global structure, refine for local cut. Real placers nest this inside V-cycles with hyperedges and tighter balance — this lab is the skeleton.

<!-- /algorithm-walkthrough -->

## Slide 7 — Browser lab track

In the browser lab, run multilevel and compare with a plain greedy seed. Clear challenges for the refined ABC|DE result.

## Slide 8 — Implement track

Run multilevel on the tiny graph and confirm cutsize three. Re-implement project-and-refine until the unit test passes.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode multilevel
```

## Slide 9 — Pitfalls to watch

Skipping refinement leaves coarsening artifacts. Projecting labels incorrectly scrambles the fine-level seed. Too aggressive coarsening can erase structure.

## Slide 10 — Your turn

Match the golden, finish the checklist and quiz, then continue to hypergraph clustering.
