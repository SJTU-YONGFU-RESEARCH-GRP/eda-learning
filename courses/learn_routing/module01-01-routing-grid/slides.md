---
marp: true
title: Why a track graph
paginate: true
---

# Why a track graph

Detailed routers do not hop GCell to GCell

---

## The idea
- A directed M2 edge upward when y plus one is less than ny
- Canonical keys sort endpoints so left-to-right and bottom-to-top always win
- On twelve by eight you get eighty-eight M1 edges and eighty-four M2 edges

---

## 12×8 grid
![12×8 grid](assets/steps/01-grid.png)

---

## Two layers
![Two layers](assets/steps/02-layers.png)

---

## Blockage
![Blockage](assets/steps/03-block.png)

---

## Neighbors
![Neighbors](assets/steps/04-neigh.png)

---

## Capacity
![Capacity](assets/steps/05-cap.png)

---

## Browser lab track
- Open the **routing-grid** lab
- Toggle layer M1 and M2 overlays
- Highlight one horizontal track between columns one and two on row one
- Read the track list in the metrics panel and match the counts

---

## Implement track
- Inspect `h_edge`, `v_edge`, and `track_key` in `common/drutil.py`
- Print sample M1 and M2 keys for tiny_dr
- Verify diagonals are absent and layers match movement axis

---

## Pitfalls
- Counting grid points instead of directed tracks
- Treating M1 and M2 as interchangeable
- Forgetting blockages still occupy cells even if tracks exist between free neighbors

---

## Your turn
- Finish the checklist
- Sketch M1 on one row from memory
- Next: map pin placements to access points on the grid

