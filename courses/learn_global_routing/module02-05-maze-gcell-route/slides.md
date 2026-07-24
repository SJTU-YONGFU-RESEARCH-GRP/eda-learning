---
marp: true
title: Routes that detour
paginate: true
---

# Routes that detour

Pattern routers ignore blocked channels

---

## The idea
- Seed a queue with start and path list
- Pop, expand neighbors, skip edges with usage greater than or equal to capacity
- First time you dequeue the goal, return the path
- If the queue empties, return None
- Shortest feasible path wins

---

## Edge cost
![Edge cost](assets/steps/01-cost.png)

---

## L overflow
![L overflow](assets/steps/02-l-ov.png)

---

## Route maze
![Route maze](assets/steps/03-maze.png)

---

## Compare totals
![Compare totals](assets/steps/04-compare.png)

---

## When to maze
![When to maze](assets/steps/05-use.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `maze_route(a, b, usage, capacity, nx, ny)`
- Block edge ((0,0),(1,0)) at cap two and show maze cannot go direct

---

## Pitfalls
- Treating usage as per-tile instead of per-edge
- Forgetting BFS needs visited set on GCells not edges
- Returning a path through a full edge because you checked the wrong direction key

---

## Your turn
- Pass maze goldens
- Next: connect more than two pins with a star tree

