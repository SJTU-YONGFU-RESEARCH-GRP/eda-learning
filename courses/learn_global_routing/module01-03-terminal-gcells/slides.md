---
marp: true
title: Pins become terminals
paginate: true
---

# Pins become terminals

A global route starts and ends at GCell terminals, one tile per pin

---

## The idea
- Cell_gcell of x y returns column i equals floor of x over cell width clamped
- Cell A at one comma one maps to zero comma zero
- Cell D at eight comma five maps to two comma one
- Build a dictionary from cell id to GCell for every pin in the netlist

---

## Pin → GCell
![Pin → GCell](assets/steps/01-map.png)

---

## A → (0,0)
![A → (0,0)](assets/steps/02-a00.png)

---

## D → (2,1)
![D → (2,1)](assets/steps/03-d21.png)

---

## Routes on graph
![Routes on graph](assets/steps/04-route.png)

---

## Cluster seed
![Cluster seed](assets/steps/05-cluster.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `terminals(positions, data)` returning the map
- Assert A through F on spread placement
- Print terminals before any routing lab

---

## Pitfalls
- Using cell origin instead of pin center
- Off-by-one at the right or top chip edge without clamp
- Mixing site columns from legalization with GCell columns

---

## Your turn
- Complete terminals for all six cells
- Next: L-shape pattern routes between two terminals

