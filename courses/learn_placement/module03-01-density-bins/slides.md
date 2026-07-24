---
marp: true
title: Density bins and overflow
paginate: true
---

# Density bins and overflow

Density bins count cells on a grid and sum overflow above capacity

---

## The idea
- Assign each cell to a bin by coordinates
- Report HPWL and overflow together
- A pretty wirelength with piled bins fails the density half of placement

---

## Pseudocode
- Density bins count occupants per grid cell and sum overflow above capacity
- Pseudocode always pairs that number with HPWL
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- On a two-by-two grid with capacity one, both starter and golden still overflow by two
- Raise capacity to two on golden and overflow drops to one

---

## Algorithm sketch — try these

```
INPUT: positions, grid Gx×Gy, capacity C
OUTPUT: overflow, per-bin counts
assign each cell to a bin by (x,y)
overflow ← Σ max(0, count[b]−C)
report HPWL with overflow
GOLDEN 2×2 C=1: starter&golden overflow=2
C=2 on golden → overflow=1
```

---

## Partition the die into bins
![Partition the die into bins](assets/steps/01-grid-idea.png)

---

## Starter overflows by two
![Starter overflows by two](assets/steps/02-starter-overflow.png)

---

## Golden also overflows at cap one
![Golden also overflows at cap one](assets/steps/03-golden-still-overflow.png)

---

## Raise capacity to ease overflow
![Raise capacity to ease overflow](assets/steps/04-raise-capacity.png)

---

## HPWL and density travel together
![HPWL and density travel together](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **density-bins** lab from the tools shelf
- Load the starter placement, run the algorithm once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track
- Parse `tiny_place.json`, run the algorithm with a deterministic seed
- Match the browser goldens before you claim the checklist

---

## Pitfalls
- Common traps

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the starter goldens
- When you’re ready, take the short quiz, then continue to the next module

