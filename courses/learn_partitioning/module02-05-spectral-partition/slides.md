---
marp: true
title: Spectral bipartition
paginate: true
---

# Spectral bipartition

Spectral bipartition reads connectivity from the graph Laplacian

---

## The idea
- Build L equals D minus A, take the second eigenvector, sort nodes
- Reject lopsided splits
- The continuous membership becomes a hard bipartition only after the sweep chooses the best
- <!-- algorithm-walkthrough -->

---

## Build the Laplacian
![Build the Laplacian](assets/steps/01-laplacian.png)

---

## Sort by Fiedler value
![Sort by Fiedler value](assets/steps/02-fiedler-order.png)

---

## Sweep prefixes for best cut
![Sweep prefixes for best cut](assets/steps/03-sweep-cut.png)

---

## Result ABC|DE
![Result ABC|DE](assets/steps/04-final.png)

---

## When spectral helps
![When spectral helps](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **spectral-partition** lab from the tools shelf
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

