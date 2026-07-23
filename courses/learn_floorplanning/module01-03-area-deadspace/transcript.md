# Area, packing density, whitespace/deadspace

**Module id:** module01-03-area-deadspace
**Lab:** area-deadspace
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Area, packing density, whitespace/deadspace

With a legal packing in hand, score the whitespace. Module areas sum to twenty-three; the outline is eighty; deadspace is fifty-seven; density is zero point two eight seven five.


## Slide 2 — Pseudocode

Deadspace pseudocode is arithmetic after legality. Sum module areas, subtract from outline area, and divide for density.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 3 — Algorithm sketch

On the golden packing area is twenty-three, outline eighty, deadspace fifty-seven, density about zero point two eight seven five. Do not celebrate density on illegal packs.

```text
INPUT: outline W×H, modules areas
OUTPUT: area_sum, deadspace, density
area_sum ← Σ w[m]·h[m]
deadspace ← W·H − area_sum
density ← area_sum / (W·H)
only report density on legal packs
GOLDEN: area=23; outline=80; dead=57
density=0.2875
```


<!-- algorithm-walkthrough -->

## Slide 4 — Module areas sum to 23

![Module areas sum to 23](assets/steps/01-areas.png)

Add the five module areas: A is six, B is six, C is four, D is three, E is four. That is twenty-three units of silicon that must fit in the outline.

## Slide 5 — Outline area is 80

![Outline area is 80](assets/steps/02-outline-area.png)

Ten times eight is eighty. That is the budget. Module area twenty-three leaves whitespace—deadspace—equal to fifty-seven.

## Slide 6 — Density is 0.2875

![Density is 0.2875](assets/steps/03-density.png)

Density is module area over outline area: twenty-three over eighty equals zero point two eight seven five. Whitespace fraction is zero point seven one two five.

## Slide 7 — Metrics need a legal pack

![Metrics need a legal pack](assets/steps/04-legal-metrics.png)

On the golden legal packing these numbers are honest. On an overflow packing the area math still computes, but the floorplan is invalid—do not celebrate density on illegal layouts.

## Slide 8 — Report area trio every time

![Report area trio every time](assets/steps/05-takeaway.png)

Habit: print module area, outline area, deadspace, and density with every packing. Representations later change geometry; this trio stays the scoreboard.

<!-- /algorithm-walkthrough -->


## Slide 9 — Browser lab track

Open area-deadspace, load the golden packing, and read the metrics panel: module area twenty-three, outline eighty, deadspace fifty-seven, density zero point two eight seven five.

## Slide 10 — Implement track

Implement moduleAreaSum, outlineArea, deadspace, and density. Assert deadspace equals eighty minus twenty-three on the starter modules—independent of placement when sizes are fixed.

## Slide 11 — Pitfalls

Reporting density on an illegal pack; mixing outline area with bounding-box area; forgetting soft A still contributes area six at three by two.

## Slide 12 — Your turn

Print the area trio on every run. Next lab builds a slicing polish whose bounding box is nine by three inside this outline.
