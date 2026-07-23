---
marp: true
title: Hierarchical floorplanning
paginate: true
---

# Hierarchical floorplanning

Hierarchy packs cluster AB on the left and cluster CDE on the right with x offset five

---

## Pseudocode
- Hierarchical floorplan packs inside clusters first
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Teaching golden places cluster A B on the left and C D E on the right starting at x equals

---

## Algorithm sketch — try these

```
INPUT: clusters of modules
OUTPUT: top-level pack of cluster bboxes
pack each cluster internally (slice/B*/SA)
pack cluster bboxes in outline
GOLDEN teaching: AB left; CDE right @x=5
```

---

## Two clusters: AB and CDE
![Two clusters: AB and CDE](assets/steps/01-clusters.png)

---

## Left cluster packs at x<5
![Left cluster packs at x<5](assets/steps/02-left.png)

---

## Right cluster offsets by 5
![Right cluster offsets by 5](assets/steps/03-right.png)

---

## Hierarchy is legal overall
![Hierarchy is legal overall](assets/steps/04-legal.png)

---

## Hierarchy reuses the same engines
![Hierarchy reuses the same engines](assets/steps/05-takeaway.png)

---

## Browser lab track
- Open hierarchical-floorplan and Pack hierarchy
- Confirm A and B have x less than five, C D E have x at least five, and legality true

---

## Implement track
- Implement pack_hierarchical
- Assert leftMax x+w is at most rightMin x, five modules present, and legality true

---

## Pitfalls
- Overlapping cluster bounding boxes

---

## Your turn
- Accept the AB | CDE packing
- Next: assign pins P0 through P3 on all four outline sides

