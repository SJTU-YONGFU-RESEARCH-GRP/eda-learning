---
marp: true
title: Timing-driven placement
paginate: true
---

# Timing-driven placement

Timing-driven place weights critical nets in the wirelength objective

---

## The idea
- Multiply each net’s HPWL by its criticality weight and sum
- Heavy weights pull critical nets shorter even when plain HPWL looks fine
- Always report both plain and weighted totals so you can see what the objective actually

---

## Pseudocode
- Timing-driven place multiplies each net’s HPWL by criticality and sums
- Pseudocode always reports plain and weighted totals together
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Starter plain fifty-two becomes timing one hundred sixteen because the four-pin net has
- Compact golden drops timing cost to thirty

---

## Algorithm sketch — try these

```
INPUT: positions, nets, weights w[net]
OUTPUT: plain HPWL, timing HPWL
plain ← Σ HPWL(net)
timing ← Σ w[net]·HPWL(net)
optimize timing (or report both)
GOLDEN starter: plain=52 timing=116
compact: plain=14 timing=30
```

---

## Plain HPWL hides critical nets
![Plain HPWL hides critical nets](assets/steps/01-plain-vs-weighted.png)

---

## Weighted sum of net HPWLs
![Weighted sum of net HPWLs](assets/steps/02-weight-math.png)

---

## Golden timing cost drops to thirty
![Golden timing cost drops to thirty](assets/steps/03-golden-timing.png)

---

## Always quote plain and weighted
![Always quote plain and weighted](assets/steps/04-both-reports.png)

---

## Weights change what you optimize
![Weights change what you optimize](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **timing-driven-place** lab from the tools shelf
- Load the starter placement, run the algorithm once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track
- Parse `tiny_place.json`, run the algorithm with a deterministic seed
- Match the browser goldens before you claim the checklist

---

## Pitfalls
- Common traps

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the starter goldens
- When you’re ready, take the short quiz, then continue to the next module

