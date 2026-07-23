# Label propagation clustering

**Module id:** module02-01-label-propagation
**Lab:** label-propagation
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Label propagation clustering

Label propagation grows communities by letting each node adopt the strongest neighbor label. You’ll watch the asynchronous update on the tiny graph, then measure iterations-to-stable and cutsize.

<!-- algorithm-walkthrough -->

## Slide 2 — Initialize: each node is its own label

![Initialize: each node is its own label](assets/steps/01-init.png)

Start with five communities—each node labeled as itself. Every node will vote using weighted neighbor labels; async updates walk nodes in order A through E.

## Slide 3 — Each node adopts the winning neighbor label

![Each node adopts the winning neighbor label](assets/steps/02-vote-idea.png)

For a node, sum edge weights by neighbor label and take the best. Dense A–B–C and D–E pull neighbors onto shared labels quickly. Ties break lexicographically.

## Slide 4 — After iteration 1: already clustered

![After iteration 1: already clustered](assets/steps/03-after-iter1.png)

One async sweep flips A and C onto B, and D onto E. Communities A–B–C and D–E appear immediately on this tiny graph.

## Slide 5 — Iteration 2: no changes — stop

![Iteration 2: no changes — stop](assets/steps/04-iter2-stable.png)

A second sweep finds zero flips, so the algorithm reports two iterations to stable. Stability—not a cutsize objective—is the stopping rule. Cutsize lands at three.

## Slide 6 — When LP helps in EDA flows

![When LP helps in EDA flows](assets/steps/05-takeaway.png)

LP is a cheap community detector—great as a seed or coarsening hint. It does not enforce balance or timing; refinement still matters on hard instances.

<!-- /algorithm-walkthrough -->

## Slide 7 — Browser lab track

In the browser lab, show the initial labels, then run label propagation. Clear the challenges for two iterations, two communities, and the full golden label map.

## Slide 8 — Implement track

Load the tiny graph and run the reference label-propagation mode. Confirm two iterations, labels grouping A–B–C versus D–E, and cutsize three. Re-implement the vote and tie-break until the unit test passes.

```bash
# run async label propagation on the tiny graph
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode lp
```

## Slide 9 — Pitfalls to watch

Order dependence is real—document your sweep order. Without a tie-break, goldens flake. And stopping only on max iterations without checking that nothing changed hides non-convergence.

## Slide 10 — Your turn

Match the golden table, finish the checklist and quiz, then continue to spectral bisection.
