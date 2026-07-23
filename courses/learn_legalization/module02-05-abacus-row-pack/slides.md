---
marp: true
title: Abacus row packing
paginate: true
---

# Abacus row packing

Abacus-lite processes cells by increasing x and tries every row

---

## The idea
- Cross-row spread beats single-row shelf pack on displacement
- Abacus is the detailed legalizer in this course: more search, less movement
- <!-- algorithm-walkthrough -->

---

## Start from overlap seed
![Start from overlap seed](assets/steps/01-overlap-seed.png)

---

## Process by x: try each row
![Process by x: try each row](assets/steps/02-try-rows.png)

---

## Result: A@4,2 B@4,0 C@4,4
![Result: A@4,2 B@4,0 C@4,4](assets/steps/03-abacus-result.png)

---

## Lower displacement than Tetris
![Lower displacement than Tetris](assets/steps/04-vs-overlap-removal.png)

---

## Abacus minimizes movement
![Abacus minimizes movement](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **abacus-row-pack** lab from the tools shelf
- Load the overlap or float starter, run the legalizer once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track, open this module's examples and the course `common/` solvers
- Parse `tiny_legal.json`, run the algorithm with deterministic coordinates
- Match the browser goldens before you claim the checklist

---

## Pitfalls
- Common traps

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the starter goldens
- When you're ready, take the short quiz, then continue to the next module

