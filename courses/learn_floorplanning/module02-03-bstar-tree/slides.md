---
marp: true
title: B*-tree floorplans
paginate: true
---

# B*-tree floorplans

B*-trees are a popular compacted floorplan representation

---

## The idea
- Root at the lower-left
- Walking left children grows the packing rightward
- Packing is typically done with a horizontal contour so y coordinates stay compacted
- Perturbing the tree, rotate, move, swap, yields neighboring packings for annealing later

---

## Browser lab track
- Open **bstar-tree**
- Load a starter tree over A–E
- Step placement: parent, left child, right child
- Watch modules land left/right/above as the contour updates
- Inspect outline legality and deadspace
- Then code the same left/right packing rules

---

## Implement track
- Build a B*-tree for the tiny modules
- Implement contour-based packing to emit (x, y, w, h)
- Verify non-overlap and outline containment
- Print the tree in a readable parenthesized form so goldens are reviewable
- Prefer deterministic child ordering for tests

---

## Pitfalls
- Getting left/right geometry backwards is the number-one bug
- Contour updates that forget deleted segments leave modules floating or overlapping
- Don’t confuse B*-tree adjacency with netlist adjacency

---

## Your turn
- Produce a legal B*-tree packing inside the outline
- Next: sequence pairs, another classic encoding with positive and negative sequences

