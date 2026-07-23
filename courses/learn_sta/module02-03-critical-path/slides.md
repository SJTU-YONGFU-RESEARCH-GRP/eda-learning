---
marp: true
title: Critical path
paginate: true
---

# Critical path

When slack is bad, or even when it is good, you still need the path

---

## Goldens to remember
- Critical path has six pins
- Path delay equals A(out)=3.2
- Always match A(u)+d to A(v)
- Keep these numbers handy, the browser challenges and Track A tests use the same instance

---

## Pseudocode
- Critical path pseudocode walks backward from the sink
- Breaking ties toward larger arrival
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- The golden path is six pins from in through both cells to out
- Path delay must equal arrival at out, three point two on this instance

---

## Algorithm sketch — try these

```
INPUT: G, A[], sink
OUTPUT: pin path (source→…→sink)
path←[sink]; cur←sink
while cur has preds:
  pick u→cur with A[u]+delay == A[cur]
  (tie-break: largest A[u])
  prepend u; cur←u
return path
GOLDEN: in→u1/A→u1/Y→u2/A→u2/Y→out
```

---

## Start from the worst endpoint
![Start from the worst endpoint](assets/steps/01-worst-sink.png)

---

## Step to the matching predecessor
![Step to the matching predecessor](assets/steps/02-match-pred.png)

---

## The full golden path
![The full golden path](assets/steps/03-full-path.png)

---

## Fix the path, not a random gate
![Fix the path, not a random gate](assets/steps/04-why-it-matters.png)

---

## Slack and path travel together
![Slack and path travel together](assets/steps/05-slack-path.png)

---

## Browser lab track
- In the browser lab, open **critical-path**
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

