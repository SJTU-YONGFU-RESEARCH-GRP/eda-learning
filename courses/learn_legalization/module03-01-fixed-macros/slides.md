---
marp: true
title: Fixed macros
paginate: true
---

# Fixed macros

Macro D is locked at (8, 4) on the top row, width two blocks sites eight and nine

---

## The idea
- Fixed cells are placed first; occupied intervals block shelf and Abacus trials on that row
- Legality adds a macro check, any drift off the lock fails
- Movable cells must route around macro sites, not slide through them

---

## Pseudocode
- Macro legalization adds one precondition to the Abacus sketch: place locked cells first
- Their site intervals become obstacles for every later try-place on that row
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- The legality line in the sketch is new too
- On this instance Abacus still finishes legal with displacement four

---

## Algorithm sketch — try these

```
INPUT: positions, widths, fixed F (e.g. D@(8,4))
OUTPUT: legal pack; macros never move
place every f in F at locked (x,y)
run Abacus/Tetris on movables only
F intervals block try-place / left-pack
fail legality if any macro drifted
GOLDEN: D stays (8,4); Abacus disp=4; legal
```

---

## Macro D locked at (8, 4)
![Macro D locked at (8, 4)](assets/steps/01-d-locked.png)

---

## Abacus with fixed macros
![Abacus with fixed macros](assets/steps/02-abacus-fixed.png)

---

## D never moves
![D never moves](assets/steps/03-d-never-moves.png)

---

## Still legal, displacement 4
![Still legal, displacement 4](assets/steps/04-still-legal.png)

---

## Movables avoid macro sites
![Movables avoid macro sites](assets/steps/05-avoid-macro.png)

---

## Browser lab track
- In the browser lab track, open the **fixed-macros** lab from the tools shelf
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

