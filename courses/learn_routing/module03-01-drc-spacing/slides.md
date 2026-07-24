---
marp: true
title: Geometry rules matter
paginate: true
---

# Geometry rules matter

Signoff DRC is vast; spacing lite teaches the idea

---

## The idea
- Group segment points by layer
- For M1 pairs on the same row y
- Likewise for M2 pairs on the same column x
- Otherwise pass

---

## Lite checker
![Lite checker](assets/steps/01-lite.png)

---

## Spread pass
![Spread pass](assets/steps/02-pass.png)

---

## Violation demo
![Violation demo](assets/steps/03-fail.png)

---

## After route
![After route](assets/steps/04-route.png)

---

## Real DRC
![Real DRC](assets/steps/05-real.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `drc_spacing_lite(segments, min_dist)`
- Feed the golden failing segment set from test_solvers and assert pass is false

---

## Pitfalls
- Checking cross-layer pairs, this lite rule is same-layer only
- Using Manhattan grid distance across rows for M1 horizontal segments
- Treating DRC pass as proof of tape-out readiness

---

## Your turn
- Clear DRC spacing challenges
- Next: rip-up the hottest net and A* reroute

