---
marp: true
title: Timing-aware clustering
paginate: true
---

# Timing-aware clustering

Critical nets should stay uncut

---

## Mark critical edges
![Mark critical edges](assets/steps/01-criticality.png)

---

## Reweight then refine
![Reweight then refine](assets/steps/02-weight.png)

---

## Land on ABC|DE
![Land on ABC|DE](assets/steps/03-result.png)

---

## Critical edges uncut
![Critical edges uncut](assets/steps/04-protect.png)

---

## Timing as an objective
![Timing as an objective](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab, run timing-aware refinement from the bad seed
- Confirm plain cut three and weighted cut seven

---

## Implement track
- Run timing-aware mode and confirm ABC versus DE, plain three, weighted seven

---

## Implement track — try these

```
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode timing --seed ../module02-05-kernighan-lin/examples/seed_partition.json --criticality examples/criticality.json

```

---

## Pitfalls to watch
- Criticality of one means no boost, document defaults
- Mixing plain and weighted metrics in the same table confuses compares

---

## Your turn
- Match the golden

