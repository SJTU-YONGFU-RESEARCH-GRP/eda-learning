---
marp: true
title: Simulated annealing placement
paginate: true
---

# Simulated annealing placement

Simulated annealing jogs one cell at a time under an HPWL cost

---

## The idea
- Propose a small axis move, accept improvements always
- Keep the best iterate, not only the final temperature
- Fix the seed so your golden stays stable across runs

---

## Pseudocode
- Placement annealing jogs one cell per move under HPWL cost, accepts by Metropolis
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Seed forty-two with sixty moves yields best HPWL near forty-nine point six from fifty-two
- Lock the seed so goldens stay stable

---

## Algorithm sketch — try these

```
INPUT: positions, seed, moves, T0
OUTPUT: best positions + best HPWL
for i in 1..moves:
  jog one cell on one axis
  accept if ΔHPWL<0 or rand<e^(−Δ/T)
  keep best; cool T
GOLDEN seed=42, 60 moves → best≈49.6
accepted≈44 rejected≈16
```

---

## Anneal from HPWL fifty-two
![Anneal from HPWL fifty-two](assets/steps/01-starter-sa.png)

---

## Accept improvements; maybe worsenings
![Accept improvements; maybe worsenings](assets/steps/02-accept-reject.png)

---

## Best HPWL near forty-nine point six
![Best HPWL near forty-nine point six](assets/steps/03-best-not-final.png)

---

## Fix the seed for goldens
![Fix the seed for goldens](assets/steps/04-seed-lock.png)

---

## SA is a stochastic local search
![SA is a stochastic local search](assets/steps/05-takeaway.png)

---

## Browser lab track
- In the browser lab track, open the **sa-placement** lab from the tools shelf
- Load the starter placement, run the algorithm once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track
- Parse `tiny_place.json`, run the algorithm with a deterministic seed
- Match the browser goldens before you claim the checklist

---

## Pitfalls
- Common traps

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the starter goldens
- When you’re ready, take the short quiz, then continue to the next module

