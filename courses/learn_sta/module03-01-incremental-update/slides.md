---
marp: true
title: Incremental timing update
paginate: true
---

# Incremental timing update

Real timers cannot rebuild the chip after every buffer insert

---

## Goldens to remember
- Invalidated cone: u1/Y, u2/A, u2/Y, out
- Clean: in, u1/A
- ΔA(out)=+0.8
- Keep these numbers handy, the browser challenges and Track A tests use the same instance
- <!-- algorithm-walkthrough -->

---

## Start from a full analysis
![Start from a full analysis](assets/steps/01-base-tags.png)

---

## Edit one cell delay
![Edit one cell delay](assets/steps/02-local-edit.png)

---

## Invalidate the fanout cone
![Invalidate the fanout cone](assets/steps/03-invalidate-cone.png)

---

## Recompute only the dirty pins
![Recompute only the dirty pins](assets/steps/04-recompute.png)

---

## Why timers insist on incremental
![Why timers insist on incremental](assets/steps/05-why-incremental.png)

---

## Browser lab track
- In the browser lab, open **incremental-update**
- Load the starter, run the analysis once, and read the metrics panel
- Orient yourself, challenge panel, canvas, Check, then mirror the same goldens in code

---

## Implement track
- In the implement track
- Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print

---

## Pitfall
- Do not mix setup and hold required maps
- Do not propagate before the graph is levelized
- After an edit or exception, recompute, stale tags lie

---

## Your turn
- Finish the checklist on at least one track, preferably both
- When your numbers match the goldens, take the quiz, then continue

