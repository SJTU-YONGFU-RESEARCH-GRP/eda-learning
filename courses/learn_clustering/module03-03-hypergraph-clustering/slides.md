---
marp: true
title: Hypergraph clustering
paginate: true
---

# Hypergraph clustering

Netlists are hypergraphs, one net can touch many pins

---

## Nets are hyperedges
![Nets are hyperedges](assets/steps/01-nets.png)

---

## Affinity = shared pin weight
![Affinity = shared pin weight](assets/steps/02-affinity.png)

---

## Merge down to K=2
![Merge down to K=2](assets/steps/03-merge-k2.png)

---

## Hyperedge cut = 1
![Hyperedge cut = 1](assets/steps/04-cut-1.png)

---

## Why hypergraphs in EDA
![Why hypergraphs in EDA](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab, load the starter hypergraph and run greedy clustering to K equals two
- Confirm hyperedge cut one for ABC versus DE

---

## Implement track
- Run hypergraph greedy to K equals two
- Confirm hyperedge cut one and the natural clusters

---

## Implement track — try these

```
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_hypergraph.json --mode hypergraph --k 2
```

---

## Pitfalls to watch
- Clique-expanding hyperedges changes the objective
- Counting a cut once per hyperedge, not per pair, is required
- Empty or singleton nets must be filtered

---

## Your turn
- Match hyperedge cut one

