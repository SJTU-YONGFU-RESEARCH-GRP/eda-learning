# Hierarchical floorplanning

**Module id:** module04-01-hierarchical-floorplan
**Lab:** hierarchical-floorplan
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Hierarchical floorplanning

Hierarchy packs cluster AB on the left and cluster CDE on the right with x offset five. Local pack, then place clusters—legal overall with clusters separated in x.


## Slide 2 — Pseudocode

Hierarchical floorplan packs inside clusters first, then packs the cluster bounding boxes in the outline.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 3 — Algorithm sketch

Teaching golden places cluster A B on the left and C D E on the right starting at x equals five.

```text
INPUT: clusters of modules
OUTPUT: top-level pack of cluster bboxes
pack each cluster internally (slice/B*/SA)
pack cluster bboxes in outline
GOLDEN teaching: AB left; CDE right @x=5
```


<!-- algorithm-walkthrough -->

## Slide 4 — Two clusters: AB and CDE

![Two clusters: AB and CDE](assets/steps/01-clusters.png)

Hierarchy packs locally first. Left cluster holds A and B; right cluster holds C, D, and E. Each cluster is a mini-floorplan.

## Slide 5 — Left cluster packs at x<5

![Left cluster packs at x<5](assets/steps/02-left.png)

AB occupies the left side with A at the origin and B at x equals three. Everything in this cluster stays left of x equals five.

## Slide 6 — Right cluster offsets by 5

![Right cluster offsets by 5](assets/steps/03-right.png)

CDE packs in local coordinates, then shifts by five in x. C, D, and E all land at x greater than or equal to five—no cluster overlap.

## Slide 7 — Hierarchy is legal overall

![Hierarchy is legal overall](assets/steps/04-legal.png)

Placing the two cluster bounding boxes yields a legal chip packing. Hierarchy scales: recurse inside clusters, then assemble.

## Slide 8 — Hierarchy reuses the same engines

![Hierarchy reuses the same engines](assets/steps/05-takeaway.png)

Each level can use slicing, B-star, or SA. The teaching golden is simply AB left and CDE right at offset five.

<!-- /algorithm-walkthrough -->


## Slide 9 — Browser lab track

Open hierarchical-floorplan and Pack hierarchy. Confirm A and B have x less than five, C D E have x at least five, and legality true.

## Slide 10 — Implement track

Implement pack_hierarchical. Assert leftMax x+w is at most rightMin x, five modules present, and legality true.

## Slide 11 — Pitfalls

Overlapping cluster bounding boxes; forgetting the offset; applying different legality rules at each level.

## Slide 12 — Your turn

Accept the AB | CDE packing. Next: assign pins P0 through P3 on all four outline sides.
