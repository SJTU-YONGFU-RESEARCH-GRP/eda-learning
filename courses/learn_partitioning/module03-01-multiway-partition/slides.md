---
marp: true
title: Multiway partitioning
paginate: true
---

# Multiway partitioning

Direct multiway partitioning assigns nodes to k parts without forcing a binary tree of cuts

---

## The idea
- Multiway objectives count every edge that leaves its part
- Balance becomes a k-way size vector
- Teaching point

---

## Pseudocode
- Multiway compares two constructors in pseudocode
- Both must report the same cutsize metric
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Recursive k equals three lands A B, C, and D E with cut eight
- Alphabetical round-robin shreds heavy edges and scores about eighteen

---

## Algorithm sketch — try these

```
INPUT: G, k
OUTPUT: k-way assignment + cutsize
method A: recursive_bisection(G,k)
method B: round-robin / block assign labels
cut ← Σ w where side[u]≠side[v]
GOLDEN k=3 recursive: AB|C|DE cut=8
round-robin alphabetic: cut≈18 (worse)
```

---

## k-way vs naive assignment
![k-way vs naive assignment](assets/steps/01-problem.png)

---

## Recursive: AB|C|DE cut 8
![Recursive: AB|C|DE cut 8](assets/steps/02-recursive.png)

---

## Round-robin: AD|BE|C cut 18
![Round-robin: AD|BE|C cut 18](assets/steps/03-roundrobin.png)

---

## Structure beats indexing
![Structure beats indexing](assets/steps/04-compare.png)

---

## Multiway literacy
![Multiway literacy](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **multiway-partition** lab from the tools shelf
- Load the starter graph, run the algorithm once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track
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

