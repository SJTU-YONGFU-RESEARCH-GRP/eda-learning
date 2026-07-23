---
marp: true
title: Site and row model
paginate: true
---

# Site and row model

Legalization snaps cells to a discrete grid

---

## The idea
- Every cell sits on exactly one row with a lower-left coordinate aligned to site pitch one
- Width tells you how many consecutive sites the rectangle covers
- The golden packing is legal
- <!-- algorithm-walkthrough -->

---

## Twelve-by-six chip, three rows
![Twelve-by-six chip, three rows](assets/steps/01-empty-chip.png)

---

## Cell widths A–D = 2, E–F = 1
![Cell widths A–D = 2, E–F = 1](assets/steps/02-cell-widths.png)

---

## Site pitch equals one
![Site pitch equals one](assets/steps/03-site-pitch.png)

---

## Golden legal packing
![Golden legal packing](assets/steps/04-golden-pack.png)

---

## Contrast: illegal overlap stack
![Contrast: illegal overlap stack](assets/steps/05-overlap-contrast.png)

---

## Browser lab track
- In the browser lab track, open the **site-row-model** lab from the tools shelf
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

