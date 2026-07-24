---
marp: true
title: When usage exceeds capacity
paginate: true
---

# When usage exceeds capacity

Each directed M1 or M2 track has capacity one on tiny_dr

---

## The idea
- Path_track_usage walks consecutive segment pairs
- Track_overflow computes max of zero and usage minus capacity per track
- Sequential L-HV on all six nets should yield positive total overflow at cap one

---

## Usage heat
![Usage heat](assets/steps/01-def.png)

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
- Implement `path_track_usage` and `track_overflow`
- Call sequential_detailed with mode l_hv on tiny_dr and assert total overflow is greater

---

## Pitfalls
- Computing overflow before summing all nets
- Using GCell edge usage from global routing instead of directed tracks
- Reporting negative overflow values

---

## Your turn
- Hit overflow targets
- Next: assign vias on two-layer L paths

