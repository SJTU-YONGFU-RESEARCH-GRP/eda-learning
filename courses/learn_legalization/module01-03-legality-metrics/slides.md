---
marp: true
title: Legality metrics
paginate: true
---

# Legality metrics

Before you celebrate wirelength, ask whether the placement is legal

---

## The idea
- Check on-row placement, site alignment, in-chip bounds, and pairwise overlap
- Report displacement as L1 Manhattan distance from the origin layout
- Pair legality with HPWL after legalize
- <!-- algorithm-walkthrough -->

---

## Overlap seed is illegal
![Overlap seed is illegal](assets/steps/01-overlap-illegal.png)

---

## Four legality checks
![Four legality checks](assets/steps/02-checks.png)

---

## Golden placement passes
![Golden placement passes](assets/steps/03-golden-ok.png)

---

## Displacement: L1 from origin
![Displacement: L1 from origin](assets/steps/04-displacement.png)

---

## HPWL after legalize
![HPWL after legalize](assets/steps/05-hpwl-after.png)

---

## Browser lab track
- In the browser lab track, open the **legality-metrics** lab from the tools shelf
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

