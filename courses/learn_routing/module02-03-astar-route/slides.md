---
marp: true
title: Congestion-aware search
paginate: true
---

# Congestion-aware search

Lee ignores other nets

---

## The idea
- Maintain open heap ordered by f equals g plus Manhattan distance to goal
- Expand four neighbors on M1 for horizontal steps and M2 for vertical
- Step cost is one plus ten times overflow penalty when usage meets capacity
- First time you pop the goal, return the path

---

## Track cost
![Track cost](assets/steps/01-cost.png)

---

## Layered overflow
![Layered overflow](assets/steps/02-l-ov.png)

---

## Route A*
![Route A*](assets/steps/03-astar.png)

---

## Compare totals
![Compare totals](assets/steps/04-compare.png)

---

## Move pins
![Move pins](assets/steps/05-move.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement or call `astar_route(start, goal, usage, cap, nx, ny, blocks)`
- Block the hot edge and show A* cannot go direct; unblock a vertical detour path exists

---

## Pitfalls
- Using undirected track keys inconsistently
- Checking capacity on the wrong layer for a move
- Forgetting blockages still forbid cells even when tracks are free

---

## Your turn
- Clear A* challenges
- Next: deposit segments on tracks and measure overflow

