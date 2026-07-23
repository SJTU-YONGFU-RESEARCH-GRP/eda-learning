---
marp: true
title: Tetris row packing
paginate: true
---

# Tetris row packing

Tetris-lite assigns each cell to its nearest row, then left-packs like overlap removal

---

## The idea
- Tetris is simpler than Abacus but moves cells farther on this toy
- Contrast disp six versus Abacus disp four
- Trade simpler control flow against a tighter displacement budget and slightly higher HPWL
- <!-- algorithm-walkthrough -->

---

## Same overlap seed
![Same overlap seed](assets/steps/01-overlap-seed.png)

---

## Nearest row, then left pack
![Nearest row, then left pack](assets/steps/02-nearest-row.png)

---

## Result: disp 6, HPWL 32
![Result: disp 6, HPWL 32](assets/steps/03-tetris-result.png)

---

## Contrast Abacus disp 4
![Contrast Abacus disp 4](assets/steps/04-contrast-abacus.png)

---

## Tradeoff: simpler vs better displacement
![Tradeoff: simpler vs better displacement](assets/steps/05-tradeoff.png)

---

## Browser lab track
- In the browser lab track, open the **tetris-row-pack** lab from the tools shelf
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

