---
marp: true
title: Half-perimeter wirelength
paginate: true
---

# Half-perimeter wirelength

Placement assigns cell coordinates to cut wirelength while keeping density under control

---

## The idea
- Bbox half-perimeter wirelength (HPWL) metrics
- You’ll take a placement instance, apply the update rule until a stop condition
- Watch HPWL every time, and density overflow when the lab uses bins

---

## Browser lab track
- In the browser lab track, open the **hpwl-metrics** lab from the tools shelf
- Load the starter placement, run the algorithm once, and read the metrics panel
- Orient yourself

---

## Implement track
- In the implement track, open this module’s examples and build the full algorithm
- Parse the tiny placement, run the core loop with clear stop rules
- Prefer a deterministic seed so your golden answers stay stable

---

## Pitfalls
- Common traps

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the expected range on the starter placement
- When you’re ready, take the short quiz, then continue to the next module

