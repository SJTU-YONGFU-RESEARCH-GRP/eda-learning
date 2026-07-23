---
marp: true
title: Boundary pins
paginate: true
---

# Boundary pins

Chips talk to the outside world through I/O pins on the outline edges, north, east, south, west

---

## The idea
- Each pin gets an edge and a position along that edge
- Modules that connect to a pin prefer shorter Manhattan stubs toward that side
- You can score a packing with a simple pin-to-module wirelength proxy
- Fixed outline still governs module legality

---

## Browser lab track
- Open **pin-assignment**
- Place a few pins on the four edges
- Connect them to modules A–E with a toy netlist
- Watch the wirelength proxy as you move pins or modules
- Then implement edge assignment and scoring in Track A

---

## Implement track
- Add a pin list: id, side, offset
- Assign sides for a handful of I/Os
- Score sum of distances from module centers (or abutment points) to pin locations
- Keep modules legal under the outline while you tweak assignments
- Print the assignment table and score

---

## Pitfalls
- Putting pins inside the outline instead of on the boundary breaks the model
- Crowding every pin onto one edge creates congestion you won’t see if you only watch
- Don’t forget that pin order on an edge can matter for packaging, even on a toy

---

## Your turn
- Assign boundary pins and report a wirelength proxy beside deadspace
- Then continue to offline compare, and finally the wrap

