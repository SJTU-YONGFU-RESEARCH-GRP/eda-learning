---
marp: true
title: L-shape routes
paginate: true
---

# L-shape routes

RUDY paints the whole bbox

---

## The idea
- For a two-pin net
- Multi-pin nets: star from the bbox center to each pin and deposit like two-pin edges
- Compare the resulting matrix to RUDY on the same placement

---

## L-shape idea
![L-shape idea](assets/steps/01-lshape.png)

---

## Deposit along legs
![Deposit along legs](assets/steps/02-deposit.png)

---

## Multi-pin star
![Multi-pin star](assets/steps/03-multi.png)

---

## Versus RUDY
![Versus RUDY](assets/steps/04-compare.png)

---

## Spread again
![Spread again](assets/steps/05-cool.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `probabilistic_demand`
- On spread placement, print both RUDY and probabilistic totals
- Explain one tile where they disagree and why

---

## Pitfalls
- Double-counting the corner GCell on both L legs
- Forgetting multi-pin nets
- Document your unit choice

---

## Your turn
- Clear the checklist
- Next: turn demand into a congestion heat map

