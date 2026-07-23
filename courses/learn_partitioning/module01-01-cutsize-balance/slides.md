---
marp: true
title: Cutsize and balance
paginate: true
---

# Cutsize and balance

Cutsize adds the weights of edges that cross the cut

---

## The idea
- For every edge, if the endpoints sit in different parts, add its weight to the cut
- Balance ratio is the smaller part size over the larger
- Never celebrate a zero cut that parks every node on one side
- <!-- algorithm-walkthrough -->

---

## Same graph, two bipartitions
![Same graph, two bipartitions](assets/steps/01-graph.png)

---

## Bad seed: cutsize 12
![Bad seed: cutsize 12](assets/steps/02-bad-seed.png)

---

## Bad seed balance: ratio 2/3
![Bad seed balance: ratio 2/3](assets/steps/03-bad-balance.png)

---

## Golden ABC|DE: cutsize 3
![Golden ABC|DE: cutsize 3](assets/steps/04-golden.png)

---

## Cutsize + balance literacy
![Cutsize + balance literacy](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **cutsize-balance** lab from the tools shelf
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

