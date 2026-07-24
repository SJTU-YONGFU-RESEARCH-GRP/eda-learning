---
marp: true
title: Uniform wire density
paginate: true
---

# Uniform wire density

RUDY, Rectangular Uniform wire DensitY, spreads each net’s wirelength evenly across GCells under its bounding box

---

## The idea
- For each net, take the axis-aligned bbox of pin positions
- Half-perimeter wirelength is width plus height
- Collect overlapping GCells, at least one
- Density equals HPWL divided by the tile count
- Add that density into every overlapping tile
- Sum across nets for the demand map

---

## Net bounding box
![Net bounding box](assets/steps/01-bbox.png)

---

## Uniform share
![Uniform share](assets/steps/02-share.png)

---

## Sum over nets
![Sum over nets](assets/steps/03-sum.png)

---

## Overflow appears
![Overflow appears](assets/steps/04-overflow.png)

---

## Spread cools total pattern
![Spread cools total pattern](assets/steps/05-spread.png)

---

## Browser lab track
![Browser lab starter](assets/lab-starter.png)

---

## Implement track
- Implement `rudy_demand(positions)` in `common/solvers.py`
- On `congested_seed`
- Match the browser golden within a small rounding tolerance

---

## Pitfalls
- Dividing by bbox area in continuous units while depositing into discrete tiles
- Skipping nets with coincident pins, still touch one GCell
- Mutating the demand matrix in place across calls without zeroing

---

## Your turn
- Ship Track A RUDY and clear the browser challenges
- Next: probabilistic L-shapes for a different demand signature

