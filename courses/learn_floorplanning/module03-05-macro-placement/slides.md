---
marp: true
title: Hard macro / fixed-block placement
paginate: true
---

# Hard macro / fixed-block placement

Macros are hard fixed rectangles

---

## Free golden has movable D
![Free golden has movable D](assets/steps/01-free.png)

---

## Fix macro D at (0,0)
![Fix macro D at (0,0)](assets/steps/02-fix-d.png)

---

## Pack A–E around the macro
![Pack A–E around the macro](assets/steps/03-pack-rest.png)

---

## Macro packing is legal
![Macro packing is legal](assets/steps/04-legal.png)

---

## Macros first, then cells
![Macros first, then cells](assets/steps/05-takeaway.png)

---

## Browser lab track
- Open macro-placement
- Compare free golden D at zero comma two with Place macros: D at zero comma zero
- Confirm legality and the macro flag

---

## Implement track
- Fix D, pack the rest, assert D at (0,0), D.macro true, and is_legal_packing true
- Note the free golden differs

---

## Pitfalls
- Moving macros after fixing them

---

## Your turn
- Ship the legal macro packing
- Next: hierarchical AB left and CDE right at offset five

