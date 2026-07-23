---
marp: true
title: Hard macros
paginate: true
---

# Hard macros

Hard macros are fixed-size blocks, memories, analog IP, pre-placed covers

---

## The idea
- Mark macros as hard: width and height immutable
- If position is fixed, lock (x, y) and forbid moves that shift them
- Other modules pack in the remaining free space
- Cost still includes overflow and deadspace
- Legality checks apply unchanged, macros are just immovable obstacles

---

## Browser lab track
- Open **macro-placement**
- Lock one module as a fixed hard block
- Try to pack the others around it
- Force an overlap and watch the checker
- Unlock and compare freedom
- Then encode fixed blocks in your Track A data model

---

## Implement track
- Extend `tiny_modules.json` with a `fixed: true` and optional `x`, `y` on one module
- Pack the rest with your chosen representation, treating the macro as an obstacle
- Fail loudly if a move would shift a fixed macro
- Report legality and deadspace

---

## Pitfalls
- Silently moving a “fixed” macro during SA is a trust-breaking bug
- Also don’t shrink hard macros when soft sizing runs
- Overlapping two macros at init means the instance is already illegal

---

## Your turn
- Produce a legal packing with at least one fixed hard macro
- Next: hierarchical floorplans that nest sub-packings inside parent regions

