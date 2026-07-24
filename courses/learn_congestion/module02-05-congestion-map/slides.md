---
marp: true
title: Demand over capacity
paginate: true
---

# Demand over capacity

Congestion is a ratio: demand divided by capacity

---

## The idea
- Cong[i][j] equals demand[i][j] over Cap
- Values above one are oversubscribed
- The hottest GCell is the argmax
- On the congested seed, expect the center columns to light up first

---

## Demand / Cap
![Demand / Cap](assets/steps/01-ratio.png)

---

## Hottest tile
![Hottest tile](assets/steps/02-hot.png)

---

## Read the colors
![Read the colors](assets/steps/03-legend.png)

---

## Move the hotspot
![Move the hotspot](assets/steps/04-move.png)

---

## Cooler map
![Cooler map](assets/steps/05-spread.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Build `congestion_map(demand, capacity)` returning the ratio matrix and hottest index
- Print hottest for both placement seeds

---

## Pitfalls
- Dividing by zero capacity
- Pick a fixed scan order

---

## Your turn
- Finish the lab
- Next: overflow metrics compress the map into totals you can regress

