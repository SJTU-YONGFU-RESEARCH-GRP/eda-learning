---
marp: true
title: Order matters on tracks
paginate: true
---

# Order matters on tracks

Production detailed routers process nets in an order

---

## The idea
- Initialize empty usage
- Increment usage on every track key in the route
- Report final usage and track_overflow summary

---

## Net order
![Net order](assets/steps/01-order.png)

---

## Layered pass
![Layered pass](assets/steps/02-layer-all.png)

---

## Lee pass
![Lee pass](assets/steps/03-lee-all.png)

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
- Implement `sequential_detailed` and `route_from_data`
- Print usage and overflow after routing all six nets
- Compare astar mode with l_hv on total overflow

---

## Pitfalls
- Parallel deposit without order, hides rip-up motivation
- Ignoring multi-pin net in order list
- Resetting usage between nets accidentally

---

## Your turn
- Complete sequential detailed routing
- Offline compare and wrap come next

