# Spectral bipartition

**Module id:** module02-05-spectral-partition
**Lab:** spectral-partition
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Spectral bipartition

Spectral bipartition reads connectivity from the graph Laplacian. The Fiedler vector gives a soft ordering of nodes; a balanced sweep of that order picks the cut. On the starter graph the winning split is DE versus ABC with cutsize three.

## Slide 2 — The idea

Build L equals D minus A, take the second eigenvector, sort nodes, and try balanced prefixes. Reject lopsided splits. The continuous membership becomes a hard bipartition only after the sweep chooses the best legal cut.


## Slide 3 — Pseudocode

Spectral bipartition reads the Fiedler vector of the Laplacian, sorts nodes, then sweeps balanced prefixes for the cheapest cut.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

On the starter graph the winning split is D E versus A B C with cutsize three—the same golden communities KL and FM refine toward.

```text
INPUT: weighted undirected G
OUTPUT: side[] bipartition
L ← Laplacian; take Fiedler eigenvector
order ← nodes sorted by Fiedler value
sweep balanced prefixes; pick min cutsize
GOLDEN: DE|ABC (or ABC|DE) cut=3
```


<!-- algorithm-walkthrough -->

## Slide 5 — Build the Laplacian

![Build the Laplacian](assets/steps/01-laplacian.png)

Spectral methods read connectivity from the graph Laplacian L = D − A. The Fiedler vector (second eigenvector) encodes a soft cut.

## Slide 6 — Sort by Fiedler value

![Sort by Fiedler value](assets/steps/02-fiedler-order.png)

After iteration, nodes order low→high as E, D, C, B, A. E is most negative; A is most positive — natural bipartition candidates.

## Slide 7 — Sweep prefixes for best cut

![Sweep prefixes for best cut](assets/steps/03-sweep-cut.png)

Try every balanced prefix of the order as side 0. The winning split is {D,E} vs {A,B,C} with cutsize 3.

## Slide 8 — Result ABC|DE

![Result ABC|DE](assets/steps/04-final.png)

Spectral recovers the same communities as unconstrained greedy and grow-from-D. Global eigenvectors find the cut without greedy merges.

## Slide 9 — When spectral helps

![When spectral helps](assets/steps/05-takeaway.png)

Spectral is a strong initializer for bipartition. On larger chips it pairs with multilevel; here the tiny instance grades against golden cut 3.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **spectral-partition** lab from the tools shelf. Load the starter graph, run the algorithm once, and read cutsize and balance in the metrics panel. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse the tiny graph, run the algorithm with a deterministic seed, and print the assignment plus cutsize and balance. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; flipping locked terminals; and stopping before rollback to the best KL or FM prefix. For multilevel flows, verify coarsening before you blame the refiner.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
