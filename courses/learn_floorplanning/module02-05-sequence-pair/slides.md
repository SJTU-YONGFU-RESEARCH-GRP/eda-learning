---
marp: true
title: Sequence pairs
paginate: true
---

# Sequence pairs

A sequence pair is two permutations of the modules, often called the positive and negative sequences, Γ-plus and Γ-minus

---

## The idea
- If module A appears before B in both sequences, A is left of B
- If A appears before B in Γ-plus but after B in Γ-minus
- Horizontal and vertical constraint graphs yield x and y via longest paths
- Soft sizing and rotation can be layered on later; first get hard rectangles right

---

## Browser lab track
- Open **sequence-pair**
- Load starter Γ-plus and Γ-minus
- Highlight one pair of modules and read the implied relation, left-of or above
- Pack and inspect deadspace under the fixed outline
- Swap two symbols in one sequence and watch relations flip
- Then implement packing from sequences in Track A

---

## Implement track
- Represent Γ-plus and Γ-minus as lists of module ids
- Build constraint edges, compute coordinates
- Report deadspace
- Keep permutations as permutations, no duplicate ids
- Deterministic packing helps goldens

---

## Pitfalls
- Mixing up which sequence pair condition means “left of” versus “above” yields mirrored
- Forgetting transitive longest-path compaction leaves unnecessary whitespace
- And sequence pairs can encode non-slicing packings

---

## Your turn
- Pack A–E from a sequence pair and verify legality
- Next you’ll search the space of representations with simulated annealing

