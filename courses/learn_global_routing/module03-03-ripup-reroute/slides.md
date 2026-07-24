---
marp: true
title: Relieve hotspots
paginate: true
---

# Relieve hotspots

When overflow appears, global routers rip up contributing nets and reroute around congested edges

---

## The idea
- Score each net by overflow on its edges
- Subtract its route from usage
- Run maze_route between its pins with the remaining usage map
- Add the new edges back
- Total overflow should not rise; ideally it drops versus the pre-rip state

---

## Sequential L first
![Sequential L first](assets/steps/01-seq.png)

---

## Pick hot edge
![Pick hot edge](assets/steps/02-pick.png)

---

## Rip nets
![Rip nets](assets/steps/03-rip.png)

---

## Maze reroute
![Maze reroute](assets/steps/04-maze-r.png)

---

## Iterate
![Iterate](assets/steps/05-loop.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `ripup_reroute(routes, usage, capacity, nets, term, nx, ny)`
- Assert total overflow after is less than or equal to before on tiny_gr sequential L seed

---

## Pitfalls
- Ripping a net but leaving ghost usage on its old edges
- Rerouting with pattern L through the same hot edge
- Picking the wrong net to rip, use overflow contribution not HPWL

---

## Your turn
- Clear rip-up challenges
- Next: tie it together with full sequential global routing

