---
marp: true
title: When usage exceeds capacity
paginate: true
---

# When usage exceeds capacity

Each GCell edge has capacity two on tiny_gr

---

## The idea
- For each edge e, overflow e equals max of zero and usage e minus capacity
- Total is the sum across edges
- Max is the worst edge
- Count is how many edges have positive overflow
- Sequential L-HV on all six nets should yield positive total overflow at cap two

---

## Overflow
![Overflow](assets/steps/01-def.png)

---

## Total overflow
![Total overflow](assets/steps/02-total.png)

---

## Max overflow
![Max overflow](assets/steps/03-max.png)

---

## Overflow count
![Overflow count](assets/steps/04-count.png)

---

## Hit targets
![Hit targets](assets/steps/05-target.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `edge_overflow(usage, capacity)`
- Call route_nets with mode l_hv on tiny_gr and assert total overflow is greater than zero

---

## Pitfalls
- Computing overflow before summing all nets
- Using tile demand from congestion instead of edge usage
- Reporting negative overflow values

---

## Your turn
- Hit overflow targets
- Next: rip-up the hottest net and maze reroute

