---
marp: true
title: Slack, setup, and hold
paginate: true
---

# Slack, setup, and hold

Slack turns tags into a pass or fail

---

## Goldens to remember
- Setup: R−A = 10−3.2 = 6.8
- Hold lite: A−0 = 3.2
- Positive means the check passes
- Keep these numbers handy, the browser challenges and Track A tests use the same instance
- <!-- algorithm-walkthrough -->

---

## Setup slack is required minus arrival
![Setup slack is required minus arrival](assets/steps/01-setup-formula.png)

---

## Hold slack uses a different required
![Hold slack uses a different required](assets/steps/02-hold-formula.png)

---

## The sign tells you pass or fail
![The sign tells you pass or fail](assets/steps/03-sign-matters.png)

---

## Report slack at endpoints first
![Report slack at endpoints first](assets/steps/04-endpoint-habit.png)

---

## Period changes setup, not hold lite
![Period changes setup, not hold lite](assets/steps/05-period-knob.png)

---

## Browser lab track
- In the browser lab, open **slack-setup-hold**
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

