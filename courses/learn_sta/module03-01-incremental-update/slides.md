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

---

## Pseudocode
- Incremental STA is cone invalidation plus selective recompute
- After an arc delay edit
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Bump the u1 cell delay from one point two to two
- The golden cone is u1/Y, u2/A, u2/Y, and out
- Arrival at out becomes four and setup slack six

---

## Algorithm sketch — try these

```
INPUT: G, edit u→v delay:=d', A_old
OUTPUT: A_new, invalidated cone
set delay(u,v)←d'
inv ← BFS successors from v (incl. v)
delete A[p] for p in inv
recompute A in topo order for missing pins
GOLDEN edit 1.2→2.0 on u1 cell:
  inv={u1/Y,u2/A,u2/Y,out}; A[out]=4.0
```

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

