---
marp: true
title: Why a routing graph
paginate: true
---

# Why a routing graph

Global routers do not hop pixel by pixel

---

## The idea
- To the upper neighbor when j plus one is less than ny
- On four by two you get eleven edges
- Store each edge as a sorted pair of GCell indices so direction does not matter

---

## GCell graph
![GCell graph](assets/steps/01-grid.png)

---

## Horizontal edges
![Horizontal edges](assets/steps/02-h.png)

---

## Vertical edges
![Vertical edges](assets/steps/03-v.png)

---

## Neighbors
![Neighbors](assets/steps/04-neigh.png)

---

## Capacity
![Capacity](assets/steps/05-cap.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `edge_list(nx, ny)` in `common/grutil.py`
- Print all edges for the tiny instance
- Verify ((0,0),(1,0)) is present and diagonals are absent

---

## Pitfalls
- Counting tile interiors instead of adjacency channels
- Double-counting undirected edges as two directed arcs without collapsing
- Forgetting top and right boundary checks

---

## Your turn
- Finish the checklist
- Sketch the eleven edges from memory
- Next: map pin placements to terminal GCells

