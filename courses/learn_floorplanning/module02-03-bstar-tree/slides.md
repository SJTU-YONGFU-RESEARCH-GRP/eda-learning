---
marp: true
title: B*-tree floorplan representation
paginate: true
---

# B*-tree floorplan representation

B-star stores packing adjacency: left child sits right-of the parent; right child sits above on a contour

---

## Root A at the origin
![Root A at the origin](assets/steps/01-root.png)

---

## Left chain B→C→E
![Left chain B→C→E](assets/steps/02-left-chain.png)

---

## Right child D above A
![Right child D above A](assets/steps/03-right-d.png)

---

## Full B* pack is legal
![Full B* pack is legal](assets/steps/04-legal.png)

---

## B* is compact and mutable
![B* is compact and mutable](assets/steps/05-takeaway.png)

---

## Browser lab track
- Open bstar-tree and Pack B*-tree
- Confirm A at zero comma zero, B at x equals three, D above A

---

## Implement track
- Build the golden tree and contour-pack it
- Assert A at (0,0), B.x equals A.x plus A.w, D.y at least A.h, and legality true

---

## Pitfalls
- Reversing left/right geometry; stale contour segments; treating the tree as a netlist

---

## Your turn
- Produce the legal B-star packing
- Next: sequence-pair permutations as another encoding

