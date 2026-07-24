---
marp: true
title: Pins need grid access
paginate: true
---

# Pins need grid access

A detailed route starts and ends at grid access points, integer cells the router can reach

---

## The idea
- Pin_grid of x y returns column gx equals round of x clamped zero to nx minus one
- Cell A at one comma one maps to one comma one
- Cell E at five comma three sits near the blockage at five comma two

---

## Pin → grid
![Pin → grid](assets/steps/01-map.png)

---

## A → (1,1)
![A → (1,1)](assets/steps/02-a11.png)

---

## D → (8,5)
![D → (8,5)](assets/steps/03-d85.png)

---

## Blocked pins
![Blocked pins](assets/steps/04-nudge.png)

---

## Routes from pins
![Routes from pins](assets/steps/05-route.png)

---

## Browser lab track
- Open **pin-access**
- Hover each cell and read its access grid point
- Move a pin across the blockage boundary and watch the access index shift
- Confirm all six cells on tiny_dr match your Track A printout

---

## Implement track
- Implement or call `terminals(positions, data)` in `common/drutil.py`
- Assert A through F on spread placement
- Print access points before any routing lab

---

## Pitfalls
- Using GCell floor divide from global routing instead of per-grid rounding
- Off-by-one at the chip edge without clamp
- Ignoring blockages when assigning access

---

## Your turn
- Complete access points for all six cells
- Next: Lee maze routing around the central blockage

