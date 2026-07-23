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
- <!-- algorithm-walkthrough -->

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
- In the implement track, open this module’s examples and the course `common/` solvers
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

