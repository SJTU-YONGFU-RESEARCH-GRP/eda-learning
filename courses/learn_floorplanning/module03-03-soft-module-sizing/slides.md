---
marp: true
title: Soft module aspect sizing
paginate: true
---

# Soft module aspect sizing

Soft module A keeps area six but may reshape between aspect one half and two

---

## A is soft with area 6
![A is soft with area 6](assets/steps/01-soft-a.png)

---

## Reshape A to 2×3
![Reshape A to 2×3](assets/steps/02-reshape.png)

---

## Soft packing stays legal
![Soft packing stays legal](assets/steps/03-legal.png)

---

## Hard vs soft views
![Hard vs soft views](assets/steps/04-compare.png)

---

## Softness is constrained freedom
![Softness is constrained freedom](assets/steps/05-takeaway.png)

---

## Browser lab track
- Open soft-module-sizing
- Show hard three-by-two, then Reshape A to two by three
- Confirm area six and legality true on the soft packing

---

## Implement track
- Implement resize_soft that preserves area, then pack
- Assert soft A ends at two by three with area six and a legal outline fit

---

## Pitfalls
- Changing area when reshaping; ignoring aspect bounds; leaving hard modules soft by mistake

---

## Your turn
- Accept a legal soft packing with A at two by three
- Next: fix macro D at the origin

