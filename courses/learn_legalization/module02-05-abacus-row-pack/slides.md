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

---

## Pseudocode
- Abacus needs a nested loop in pseudocode: outer cells in x order, inner trial of every row
- For each trial you compute leftmost legal x and an L1 cost back to the origin
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Fixed macros sit first so their intervals block later trials
- On the overlap seed the sketch lands A at four two

---

## Algorithm sketch — try these

```
INPUT: origin, widths, rows Y[], fixed macros
OUTPUT: legal pack minimizing Σ L1 move
place fixed macros first
order ← movables by origin.x
for each cell c in order:
  for each row y: trial leftmost legal x
  keep (x,y) with min |Δx|+|Δy| to origin
  place c at best
GOLDEN: A(4,2) B(4,0) C(4,4); disp=4; HPWL=38
```

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
- Open the interactive lab
- Reveal golden is study-only
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track
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

