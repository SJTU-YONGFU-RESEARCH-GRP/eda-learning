---
marp: true
title: Quadratic placement
paginate: true
---

# Quadratic placement

Quadratic-lite placement averages neighbors under fixed pads, here A and D stay pinned

---

## The idea
- Gauss–Seidel style
- Fixed pads anchor the system
- Teaching point: pad constraints raise HPWL versus unconstrained force on the same seed

---

## Pseudocode
- Quadratic-lite solves free cells toward neighbor averages under pinned pads
- Damping keeps the system from collapsing
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- With A and D fixed

---

## Algorithm sketch — try these

```
INPUT: positions, nets, fixed pads {A,D}
OUTPUT: free-cell coords + HPWL
repeat: for free c:
  blend toward neighbor average (damped)
pads A,D remain pinned
GOLDEN starter 52 → HPWL 48
```

---

## Pads A and D stay fixed
![Pads A and D stay fixed](assets/steps/01-pads-fixed.png)

---

## Free cells slide toward neighbors
![Free cells slide toward neighbors](assets/steps/02-free-cells.png)

---

## After quadratic: HPWL forty-eight
![After quadratic: HPWL forty-eight](assets/steps/03-after-quad.png)

---

## Quadratic vs unconstrained force
![Quadratic vs unconstrained force](assets/steps/04-vs-force.png)

---

## Pads anchor the solve
![Pads anchor the solve](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **quadratic-place** lab from the tools shelf
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

