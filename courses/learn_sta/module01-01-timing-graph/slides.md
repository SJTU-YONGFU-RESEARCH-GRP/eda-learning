---
marp: true
title: Timing graph
paginate: true
---

# Timing graph

Static timing starts with a directed timing graph

---

## Goldens to remember
- Goldens: six pins, five arcs, levels zero through five, path delay three point two
- A cycle returns no levels
- Keep these numbers handy, the browser challenges and Track A tests use the same instance
- <!-- algorithm-walkthrough -->

---

## Start with a tiny timing chain
![Start with a tiny timing chain](assets/steps/01-tiny-chain.png)

---

## Name sources and sinks
![Name sources and sinks](assets/steps/02-sources-sinks.png)

---

## Levelize with Kahn's algorithm
![Levelize with Kahn's algorithm](assets/steps/03-levelize.png)

---

## Topo order and delay sums
![Topo order and delay sums](assets/steps/04-topo-delays.png)

---

## A cycle fails levelize
![A cycle fails levelize](assets/steps/05-cycle-reject.png)

---

## Browser lab track
- In the browser lab, open **timing-graph**
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

