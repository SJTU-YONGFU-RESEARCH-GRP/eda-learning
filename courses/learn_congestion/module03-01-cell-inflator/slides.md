---
marp: true
title: Make hot cells larger
paginate: true
---

# Make hot cells larger

Inflators tell the placer that cells in congested GCells should act bigger, encouraging spreading on the next pass

---

## The idea
- Map each cell center to a GCell
- If that tile’s congestion exceeds one, inflate; otherwise leave width alone
- Alpha around zero point five keeps the demo visible without exploding geometry
- Coordinates stay put, this lab changes widths, not x y

---

## Why inflate
![Why inflate](assets/steps/01-idea.png)

---

## Scale rule
![Scale rule](assets/steps/02-rule.png)

---

## Apply once
![Apply once](assets/steps/03-run.png)

---

## Quiet tiles
![Quiet tiles](assets/steps/04-quiet.png)

---

## Link to place
![Link to place](assets/steps/05-link.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `inflate_cells` with alpha equals zero point five
- Print before/after widths for cells sitting in oversubscribed tiles

---

## Pitfalls
- Inflating every cell when only some GCells are hot
- Inflating height when the placer model only tracks width
- Applying inflation twice without resetting to base widths

---

## Your turn
- Clear the inflator challenges
- Next: net weighting, the wirelength-side knob

