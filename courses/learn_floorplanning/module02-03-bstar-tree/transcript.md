# B*-tree floorplan representation

**Module id:** module02-03-bstar-tree
**Lab:** bstar-tree
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — B*-tree floorplan representation

B-star stores packing adjacency: left child sits right-of the parent; right child sits above on a contour. Root A at the origin; left chain B then C then E; right child D above A.

<!-- algorithm-walkthrough -->

## Slide 2 — Root A at the origin

![Root A at the origin](assets/steps/01-root.png)

B-star packing places the root at the lower left. A lands at zero comma zero with size three by two. Left children go right-of; right children go above via the contour.

## Slide 3 — Left chain B→C→E

![Left chain B→C→E](assets/steps/02-left-chain.png)

The left spine walks rightward: B at x equals three, then C, then E. Contour heights track the skyline so later modules sit tightly.

## Slide 4 — Right child D above A

![Right child D above A](assets/steps/03-right-d.png)

D is the right child of A, so it packs above A on the contour. Its y is at least two—A's height—keeping the tree geometry honest.

## Slide 5 — Full B* pack is legal

![Full B* pack is legal](assets/steps/04-legal.png)

All five modules are placed. The packing is legal inside ten by eight. Perturbing the tree—swap, rotate, move—will feed simulated annealing later.

## Slide 6 — B* is compact and mutable

![B* is compact and mutable](assets/steps/05-takeaway.png)

B-star stores adjacency for packing, not connectivity. Get left and right semantics right, keep the contour correct, and you have a fast neighbor generator for search.

<!-- /algorithm-walkthrough -->


## Slide 7 — Browser lab track

Open bstar-tree and Pack B*-tree. Confirm A at zero comma zero, B at x equals three, D above A, and a legal five-module packing.

## Slide 8 — Implement track

Build the golden tree and contour-pack it. Assert A at (0,0), B.x equals A.x plus A.w, D.y at least A.h, and legality true.

## Slide 9 — Pitfalls

Reversing left/right geometry; stale contour segments; treating the tree as a netlist.

## Slide 10 — Your turn

Produce the legal B-star packing. Next: sequence-pair permutations as another encoding.
