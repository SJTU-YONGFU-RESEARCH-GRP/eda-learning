---
marp: true
title: Congestion-aware clustering
paginate: true
---

# Congestion-aware clustering

When bridge edges are congested, cutting them becomes expensive

---

## Start from BAD_SEED
![Start from BAD_SEED](assets/steps/01-bad-seed.png)

---

## λ=0 → ordinary FM
![λ=0 → ordinary FM](assets/steps/02-lam0.png)

---

## Boost weights by λ·cong
![Boost weights by λ·cong](assets/steps/03-boost.png)

---

## λ=5 → pen 0, plain 5
![λ=5 → pen 0, plain 5](assets/steps/04-lam5.png)

---

## Objective tradeoffs
![Objective tradeoffs](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab, compare lambda zero with lambda five from the same bad seed
- Watch the penalty drop to zero when the congested bridge is avoided

---

## Implement track
- Run congestion-aware partition at lambda zero and five
- Confirm plain cut three with penalty nine at lambda zero

---

## Implement track — try these

```
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode congestion --seed ../module02-05-kernighan-lin/examples/seed_partition.json --congestion examples/congestion.json --lambda 5
```

---

## Pitfalls to watch
- Applying congestion only after FM misses the point, weights must change before moves
- Huge lambda can ignore connectivity entirely

---

## Your turn
- Match both lambda goldens

