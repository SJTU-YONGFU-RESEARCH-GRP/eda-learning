---
marp: true
title: Supply and load
paginate: true
---

# Supply and load

A GCell has a routing budget, capacity

---

## The idea
- Surplus equals demand minus capacity
- Positive surplus means overflow
- List oversubscribed tiles before you trust a heat map
- Capacity can later become anisotropic edge capacities

---

## Capacity budget
![Capacity budget](assets/steps/01-cap.png)

---

## Demand arrives
![Demand arrives](assets/steps/02-demand.png)

---

## Oversubscribed tiles
![Oversubscribed tiles](assets/steps/03-flag.png)

---

## Lower Cap
![Lower Cap](assets/steps/04-toggle.png)

---

## Spread helps
![Spread helps](assets/steps/05-spread.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Given a demand matrix from RUDY (or a hand-filled stub)
- Print both for capacity equals two and capacity equals one
- Keep the API ready for the overflow-metrics lab

---

## Pitfalls
- Comparing demand to capacity without documenting units
- Treating zero demand as “healthy” while ignoring that neighboring tiles may be hot
- Changing capacity mid-challenge without resetting the starter placement

---

## Your turn
- Complete Track A or B
- Next: RUDY, the classic demand estimator that fills those tiles from net bounding boxes

