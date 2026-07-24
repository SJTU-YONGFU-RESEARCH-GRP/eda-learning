---
marp: true
title: Why GCells
paginate: true
---

# Why GCells

After legalization you have legal cell sites, but routers still think in coarser tiles called GCells

---

## The idea
- Index with lower-left origin
- Column i is floor of x over cell width, clamped to zero through three
- Row j is floor of y over cell height, clamped to zero or one
- Cell A at one comma one lands in GCell zero comma zero
- Cell D at eight comma five lands in two comma one
- Memorize that mapping, every estimator reuses it

---

## Chip and GCells
![Chip and GCells](assets/steps/01-chip.png)

---

## A lands in (0,0)
![A lands in (0,0)](assets/steps/02-a00.png)

---

## D lands in (2,1)
![D lands in (2,1)](assets/steps/03-d21.png)

---

## Paint all centers
![Paint all centers](assets/steps/04-paint.png)

---

## Clustered seed
![Clustered seed](assets/steps/05-seed.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Parse `tiny_cong.json`
- Print nx, ny, cellW, cellH
- Write `cell_gcell(x, y)` returning (i, j)
- Assert A→(0,0) and D→(2,1) on the spread placement
- No demand yet, this module is pure geometry

---

## Pitfalls
- Using upper-left image coordinates instead of chip lower-left
- Forgetting to clamp points on the right or top edge into the last tile
- Mixing site columns from legalization with GCell columns, different grids

---

## Your turn
- Finish the checklist
- Be able to sketch the eight GCells from memory
- Next: capacity versus demand, the supply side of the map

