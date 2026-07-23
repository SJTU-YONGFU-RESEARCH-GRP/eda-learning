---
marp: true
title: Hypergraph partitioning
paginate: true
---

# Hypergraph partitioning

Netlists are hypergraphs: one net can touch many cells

---

## The idea
- Optimize hyperedge cut, not only pairwise edge cut
- Multi-pin nets dominate affinity in real designs
- Use clique expansion only for drawing or as a heuristic substrate

---

## Pseudocode
- Hypergraph cut counts a net once if it spans more than one part
- Pseudocode is a span check per hyperedge
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- On the starter hypergraph, golden ABC versus DE leaves a single cut net
- Expanding to a clique can tell a different numeric story, report which model you used

---

## Algorithm sketch — try these

```
INPUT: hyperedges e={pins…}, side[]
OUTPUT: hyperedge_cut
cut ← count edges with |{side[p]:p∈e}| > 1
(optional) expand to pairwise clique for KL/FM
GOLDEN ABC|DE: one cut net on starter H
pairwise clique expansion can differ
```

---

## Nets are hyperedges
![Nets are hyperedges](assets/steps/01-nets.png)

---

## Bad seed: hyperedge cut 6
![Bad seed: hyperedge cut 6](assets/steps/02-bad-seed.png)

---

## FM on clique expansion
![FM on clique expansion](assets/steps/03-fm-run.png)

---

## Refined ABC|DE: hyper cut 1
![Refined ABC|DE: hyper cut 1](assets/steps/04-refined.png)

---

## Why hypergraphs in partition
![Why hypergraphs in partition](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **hypergraph-partition** lab from the tools shelf
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

