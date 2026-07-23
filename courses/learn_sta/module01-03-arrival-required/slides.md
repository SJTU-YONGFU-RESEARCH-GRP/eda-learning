---
marp: true
title: Arrival and required times
paginate: true
---

# Arrival and required times

Once the graph is levelized, you propagate tags

---

## Goldens to remember
- Forward: A(in)=0, A(u1/Y)=1.2, A(out)=3.2
- Backward setup: R(out)=10, R(in)=6.8
- Keep these numbers handy, the browser challenges and Track A tests use the same instance

---

## Pseudocode
- Arrival and required need two written passes
- Forward topo takes a max over predecessors for arrival
- Reverse topo takes a min over successors for setup required from the period at sinks
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Goldens on the chain
- Arrival is latest; required is earliest

---

## Algorithm sketch — try these

```
INPUT: DAG G, period, arrival seeds
OUTPUT: A[], R_setup[]
for p in topo(G):
  A[p]← max over u→p of A[u]+delay   (sources: seed/0)
for sinks: R[p]←period×cycles
for p in reverse_topo:
  R[p]← min over p→v of R[v]−delay
GOLDEN: A[out]=3.2; R[out]=10; R[in]=6.8
```

---

## Seed arrival at the source
![Seed arrival at the source](assets/steps/01-seed-arrival.png)

---

## Propagate arrival forward
![Propagate arrival forward](assets/steps/02-forward-wave.png)

---

## Seed required at the sink
![Seed required at the sink](assets/steps/03-seed-required.png)

---

## Propagate required backward
![Propagate required backward](assets/steps/04-backward-wave.png)

---

## Keep both tags on every pin
![Keep both tags on every pin](assets/steps/05-both-tags.png)

---

## Browser lab track
- In the browser lab, open **arrival-required**
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

