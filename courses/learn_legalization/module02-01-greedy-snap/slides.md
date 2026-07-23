---
marp: true
title: Greedy snap
paginate: true
---

# Greedy snap

Global placement leaves fractional coordinates, the float seed puts A near (3.7, 1.2) and B near (4.1, 1.4)

---

## The idea
- Snap quantizes coordinates but does not remove overlap
- After snap, A and B still fail with overlap A/B
- Teaching point

---

## Pseudocode
- Greedy snap is the first written loop after global place
- Pseudocode here has one pass
- Fixed macros stay put
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- The important line in the sketch is the note after the loop: snap does not remove overlap
- On the float starter

---

## Algorithm sketch — try these

```
INPUT: float positions, widths, rows Y[], chip W
OUTPUT: snapped positions (may still overlap)
for each movable cell c:
  x ← round(x) clamped to [0, W−w[c]]
  y ← nearest row in Y[]
fixed macros: keep locked (x,y)
NOTE: snap ≠ legal — A,B may share a site
GOLDEN float: A→(4,2), B→(4,2) still overlap
```

---

## Float placement from global place
![Float placement from global place](assets/steps/01-float-seed.png)

---

## Snap every cell to nearest site
![Snap every cell to nearest site](assets/steps/02-snap-all.png)

---

## Still illegal: A/B overlap
![Still illegal: A/B overlap](assets/steps/03-still-overlap.png)

---

## Teaching point: snap ≠ legal
![Teaching point: snap ≠ legal](assets/steps/04-snap-not-legal.png)

---

## Next: overlap removal / Abacus
![Next: overlap removal / Abacus](assets/steps/05-next-phase.png)

---

## Browser lab track
- In the browser lab track, open the **greedy-snap** lab from the tools shelf
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

