---
marp: true
title: Multilevel clustering
paginate: true
---

# Multilevel clustering

Multilevel clustering coarsens, partitions, then refines

---

## Coarsen with greedy merge
![Coarsen with greedy merge](assets/steps/01-coarsen.png)

---

## Project to a bipartition
![Project to a bipartition](assets/steps/02-project.png)

---

## FM-refine on the fine graph
![FM-refine on the fine graph](assets/steps/03-fm-refine.png)

---

## Golden: cutsize 3
![Golden: cutsize 3](assets/steps/04-final.png)

---

## Multilevel mindset
![Multilevel mindset](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab, run multilevel and compare with a plain greedy seed
- Clear challenges for the refined ABC|DE result

---

## Implement track
- Run multilevel on the tiny graph and confirm cutsize three
- Re-implement project-and-refine until the unit test passes

---

## Implement track — try these

```
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode multilevel
```

---

## Pitfalls to watch
- Skipping refinement leaves coarsening artifacts
- Projecting labels incorrectly scrambles the fine-level seed
- Too aggressive coarsening can erase structure

---

## Your turn
- Match the golden, finish the checklist and quiz, then continue to hypergraph clustering

