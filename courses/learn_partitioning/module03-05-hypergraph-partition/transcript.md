# Hypergraph partitioning

**Module id:** module03-05-hypergraph-partition
**Lab:** hypergraph-partition
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Hypergraph partitioning

Netlists are hypergraphs: one net can touch many cells. A hyperedge is cut if it spans more than one part. On the starter hypergraph the golden ABC versus DE leaves a single cut net—pairwise clique expansion would tell a different story.

## Slide 2 — The idea

Optimize hyperedge cut, not only pairwise edge cut. Multi-pin nets dominate affinity in real designs. Use clique expansion only for drawing or as a heuristic substrate—not as the reported objective unless the lab says so.


## Slide 3 — Pseudocode

Hypergraph cut counts a net once if it spans more than one part. Pseudocode is a span check per hyperedge—not a sum of clique pairs unless you expand deliberately.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

On the starter hypergraph, golden ABC versus DE leaves a single cut net. Expanding to a clique can tell a different numeric story—report which model you used.

```text
INPUT: hyperedges e={pins…}, side[]
OUTPUT: hyperedge_cut
cut ← count edges with |{side[p]:p∈e}| > 1
(optional) expand to pairwise clique for KL/FM
GOLDEN ABC|DE: one cut net on starter H
pairwise clique expansion can differ
```


<!-- algorithm-walkthrough -->

## Slide 5 — Nets are hyperedges

![Nets are hyperedges](assets/steps/01-nets.png)

TINY_HYPERGRAPH has four nets: n1={A,B,C} w=3, n2={D,E}, n3={C,D}, n4={A,B}. Cut counts whole nets spanning ≥2 sides — not pairwise edges alone.

## Slide 6 — Bad seed: hyperedge cut 6

![Bad seed: hyperedge cut 6](assets/steps/02-bad-seed.png)

BAD_SEED AE|BCD cuts nets n1(3), n2(2), and n4(1) — hyperedge cut 6. Same seed as graph labs, worse hyper objective.

## Slide 7 — FM on clique expansion

![FM on clique expansion](assets/steps/03-fm-run.png)

Hypergraph FM clique-expands nets to pair edges, then runs standard FM from the bad seed. Objective reports hyperedge cut on the original nets.

## Slide 8 — Refined ABC|DE: hyper cut 1

![Refined ABC|DE: hyper cut 1](assets/steps/04-refined.png)

FM reaches ABC|DE. Only bridge net n3={C,D} crosses sides — hyperedge cut 1. n1, n2, n4 stay uncut.

## Slide 9 — Why hypergraphs in partition

![Why hypergraphs in partition](assets/steps/05-takeaway.png)

Real netlists are hypergraphs. Modeling nets honestly changes the cut objective — clique expansion is for moves, hyper cut is for scoring.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **hypergraph-partition** lab from the tools shelf. Load the starter graph, run the algorithm once, and read cutsize and balance in the metrics panel. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse the tiny graph, run the algorithm with a deterministic seed, and print the assignment plus cutsize and balance. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; flipping locked terminals; and stopping before rollback to the best KL or FM prefix. For multilevel flows, verify coarsening before you blame the refiner.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
