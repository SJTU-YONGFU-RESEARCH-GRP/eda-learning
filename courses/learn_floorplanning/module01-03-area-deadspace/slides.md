---
marp: true
title: Area, packing density, whitespace/deadspace
paginate: true
---

# Area, packing density, whitespace/deadspace

With a legal packing in hand, score the whitespace

---

## Pseudocode
- Deadspace pseudocode is arithmetic after legality
- Sum module areas, subtract from outline area, and divide for density
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- On the golden packing area is twenty-three
- Do not celebrate density on illegal packs

---

## Algorithm sketch — try these

```
INPUT: outline W×H, modules areas
OUTPUT: area_sum, deadspace, density
area_sum ← Σ w[m]·h[m]
deadspace ← W·H − area_sum
density ← area_sum / (W·H)
only report density on legal packs
GOLDEN: area=23; outline=80; dead=57
density=0.2875
```

---

## Module areas sum to 23
![Module areas sum to 23](assets/steps/01-areas.png)

---

## Outline area is 80
![Outline area is 80](assets/steps/02-outline-area.png)

---

## Density is 0.2875
![Density is 0.2875](assets/steps/03-density.png)

---

## Metrics need a legal pack
![Metrics need a legal pack](assets/steps/04-legal-metrics.png)

---

## Report area trio every time
![Report area trio every time](assets/steps/05-takeaway.png)

---

## Browser lab track
- Open area-deadspace, load the golden packing, and read the metrics panel

---

## Implement track
- Implement moduleAreaSum, outlineArea, deadspace, and density
- Assert deadspace equals eighty minus twenty-three on the starter modules

---

## Pitfalls
- Reporting density on an illegal pack

---

## Your turn
- Print the area trio on every run
- Next lab builds a slicing polish whose bounding box is nine by three inside this outline

