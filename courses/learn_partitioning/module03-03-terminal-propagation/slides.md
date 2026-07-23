---
marp: true
title: Terminal propagation
paginate: true
---

# Terminal propagation

Pads and fixed I/O pin nodes to sides before free cells move

---

## The idea
- Fixed terminals never flip
- Their neighbors inherit a pull toward the terminal’s part
- Ignoring terminals produces pretty cuts that violate the floorplan interface
- <!-- algorithm-walkthrough -->

---

## Fix pads A and E to opposite sides
![Fix pads A and E to opposite sides](assets/steps/01-fixed-terminals.png)

---

## B joins A (w=5)
![B joins A (w=5)](assets/steps/02-b-joins-a.png)

---

## D joins E (w=5)
![D joins E (w=5)](assets/steps/03-d-joins-e.png)

---

## C bridges by neighbor vote
![C bridges by neighbor vote](assets/steps/04-c-bridge.png)

---

## Fixed I/O drives partition
![Fixed I/O drives partition](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **terminal-propagation** lab from the tools shelf
- Load the starter graph, run the algorithm once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track, open this module’s examples and the course `common/` solvers
- Parse the tiny graph, run the algorithm with a deterministic seed
- Match the browser goldens before you claim the checklist

---

## Pitfalls
- Common traps
- For multilevel flows, verify coarsening before you blame the refiner

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the starter goldens
- When you’re ready, take the short quiz, then continue to the next module

