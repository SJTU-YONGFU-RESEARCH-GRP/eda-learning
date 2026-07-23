---
marp: true
title: Fixed-outline constraints
paginate: true
---

# Fixed-outline constraints

Floorplanning on this course uses a fixed outline ten by eight

---

## Pseudocode
- Fixed-outline legality is two loops in pseudocode
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Outline is ten by eight
- Golden packing of A through E is legal
- Bad seed with E at x nine overflows
- Overlap of C and E is the other failure mode

---

## Algorithm sketch — try these

```
INPUT: outline W×H, modules (x,y,w,h)
OUTPUT: legal? / failure reason
for each m: fail if outside [0,W]×[0,H]
for each pair: fail if interior overlap
edge-touch OK; positive-area overlap not
GOLDEN pack legal; E@x=9 overflow illegal
outline 10×8 (area 80); modules A–E
```

---

## Fixed outline is 10×8
![Fixed outline is 10×8](assets/steps/01-outline.png)

---

## Bad pack: E overflows
![Bad pack: E overflows](assets/steps/02-bad-overflow.png)

---

## Overlap is also illegal
![Overlap is also illegal](assets/steps/03-overlap.png)

---

## Golden pack is legal
![Golden pack is legal](assets/steps/04-golden.png)

---

## Legality is the gate
![Legality is the gate](assets/steps/05-takeaway.png)

---

## Browser lab track
- Open the fixed-outline lab
- Show the bad seed: E overflows past the right edge
- Then show overlap, then golden
- Watch legality flip from false to true when the golden packing loads

---

## Implement track
- Parse tiny_modules.json, assign (x, y)
- On the golden packing, legality must pass

---

## Pitfalls
- Off-by-one edges, treating centers as rectangles
- Edge-touching is allowed; interior overlap is not

---

## Your turn
- Get a legal packing of A through E inside ten by eight
- Quiz checks the overflow failure and the golden pass
- Next: deadspace fifty-seven on this same instance

