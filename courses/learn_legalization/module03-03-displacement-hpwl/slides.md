---
marp: true
title: Displacement versus HPWL
paginate: true
---

# Displacement versus HPWL

Legalization cost combines HPWL and displacement

---

## The idea
- Lambda one gives cost forty-two
- Higher lambda favors staying near global placement even when wirelength could be slightly
- <!-- algorithm-walkthrough -->

---

## Cost = HPWL + λ · displacement
![Cost = HPWL + λ · displacement](assets/steps/01-cost-formula.png)

---

## Abacus vs overlap origin
![Abacus vs overlap origin](assets/steps/02-abacus-metrics.png)

---

## λ = 1 → cost 42
![λ = 1 → cost 42](assets/steps/03-lambda-1.png)

---

## λ = 5 → cost 58
![λ = 5 → cost 58](assets/steps/04-lambda-5.png)

---

## Higher λ favors staying put
![Higher λ favors staying put](assets/steps/05-lambda-tradeoff.png)

---

## Browser lab track
- In the browser lab track, open the **displacement-hpwl** lab from the tools shelf
- Load the overlap or float starter, run the legalizer once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track, open this module's examples and the course `common/` solvers
- Parse `tiny_legal.json`, run the algorithm with deterministic coordinates
- Match the browser goldens before you claim the checklist

---

## Pitfalls
- Common traps

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the starter goldens
- When you're ready, take the short quiz, then continue to the next module

