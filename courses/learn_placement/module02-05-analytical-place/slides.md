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

---

## Pseudocode
- Analytical lite is three stages in pseudocode
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Default teaching run lands near forty-eight point one HPWL
- Winning wirelength while overflowing every bin is not success, report both metrics

---

## Algorithm sketch — try these

```
INPUT: positions, bins, pads
OUTPUT: positions, HPWL, overflow
stage1: wirelength pull (force/quad style)
stage2: push out of overloaded bins
stage3: light reconnect for HPWL
report HPWL and overflow together
GOLDEN lite ≈48.1 HPWL after defaults
```

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

