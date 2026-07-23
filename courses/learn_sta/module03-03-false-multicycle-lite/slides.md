---
marp: true
title: False and multicycle paths (engine view)
paginate: true
---

# False and multicycle paths (engine view)

Exceptions change which arcs propagate and how large the required window is

---

## Goldens to remember
- Multicycle cycles=2 → R(out)=20, slack=16.8
- False-path disables u1/Y→u2/A so A(u2/A) falls to 0 in the lite model
- Keep these numbers handy, the browser challenges and Track A tests use the same instance
- <!-- algorithm-walkthrough -->

---

## Normal single-cycle setup
![Normal single-cycle setup](assets/steps/01-normal-check.png)

---

## Multicycle widens the required window
![Multicycle widens the required window](assets/steps/02-multicycle.png)

---

## False path disables an arc
![False path disables an arc](assets/steps/03-false-path.png)

---

## Exceptions are engine data
![Exceptions are engine data](assets/steps/04-engine-data.png)

---

## Always recheck after exceptions
![Always recheck after exceptions](assets/steps/05-recheck.png)

---

## Browser lab track
- In the browser lab, open **false-multicycle-lite**
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

