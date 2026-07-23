---
marp: true
title: Label propagation clustering
paginate: true
---

# Label propagation clustering

Label propagation grows communities by letting each node adopt the strongest neighbor label

---

## Initialize: each node is its own label
![Initialize: each node is its own label](assets/steps/01-init.png)

---

## Each node adopts the winning neighbor label
![Each node adopts the winning neighbor label](assets/steps/02-vote-idea.png)

---

## After iteration 1: already clustered
![After iteration 1: already clustered](assets/steps/03-after-iter1.png)

---

## Iteration 2: no changes — stop
![Iteration 2: no changes — stop](assets/steps/04-iter2-stable.png)

---

## When LP helps in EDA flows
![When LP helps in EDA flows](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab, show the initial labels, then run label propagation
- Clear the challenges for two iterations, two communities, and the full golden label map

---

## Implement track
- Load the tiny graph and run the reference label-propagation mode
- Confirm two iterations, labels grouping A–B–C versus D–E, and cutsize three
- Re-implement the vote and tie-break until the unit test passes

---

## Implement track — try these

```
# run async label propagation on the tiny graph
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode lp

```

---

## Pitfalls to watch
- Order dependence is real, document your sweep order
- Without a tie-break, goldens flake
- And stopping only on max iterations without checking that nothing changed hides

---

## Your turn
- Match the golden table, finish the checklist and quiz, then continue to spectral bisection

