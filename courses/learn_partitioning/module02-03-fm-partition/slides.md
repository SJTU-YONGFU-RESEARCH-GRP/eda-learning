---
marp: true
title: Fiduccia–Mattheyses bipartition
paginate: true
---

# Fiduccia–Mattheyses bipartition

Fiduccia–Mattheyses moves one vertex at a time instead of swapping a pair

---

## The idea
- Bucketed single-vertex gains, lock after each move
- Two legal flips can equal one KL swap’s total gain on this instance
- <!-- algorithm-walkthrough -->

---

## Same bad seed, different move set
![Same bad seed, different move set](assets/steps/01-bad-seed.png)

---

## Move 1: flip D (gain 3)
![Move 1: flip D (gain 3)](assets/steps/02-move-d.png)

---

## Move 2: flip A (gain 6)
![Move 2: flip A (gain 6)](assets/steps/03-move-a.png)

---

## Final ABC|DE, cutsize 3
![Final ABC|DE, cutsize 3](assets/steps/04-final.png)

---

## Pass 1 confirms local optimum
![Pass 1 confirms local optimum](assets/steps/05-pass1-stop.png)

---

## Browser lab track
- In the browser lab track, open the **fm-partition** lab from the tools shelf
- Load the starter graph, run the algorithm once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track, open this module’s examples and the course `common/` solvers
- Parse the tiny graph, run the algorithm with a deterministic seed
- Match the browser goldens before you claim the checklist

---

## Pitfalls
- Common traps
- For multilevel flows, verify coarsening before you blame the refiner

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the starter goldens
- When you’re ready, take the short quiz, then continue to the next module

