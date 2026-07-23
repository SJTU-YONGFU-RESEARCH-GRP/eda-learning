---
marp: true
title: Sequence-pair representation
paginate: true
---

# Sequence-pair representation

Sequence pair uses positive permutation A B C E D and negative D A B C E

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

