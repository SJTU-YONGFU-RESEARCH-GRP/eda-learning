# Slicing tree / polish expression packing

**Module id:** module02-01-slicing-floorplan
**Lab:** slicing-floorplan
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Slicing tree / polish expression packing

Slicing floorplans use through-cuts. The golden polish A D H B V C V E V stacks A under D, then attaches B, C, and E with vertical cuts—bounding box nine by three.

<!-- algorithm-walkthrough -->

## Slide 2 — Polish expression encodes cuts

![Polish expression encodes cuts](assets/steps/01-polish.png)

A slicing floorplan is a tree of through-cuts. Postfix polish A D H B V C V E V stacks A under D, then places B, C, and E to the right with vertical cuts.

## Slide 3 — A D H stacks height 3

![A D H stacks height 3](assets/steps/02-stack-ad.png)

A is three by two; D is three by one. An H cut stacks D above A into a three by three block at the lower left.

## Slide 4 — V attaches B on the right

![V attaches B on the right](assets/steps/03-attach-b.png)

Next V places B beside the A–D stack. Bounding width becomes five; height stays three.

## Slide 5 — Full polish packs BB 9×3

![Full polish packs BB 9×3](assets/steps/04-full.png)

Adding C and E with more V cuts finishes the golden polish. Bounding box is nine by three—legal inside the ten-by-eight outline.

## Slide 6 — Slicing cannot make wheels

![Slicing cannot make wheels](assets/steps/05-takeaway.png)

Not every packing is slicing. Wheel topologies need non-slicing codes like B-star or sequence pair—next labs. For slicing, polish plus H/V evaluation is enough.

<!-- /algorithm-walkthrough -->


## Slide 7 — Browser lab track

Open slicing-floorplan and Evaluate polish. Confirm bounding width nine, height three, and a legal packing inside ten by eight.

## Slide 8 — Implement track

Implement postfix evaluation for H and V. On the golden token list, assert width nine, height three, and is_legal_packing true.

## Slide 9 — Pitfalls

Swapping H/V meanings; leaving polish operands on the stack; assuming every packing is slicing—wheels need other reps.

## Slide 10 — Your turn

Ship a legal polish pack with BB nine by three. Next: B-star trees for non-slicing adjacency.
