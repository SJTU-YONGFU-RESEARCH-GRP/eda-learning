---
marp: true
title: Numbers that regress
paginate: true
---

# Numbers that regress

Overflow is demand above capacity

---

## The idea
- Ov equals max of zero and demand minus Cap, per tile
- Total is the sum
- Max is the worst tile
- Count is how many tiles have positive overflow
- Report all three every time you change placement

---

## Define overflow
![Define overflow](assets/steps/01-def.png)

---

## Total overflow
![Total overflow](assets/steps/02-total.png)

---

## Max overflow
![Max overflow](assets/steps/03-max.png)

---

## Congested count
![Congested count](assets/steps/04-count.png)

---

## Hit a target
![Hit a target](assets/steps/05-target.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `overflow_metrics`
- Assert congested_seed has higher total overflow than spread placement at Cap equals two
- Print the triple (total, max, count)

---

## Pitfalls
- Reporting negative “overflow.” Counting tiles with congestion greater than one while
- Comparing totals across estimators with incompatible demand units

---

## Your turn
- Hit the overflow targets
- Next: cell inflation, the first feedback knob

