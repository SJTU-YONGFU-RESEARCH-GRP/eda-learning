---
marp: true
title: Simulated annealing floorplan search
paginate: true
---

# Simulated annealing floorplan search

Toy cost adds one thousand when a packing is illegal

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

