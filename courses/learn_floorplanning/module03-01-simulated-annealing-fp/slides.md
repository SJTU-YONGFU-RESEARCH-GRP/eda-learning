---
marp: true
title: Simulated annealing floorplan search
paginate: true
---

# Simulated annealing floorplan search

Toy cost adds one thousand when a packing is illegal

---

## Pseudocode
- Floorplan annealing uses a cost that heavily penalizes illegality
- Pseudocode proposes neighbors, accepts by Metropolis, and keeps the best legal iterate
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Bad overflow seed costs about one thousand forty-four
- Golden legal packing is about thirty-six
- One teaching improve step replaces bad with golden

---

## Algorithm sketch — try these

```
INPUT: pack / representation, T schedule
OUTPUT: best legal low-cost pack
cost ← 1000·¬legal + deadspace + α·HPWL
propose neighbor (swap/move/perturb)
accept if Δ<0 or rand < e^(−Δ/T)
keep best; cool T
GOLDEN legal cost≈36; bad≈1044
```

---

## Illegal packs pay 1000
![Illegal packs pay 1000](assets/steps/01-bad-cost.png)

---

## Golden cost stays under 1000
![Golden cost stays under 1000](assets/steps/02-golden-cost.png)

---

## Neighbors swap module positions
![Neighbors swap module positions](assets/steps/03-neighbor.png)

---

## Improve: bad → golden
![Improve: bad → golden](assets/steps/04-improve.png)

---

## SA needs a representation
![SA needs a representation](assets/steps/05-takeaway.png)

---

## Browser lab track
- Open simulated-annealing-fp
- Show bad, note cost at least one thousand
- Show golden or Improve, cost drops below one thousand and legality becomes true

---

## Implement track
- Implement cost with an illegality penalty, plus deadspace and HPWL terms
- Assert cost(golden) is less than cost(bad), and saSwap only exchanges coordinates

---

## Pitfalls
- Accepting illegal states without penalty

---

## Your turn
- Demonstrate one improve step from bad to golden
- Next: soft module A reshaped from three by two to two by three

