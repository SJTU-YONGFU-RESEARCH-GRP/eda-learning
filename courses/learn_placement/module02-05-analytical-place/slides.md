---
marp: true
title: Analytical / density-aware place
paginate: true
---

# Analytical / density-aware place

Analytical lite first pulls for wirelength, then spreads for density with pads A and D fixed

---

## The idea
- Wirelength stage clusters
- Watch both HPWL and overflow
- <!-- algorithm-walkthrough -->

---

## Wirelength stage clusters first
![Wirelength stage clusters first](assets/steps/01-wl-stage.png)

---

## Density stage pushes overloaded bins
![Density stage pushes overloaded bins](assets/steps/02-density-stage.png)

---

## After analytical: about forty-eight point one
![After analytical: about forty-eight point one](assets/steps/03-after-anal.png)

---

## Report HPWL and overflow
![Report HPWL and overflow](assets/steps/04-both-metrics.png)

---

## Wirelength then density
![Wirelength then density](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **analytical-place** lab from the tools shelf
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

