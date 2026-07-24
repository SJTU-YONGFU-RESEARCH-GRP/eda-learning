---
marp: true
title: Order matters
paginate: true
---

# Order matters

Production global routers process nets in an order

---

## The idea
- Initialize empty usage
- Increment usage on every edge in the route
- Report final usage and edge_overflow summary

---

## Net order
![Net order](assets/steps/01-order.png)

---

## Pattern pass
![Pattern pass](assets/steps/02-l-all.png)

---

## Maze pass
![Maze pass](assets/steps/03-maze-all.png)

---

## Clear overflow
![Clear overflow](assets/steps/04-clear.png)

---

## Handoff
![Handoff](assets/steps/05-done.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `route_nets` and `route_nets_with_routes`
- Print usage and overflow after routing all six nets
- Compare with maze mode on total overflow

---

## Pitfalls
- Parallel deposit without order, hides rip-up motivation
- Ignoring multi-pin net in order list
- Resetting usage between nets accidentally

---

## Your turn
- Complete sequential global routing
- Offline compare and wrap come next

