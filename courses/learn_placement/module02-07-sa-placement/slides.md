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
- <!-- algorithm-walkthrough -->

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
- In the implement track, open this module’s examples and the course `common/` solvers
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

