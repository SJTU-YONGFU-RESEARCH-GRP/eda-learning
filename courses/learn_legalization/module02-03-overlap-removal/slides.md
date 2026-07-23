---
marp: true
title: Overlap removal
paginate: true
---

# Overlap removal

Overlap removal snaps first, then left-packs each row without changing row assignment

---

## The idea
- Sort movables by x within each row and place left without overlap
- D, E, and F keep their seed roles on other rows
- This is the same shelf pack Tetris uses, simple, deterministic

---

## Pseudocode
- Overlap removal is a two-phase sketch: snap first, then pack each row
- Pseudocode makes the phases explicit so you do not merge them into one vague “fix
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Inside each row
- On the teaching seed that yields A at four

---

## Algorithm sketch — try these

```
INPUT: positions, widths, rows, fixed macros
OUTPUT: legal packing (if capacity allows)
snap all movables to sites/rows
for each row y:
  sort movables by x; left-pack (skip macros)
report legal?, disp, HPWL
GOLDEN: A@4 B@6 C@8 on y=2; disp=6; HPWL=32
```

---

## A, B, C stacked at (4, 2)
![A, B, C stacked at (4, 2)](assets/steps/01-overlap-seed.png)

---

## After snap: still stacked
![After snap: still stacked](assets/steps/02-after-snap.png)

---

## Per-row pack: A@4, B@6, C@8
![Per-row pack: A@4, B@6, C@8](assets/steps/03-row-pack.png)

---

## Legal: disp 6, HPWL 32
![Legal: disp 6, HPWL 32](assets/steps/04-legal-metrics.png)

---

## D, E, F unchanged
![D, E, F unchanged](assets/steps/05-unchanged.png)

---

## Browser lab track
- In the browser lab track, open the **overlap-removal** lab from the tools shelf
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

