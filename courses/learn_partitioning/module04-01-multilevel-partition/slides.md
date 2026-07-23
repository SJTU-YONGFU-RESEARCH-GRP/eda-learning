---
marp: true
title: Multilevel partitioning
paginate: true
---

# Multilevel partitioning

A multilevel V-cycle coarsens the graph, partitions the tiny problem, projects the assignment back

---

## The idea
- Coarsening shrinks the search space
- The coarse partition is cheap
- Projection gives a feasible fine assignment that FM or KL can polish
- A bug in coarsening poisons every finer level
- <!-- algorithm-walkthrough -->

---

## Coarsen with greedy merge
![Coarsen with greedy merge](assets/steps/01-coarsen.png)

---

## Project to fine bipartition
![Project to fine bipartition](assets/steps/02-project.png)

---

## FM refine on fine graph
![FM refine on fine graph](assets/steps/03-refine.png)

---

## Final P0/P1 labels
![Final P0/P1 labels](assets/steps/04-final.png)

---

## Multilevel V-cycle mindset
![Multilevel V-cycle mindset](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **multilevel-partition** lab from the tools shelf
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

