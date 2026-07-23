---
marp: true
title: Boundary pin / I/O assignment
paginate: true
---

# Boundary pin / I/O assignment

Pins sit on outline edges

---

## Packing without pins
![Packing without pins](assets/steps/01-no-pins.png)

---

## Assign one pin per side
![Assign one pin per side](assets/steps/02-assign.png)

---

## Coverage makes pinsValid true
![Coverage makes pinsValid true](assets/steps/03-valid.png)

---

## Empty set is invalid
![Empty set is invalid](assets/steps/04-empty-bad.png)

---

## Pins feed place and route
![Pins feed place and route](assets/steps/05-takeaway.png)

---

## Browser lab track
- Open pin-assignment
- Assign golden pins, confirm four sides and valid true
- Clear pins and watch validity fail

---

## Implement track
- Implement pinsValid requiring all four sides and in-range offsets
- Assert golden pins pass and the empty list fails

---

## Pitfalls
- Putting pins inside modules

---

## Your turn
- Ship a valid four-side assignment
- Offline compare is next; then the wrap points to learn_placement

