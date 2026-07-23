---
marp: true
title: Detailed versus global legalize
paginate: true
---

# Detailed versus global legalize

Global legalize lite maps to Tetris shelf pack, displacement six, HPWL thirty-two

---

## The idea
- Pick global Tetris when you want a fast pass and can afford extra movement
- Pick detailed Abacus when displacement budget is tight
- Report both pipelines side by side in regressions, legal first, then disp and HPWL

---

## Pseudocode
- Here the sketch is two named pipelines on the same seed
- Global legalize lite means Tetris
- Detailed legalize lite means Abacus
- Pseudocode names both so regressions do not mix the labels
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Both pipelines must end legal
- Then compare displacement six versus four and HPWL thirty-two versus thirty-eight
- Pick detailed when movement budget is tight; pick global when speed matters more

---

## Algorithm sketch — try these

```
INPUT: illegal / global positions
global:   TetrisLite → disp=6 HPWL=32
detailed: AbacusLite → disp=4 HPWL=38
both must report legal=true
CHOOSE detailed when disp budget is tight
CHOOSE global when a fast shelf pack is enough
```

---

## Global = Tetris, disp 6
![Global = Tetris, disp 6](assets/steps/01-global-tetris.png)

---

## Detailed = Abacus, disp 4
![Detailed = Abacus, disp 4](assets/steps/02-detailed-abacus.png)

---

## Both pipelines legal
![Both pipelines legal](assets/steps/03-both-legal.png)

---

## Side-by-side metrics
![Side-by-side metrics](assets/steps/04-side-by-side.png)

---

## Pick detailed when displacement is tight
![Pick detailed when displacement is tight](assets/steps/05-pick-detailed.png)

---

## Browser lab track
- In the browser lab track, open the **detailed-vs-global** lab from the tools shelf
- Open the interactive lab
- Reveal golden is study-only
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track
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

