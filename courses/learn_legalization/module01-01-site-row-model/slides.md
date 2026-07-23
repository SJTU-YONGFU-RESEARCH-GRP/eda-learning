---
marp: true
title: Site and row model
paginate: true
---

# Site and row model

Legalization snaps cells to a discrete grid

---

## The idea
- Every cell sits on exactly one row with a lower-left coordinate aligned to site pitch one
- Width tells you how many consecutive sites the rectangle covers
- The golden packing is legal

---

## Pseudocode
- Pseudocode is the written sketch of the algorithm before you code it
- For this module the sketch is the site and row model itself
- Outputs are the rules every legal packing must obey
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- Read the sketch as a contract
- Every cell lower-left sits on a site and a row bottom
- Width tells how many consecutive sites the rectangle covers
- Our teaching chip is twelve by six with three rows

---

## Algorithm sketch — try these

```
INPUT: chip W×H, siteW, rowH, rows Y[], widths w[c]
OUTPUT: legal coordinate rules
for each cell c:
  x multiple of siteW; y in Y[]
  occupies [x, x+w[c]) × [y, y+rowH)
GOLDEN: W=12 H=6 siteW=1 rowH=2 Y={0,2,4}
widths A–D=2 E–F=1 (total 10 ≤ 12)
```

---

## Twelve-by-six chip, three rows
![Twelve-by-six chip, three rows](assets/steps/01-empty-chip.png)

---

## Cell widths A–D = 2, E–F = 1
![Cell widths A–D = 2, E–F = 1](assets/steps/02-cell-widths.png)

---

## Site pitch equals one
![Site pitch equals one](assets/steps/03-site-pitch.png)

---

## Golden legal packing
![Golden legal packing](assets/steps/04-golden-pack.png)

---

## Contrast: illegal overlap stack
![Contrast: illegal overlap stack](assets/steps/05-overlap-contrast.png)

---

## Browser lab track
- In the browser lab track, open the **site-row-model** lab from the tools shelf
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

