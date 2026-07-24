---
marp: true
title: Layer changes at bends
paginate: true
---

# Layer changes at bends

Real detailed routes switch between M1 and M2 at vias

---

## The idea
- Given start and goal
- L_route_layers returns segment dicts with x y layer and optional via flag
- A path from one comma one to five comma four in HV includes at least one via

---

## L-bend via
![L-bend via](assets/steps/01-bend.png)

---

## A–C example
![A–C example](assets/steps/02-ab.png)

---

## Canvas vias
![Canvas vias](assets/steps/03-draw.png)

---

## Multi-pin
![Multi-pin](assets/steps/04-multi.png)

---

## Spacing next
![Spacing next](assets/steps/05-drc.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `l_route_layers(a, b, prefer)`
- Route net A–B on tiny_dr and print segments with via flags
- Match the browser overlay

---

## Pitfalls
- Skipping the via marker at the bend
- Putting horizontal motion on M2 or vertical on M1
- Forgetting the final segment must land on the goal coordinates

---

## Your turn
- Ship Track A layer routes with vias
- Next: DRC spacing lite on parallel tracks

