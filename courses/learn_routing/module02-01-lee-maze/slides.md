---
marp: true
title: Cell paths before layers
paginate: true
---

# Cell paths before layers

Lee maze finds a shortest path on grid cells ignoring track congestion

---

## The idea
- Seed a BFS queue with start and path list
- Pop, expand neighbors4 skipping blocked cells, return the first path that reaches the goal
- If the queue empties, return None
- Shortest cell hop count wins

---

## Breadth-first
![Breadth-first](assets/steps/01-bfs.png)

---

## Around macro
![Around macro](assets/steps/02-detour.png)

---

## Route Lee
![Route Lee](assets/steps/03-lee.png)

---

## vs layered
![vs layered](assets/steps/04-compare.png)

---

## When to maze
![When to maze](assets/steps/05-use.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `lee_maze(start, goal, blocked, nx, ny)`
- Block cells inside five comma two two by two and show the path avoids them
- Match the browser overlay

---

## Pitfalls
- Treating blockages as track usage instead of forbidden cells
- Forgetting BFS needs visited on cells not edges
- Returning a path through a blocked cell because neighbor checks were skipped

---

## Your turn
- Pass Lee maze goldens
- Next: A* routing that respects track capacity

