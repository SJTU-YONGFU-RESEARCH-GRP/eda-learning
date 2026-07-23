---
marp: true
title: Detailed versus global legalize
paginate: true
---

# Detailed versus global legalize

Global legalize lite maps to Tetris shelf pack, displacement six, HPWL thirty-two

---

## The idea
- Pick global Tetris when you want a fast pass and can afford extra movement
- Pick detailed Abacus when displacement budget is tight
- Report both pipelines side by side in regressions, legal first, then disp and HPWL
- <!-- algorithm-walkthrough -->

---

## Global = Tetris, disp 6
![Global = Tetris, disp 6](assets/steps/01-global-tetris.png)

---

## Detailed = Abacus, disp 4
![Detailed = Abacus, disp 4](assets/steps/02-detailed-abacus.png)

---

## Both pipelines legal
![Both pipelines legal](assets/steps/03-both-legal.png)

---

## Side-by-side metrics
![Side-by-side metrics](assets/steps/04-side-by-side.png)

---

## Pick detailed when displacement is tight
![Pick detailed when displacement is tight](assets/steps/05-pick-detailed.png)

---

## Browser lab track
- In the browser lab track, open the **detailed-vs-global** lab from the tools shelf
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

