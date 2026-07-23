---
marp: true
title: Soft module sizing
paginate: true
---

# Soft module sizing

Hard modules have fixed width and height

---

## The idea
- For soft module A with area a
- Re-pack after each sizing move
- On our starter, A is soft; B through E stay hard
- Deadspace uses the same formula

---

## Browser lab track
- Open **soft-module-sizing**
- Select module A, drag aspect within bounds
- Confirm area of A stays constant while density of the packing geometry changes
- Then implement aspect moves in Track A

---

## Implement track
- Extend your packer so A’s (w, h) can vary under aspect constraints at constant area
- Combine with a simple search, even greedy aspect tries help
- Report legality and deadspace before and after
- Reject sizes outside aspect bounds

---

## Pitfalls
- Using aspect limits on w/h but updating only w without fixing h = area/w breaks the area
- Allowing zero width is nonsense, enforce positive sizes
- Soft sizing cannot fix an area budget that already exceeds the outline

---

## Your turn
- Improve a legal packing by resizing A within bounds
- Next: hard macros that refuse to move or resize

