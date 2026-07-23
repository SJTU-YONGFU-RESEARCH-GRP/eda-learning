# Spectral bisection

**Module id:** module02-03-spectral-bisection
**Lab:** spectral-bisection
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Spectral bisection

Spectral bisection uses the graph Laplacian and its Fiedler vector to propose a balanced cut. You’ll watch the order and the chosen split land on cutsize three.

<!-- algorithm-walkthrough -->

## Slide 2 — Build the Laplacian

![Build the Laplacian](assets/steps/01-laplacian.png)

Spectral methods read connectivity from the graph Laplacian L = D − A. The Fiedler vector (second eigenvector) encodes a soft cut.

## Slide 3 — Sort by Fiedler value

![Sort by Fiedler value](assets/steps/02-fiedler-order.png)

After iteration, nodes order low→high as E, D, C, B, A. E is most negative; A is most positive — natural bipartition candidates.

## Slide 4 — Sweep prefixes for best cut

![Sweep prefixes for best cut](assets/steps/03-sweep-cut.png)

Try every balanced prefix of the order as side 0. The winning split is {D,E} vs {A,B,C} with cutsize 3.

## Slide 5 — Result ABC|DE

![Result ABC|DE](assets/steps/04-final.png)

Spectral recovers the same communities as unconstrained greedy and LP. Teaching point: global eigenvectors can find the cut without greedy merges.

## Slide 6 — When spectral helps

![When spectral helps](assets/steps/05-takeaway.png)

Spectral is a strong initializer for bipartition. On larger chips it pairs with multilevel; here the tiny instance is exact enough to grade against goldens.

<!-- /algorithm-walkthrough -->

## Slide 7 — Browser lab track

In the browser lab, run spectral bisection and inspect the Fiedler order. Clear challenges for cutsize three and the ABC versus DE parts.

## Slide 8 — Implement track

Run the spectral mode on the tiny graph. Confirm cutsize three and the natural clusters. Re-implement the sweep yourself; a dense tiny eigensolve is fine at course scale.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode spectral
```

## Slide 9 — Pitfalls to watch

Ignoring balance can isolate one node. Numerical noise can scramble near-ties—use a stable sort. Disconnected graphs need explicit component handling.

## Slide 10 — Your turn

Match cutsize three, finish the checklist and quiz, then continue to Kernighan–Lin.
