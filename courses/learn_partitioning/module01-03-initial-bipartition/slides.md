---
marp: true
title: Initial bipartition
paginate: true
---

# Initial bipartition

Refinement needs a legal starting cut

---

## The idea
- Random shuffles then splits by half
- Greedy prefers keeping heavy edges internal when it can
- Grow expands a frontier from a seed until the part hits its size budget
- All three must report cutsize and balance so you can compare seeds fairly

---

## Pseudocode
- Initial bipartition is three named constructors in pseudocode
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Grow from D yields DE versus ABC at cut three
- Random seed seven recovers the bad AE versus BCD cut of twelve
- Always print cutsize and balance before KL or FM

---

## Algorithm sketch — try these

```
INPUT: graph G, method ∈ {random,greedy,grow}
OUTPUT: legal side[v] ∈ {0,1}
random(seed): shuffle; split by half
greedy: keep heaviest edges internal when able
grow(seed): expand frontier until size budget
report cutsize + balance for every seed
GOLDEN: grow(D)→DE|ABC cut=3
random(7)→AE|BCD cut=12
```

---

## Need a legal starting split
![Need a legal starting split](assets/steps/01-empty.png)

---

## Random seed=1: lucky ABC|DE
![Random seed=1: lucky ABC|DE](assets/steps/02-random-lucky.png)

---

## Greedy initial: AB|CDE cut 5
![Greedy initial: AB|CDE cut 5](assets/steps/03-greedy.png)

---

## Grow from D: ABC|DE cut 3
![Grow from D: ABC|DE cut 3](assets/steps/04-grow-d.png)

---

## Seed quality sets the ceiling
![Seed quality sets the ceiling](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **initial-bipartition** lab from the tools shelf
- Load the starter graph, run the algorithm once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track
- Parse the tiny graph, run the algorithm with a deterministic seed
- Match the browser goldens before you claim the checklist

---

## Pitfalls
- Common traps
- For multilevel flows, verify coarsening before you blame the refiner

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the starter goldens
- When you’re ready, take the short quiz, then continue to the next module

