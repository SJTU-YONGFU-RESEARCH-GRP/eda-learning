---
marp: true
title: Size-constrained agglomerative clustering
paginate: true
---

# Size-constrained agglomerative clustering

Size caps change which merges are legal

---

## Capacity blocks illegal merges
![Capacity blocks illegal merges](assets/steps/01-capacity-rule.png)

---

## Merge A–B (still legal)
![Merge A–B (still legal)](assets/steps/02-merge-ab.png)

---

## Merge D–E; C stays alone
![Merge D–E; C stays alone](assets/steps/03-merge-de.png)

---

## Result: cutsize 8
![Result: cutsize 8](assets/steps/04-cut-8.png)

---

## Why capacity matters in EDA
![Why capacity matters in EDA](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab
- Clear the challenges for blocked size-three clusters and the AB|C|DE parts

---

## Implement track
- Run greedy merge with capacity two and confirm cutsize eight with parts AB|C|DE
- Then lift capacity to three and recover the unconstrained ABC|DE cutsize three

---

## Implement track — try these

```
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --k 2 --capacity 2

```

---

## Pitfalls to watch
- Forgetting to check capacity before contracting is the classic bug
- Also watch stale affinities after a blocked merge candidate is skipped

---

## Your turn
- Match the capacity-two golden

