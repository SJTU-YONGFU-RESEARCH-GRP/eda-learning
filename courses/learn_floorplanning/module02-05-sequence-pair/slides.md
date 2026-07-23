---
marp: true
title: Sequence-pair representation
paginate: true
---

# Sequence-pair representation

Sequence pair uses positive permutation A B C E D and negative D A B C E

---

## Pseudocode
- Sequence-pair pseudocode turns two permutations into horizontal and vertical constraints
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Golden pos is A B C E D and neg is D A B C E
- Evaluation must place all five modules legally with non-negative coordinates

---

## Algorithm sketch — try these

```
INPUT: pos[], neg[] permutations of modules
OUTPUT: (x,y) via constraint longest paths
pos/neg order ⇒ horizontal & vertical constraints
x ← longest path in H-graph; y ← V-graph
GOLDEN pos=A B C E D; neg=D A B C E
packs legally with non-negative coords
```

---

## Two permutations encode geometry
![Two permutations encode geometry](assets/steps/01-seqs.png)

---

## Horizontal constraints set x
![Horizontal constraints set x](assets/steps/02-h-rules.png)

---

## Vertical constraints set y
![Vertical constraints set y](assets/steps/03-v-rules.png)

---

## Golden SP packs legally
![Golden SP packs legally](assets/steps/04-legal.png)

---

## SP neighbors are permutation moves
![SP neighbors are permutation moves](assets/steps/05-takeaway.png)

---

## Browser lab track
- Open sequence-pair and Pack sequence pair
- Confirm five modules, non-negative coordinates

---

## Implement track
- Implement longest-path SP packing
- Assert pos and neg are the same five ids, and the golden pair packs legally

---

## Pitfalls
- Mismatched id sets between pos and neg

---

## Your turn
- Pack the golden sequences legally
- Next: simulated annealing that prefers legal low-cost neighbors

