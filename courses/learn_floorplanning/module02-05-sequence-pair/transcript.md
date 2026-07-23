# Sequence-pair representation

**Module id:** module02-05-sequence-pair
**Lab:** sequence-pair
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Sequence-pair representation

Sequence pair uses positive permutation A B C E D and negative D A B C E. Longest-path packing from left-of and below constraints places all five modules legally.

<!-- algorithm-walkthrough -->

## Slide 2 — Two permutations encode geometry

![Two permutations encode geometry](assets/steps/01-seqs.png)

Sequence pair uses a positive and a negative permutation of the same modules. Ours are pos A B C E D and neg D A B C E—five ids each, same set.

## Slide 3 — Horizontal constraints set x

![Horizontal constraints set x](assets/steps/02-h-rules.png)

Module i is left of j when i appears before j in both sequences. Longest-path packing pushes each block as far left as those constraints allow.

## Slide 4 — Vertical constraints set y

![Vertical constraints set y](assets/steps/03-v-rules.png)

Module i is below j when i precedes j in pos but follows in neg. That fills y coordinates without overlaps for a feasible pair.

## Slide 5 — Golden SP packs legally

![Golden SP packs legally](assets/steps/04-legal.png)

Evaluating the golden sequences places all five modules with non-negative coordinates and a legal packing inside the outline.

## Slide 6 — SP neighbors are permutation moves

![SP neighbors are permutation moves](assets/steps/05-takeaway.png)

Annealing on sequence pair swaps or rotates entries in pos and neg. Feasibility stays geometric; cost can be deadspace plus wirelength.

<!-- /algorithm-walkthrough -->


## Slide 7 — Browser lab track

Open sequence-pair and Pack sequence pair. Confirm five modules, non-negative coordinates, and legality true on the golden permutations.

## Slide 8 — Implement track

Implement longest-path SP packing. Assert pos and neg are the same five ids, and the golden pair packs legally.

## Slide 9 — Pitfalls

Mismatched id sets between pos and neg; swapping the horizontal/vertical rules; negative coordinates from a buggy DP.

## Slide 10 — Your turn

Pack the golden sequences legally. Next: simulated annealing that prefers legal low-cost neighbors.
