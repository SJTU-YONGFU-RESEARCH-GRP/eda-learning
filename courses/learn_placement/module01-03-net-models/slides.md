---
marp: true
title: Net models for wirelength
paginate: true
---

# Net models for wirelength

Multi-pin nets need a model before you optimize

---

## The idea
- Bbox is cheap and standard
- Clique overestimates affinity on multi-pin nets
- Star depends on the hub choice
- Use one model for the reported objective and say which
- <!-- algorithm-walkthrough -->

---

## Bbox HPWL is the default report
![Bbox HPWL is the default report](assets/steps/01-bbox-default.png)

---

## Clique sums every pair
![Clique sums every pair](assets/steps/02-clique-model.png)

---

## Star depends on the hub
![Star depends on the hub](assets/steps/03-star-model.png)

---

## Same pins, three numbers
![Same pins, three numbers](assets/steps/04-compare-models.png)

---

## Name the model you optimize
![Name the model you optimize](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **net-models** lab from the tools shelf
- Load the starter placement, run the algorithm once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track, open this module’s examples and the course `common/` solvers
- Parse `tiny_place.json`, run the algorithm with a deterministic seed
- Match the browser goldens before you claim the checklist

---

## Pitfalls
- Common traps

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the starter goldens
- When you’re ready, take the short quiz, then continue to the next module

