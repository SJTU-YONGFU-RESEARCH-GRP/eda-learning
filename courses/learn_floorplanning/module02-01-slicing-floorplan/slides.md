---
marp: true
title: Slicing tree / polish expression packing
paginate: true
---

# Slicing tree / polish expression packing

Slicing floorplans use through-cuts

---

## Polish expression encodes cuts
![Polish expression encodes cuts](assets/steps/01-polish.png)

---

## A D H stacks height 3
![A D H stacks height 3](assets/steps/02-stack-ad.png)

---

## V attaches B on the right
![V attaches B on the right](assets/steps/03-attach-b.png)

---

## Full polish packs BB 9×3
![Full polish packs BB 9×3](assets/steps/04-full.png)

---

## Slicing cannot make wheels
![Slicing cannot make wheels](assets/steps/05-takeaway.png)

---

## Browser lab track
- Open slicing-floorplan and Evaluate polish
- Confirm bounding width nine, height three, and a legal packing inside ten by eight

---

## Implement track
- Implement postfix evaluation for H and V
- On the golden token list, assert width nine, height three, and is_legal_packing true

---

## Pitfalls
- Swapping H/V meanings

---

## Your turn
- Ship a legal polish pack with BB nine by three
- Next: B-star trees for non-slicing adjacency

