# Sequence-pair representation

**Module id:** module02-05-sequence-pair
**Lab:** sequence-pair
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Sequence-pair representation

Sequence pair uses positive permutation A B C E D and negative D A B C E. Longest-path packing from left-of and below constraints places all five modules legally.


## Slide 2 — Pseudocode

Sequence-pair pseudocode turns two permutations into horizontal and vertical constraints, then longest-path packs x and y.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 3 — Algorithm sketch

Golden pos is A B C E D and neg is D A B C E. Evaluation must place all five modules legally with non-negative coordinates.

```text
INPUT: pos[], neg[] permutations of modules
OUTPUT: (x,y) via constraint longest paths
pos/neg order ⇒ horizontal & vertical constraints
x ← longest path in H-graph; y ← V-graph
GOLDEN pos=A B C E D; neg=D A B C E
packs legally with non-negative coords
```


<!-- algorithm-walkthrough -->

## Slide 4 — Two permutations encode geometry

![Two permutations encode geometry](assets/steps/01-seqs.png)

Sequence pair uses a positive and a negative permutation of the same modules. Ours are pos A B C E D and neg D A B C E—five ids each, same set.

## Slide 5 — Horizontal constraints set x

![Horizontal constraints set x](assets/steps/02-h-rules.png)

Module i is left of j when i appears before j in both sequences. Longest-path packing pushes each block as far left as those constraints allow.

## Slide 6 — Vertical constraints set y

![Vertical constraints set y](assets/steps/03-v-rules.png)

Module i is below j when i precedes j in pos but follows in neg. That fills y coordinates without overlaps for a feasible pair.

## Slide 7 — Golden SP packs legally

![Golden SP packs legally](assets/steps/04-legal.png)

Evaluating the golden sequences places all five modules with non-negative coordinates and a legal packing inside the outline.

## Slide 8 — SP neighbors are permutation moves

![SP neighbors are permutation moves](assets/steps/05-takeaway.png)

Annealing on sequence pair swaps or rotates entries in pos and neg. Feasibility stays geometric; cost can be deadspace plus wirelength.

<!-- /algorithm-walkthrough -->


## Slide 9 — Browser lab track

Open sequence-pair and Pack sequence pair. Confirm five modules, non-negative coordinates, and legality true on the golden permutations.

## Slide 10 — Implement track

Implement longest-path SP packing. Assert pos and neg are the same five ids, and the golden pair packs legally.

## Slide 11 — Pitfalls

Mismatched id sets between pos and neg; swapping the horizontal/vertical rules; negative coordinates from a buggy DP.

## Slide 12 — Your turn

Pack the golden sequences legally. Next: simulated annealing that prefers legal low-cost neighbors.
