---
marp: true
title: Pull soft from hotspots
paginate: true
---

# Pull soft from hotspots

Net weighting raises the cost of nets that cross congested GCells so a weighted placer pulls those pins apart

---

## The idea
- For each net, average congestion over GCells under its bbox
- Scale with beta, one point zero is a clear demo
- The four-pin net on a clustered seed should outrank the short E–F net

---

## Weight hot nets
![Weight hot nets](assets/steps/01-idea.png)

---

## Mean under bbox
![Mean under bbox](assets/steps/02-bbox.png)

---

## 4-pin ranks high
![4-pin ranks high](assets/steps/03-rank.png)

---

## Spread lowers weights
![Spread lowers weights](assets/steps/04-cool.png)

---

## Use in placer
![Use in placer](assets/steps/05-use.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `net_weights_from_congestion`
- Print the six weights for congested_seed
- Confirm net index four is among the highest

---

## Pitfalls
- Averaging over the whole chip instead of the net bbox
- Using demand instead of congestion ratios
- Updating weights but forgetting the placer still optimizes unweighted HPWL in the toy lab

---

## Your turn
- Finish weighting
- Next: one full placement feedback pass

