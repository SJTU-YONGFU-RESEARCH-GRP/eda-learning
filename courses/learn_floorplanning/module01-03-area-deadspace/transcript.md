# Area, packing density, whitespace/deadspace

**Module id:** module01-03-area-deadspace
**Lab:** area-deadspace
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Area, packing density, whitespace/deadspace

With a legal packing in hand, score the whitespace. Module areas sum to twenty-three; the outline is eighty; deadspace is fifty-seven; density is zero point two eight seven five.

<!-- algorithm-walkthrough -->

## Slide 2 — Module areas sum to 23

![Module areas sum to 23](assets/steps/01-areas.png)

Add the five module areas: A is six, B is six, C is four, D is three, E is four. That is twenty-three units of silicon that must fit in the outline.

## Slide 3 — Outline area is 80

![Outline area is 80](assets/steps/02-outline-area.png)

Ten times eight is eighty. That is the budget. Module area twenty-three leaves whitespace—deadspace—equal to fifty-seven.

## Slide 4 — Density is 0.2875

![Density is 0.2875](assets/steps/03-density.png)

Density is module area over outline area: twenty-three over eighty equals zero point two eight seven five. Whitespace fraction is zero point seven one two five.

## Slide 5 — Metrics need a legal pack

![Metrics need a legal pack](assets/steps/04-legal-metrics.png)

On the golden legal packing these numbers are honest. On an overflow packing the area math still computes, but the floorplan is invalid—do not celebrate density on illegal layouts.

## Slide 6 — Report area trio every time

![Report area trio every time](assets/steps/05-takeaway.png)

Habit: print module area, outline area, deadspace, and density with every packing. Representations later change geometry; this trio stays the scoreboard.

<!-- /algorithm-walkthrough -->


## Slide 7 — Browser lab track

Open area-deadspace, load the golden packing, and read the metrics panel: module area twenty-three, outline eighty, deadspace fifty-seven, density zero point two eight seven five.

## Slide 8 — Implement track

Implement moduleAreaSum, outlineArea, deadspace, and density. Assert deadspace equals eighty minus twenty-three on the starter modules—independent of placement when sizes are fixed.

## Slide 9 — Pitfalls

Reporting density on an illegal pack; mixing outline area with bounding-box area; forgetting soft A still contributes area six at three by two.

## Slide 10 — Your turn

Print the area trio on every run. Next lab builds a slicing polish whose bounding box is nine by three inside this outline.
