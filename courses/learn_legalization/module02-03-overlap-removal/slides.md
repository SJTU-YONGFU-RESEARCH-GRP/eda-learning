---
marp: true
title: Overlap removal
paginate: true
---

# Overlap removal

Overlap removal snaps first, then left-packs each row without changing row assignment

---

## The idea
- Sort movables by x within each row and place left without overlap
- D, E, and F keep their seed roles on other rows
- This is the same shelf pack Tetris uses, simple, deterministic
- <!-- algorithm-walkthrough -->

---

## A, B, C stacked at (4, 2)
![A, B, C stacked at (4, 2)](assets/steps/01-overlap-seed.png)

---

## After snap: still stacked
![After snap: still stacked](assets/steps/02-after-snap.png)

---

## Per-row pack: A@4, B@6, C@8
![Per-row pack: A@4, B@6, C@8](assets/steps/03-row-pack.png)

---

## Legal: disp 6, HPWL 32
![Legal: disp 6, HPWL 32](assets/steps/04-legal-metrics.png)

---

## D, E, F unchanged
![D, E, F unchanged](assets/steps/05-unchanged.png)

---

## Browser lab track
- In the browser lab track, open the **overlap-removal** lab from the tools shelf
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

