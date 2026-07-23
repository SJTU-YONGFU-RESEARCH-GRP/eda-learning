# Soft module aspect sizing

**Module id:** module03-03-soft-module-sizing
**Lab:** soft-module-sizing
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Soft module aspect sizing

Soft module A keeps area six but may reshape between aspect one half and two. Reshape three by two into two by three, then pack legally—still area six.


## Slide 2 — Pseudocode

Soft sizing picks width and height for A under a fixed area and aspect bounds, then re-packs the hard modules around it.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 3 — Algorithm sketch

Hard golden keeps A at three by two. Soft teaching pack uses two by three. Area stays six; deadspace shape changes.

```text
INPUT: soft A area=6, aspect∈[0.5,2]
OUTPUT: (w,h) with w·h=area; pack rest
choose aspect; set w,h; re-pack / legalize
hard modules keep fixed w×h
GOLDEN hard A 3×2 vs soft A 2×3 pack
both area 6; whitespace shape differs
```


<!-- algorithm-walkthrough -->

## Slide 4 — A is soft with area 6

![A is soft with area 6](assets/steps/01-soft-a.png)

Module A is soft: area stays six, but aspect can move between one half and two. Hard modules B through E keep fixed shapes.

## Slide 5 — Reshape A to 2×3

![Reshape A to 2×3](assets/steps/02-reshape.png)

Reshape soft A to two by three—still area six. The soft packing moves neighbors so the outline stay legal.

## Slide 6 — Soft packing stays legal

![Soft packing stays legal](assets/steps/03-legal.png)

After reshape, the soft packing remains legal inside ten by eight. Softness is not a license to overflow—legality still gates acceptance.

## Slide 7 — Hard vs soft views

![Hard vs soft views](assets/steps/04-compare.png)

Compare the hard three-by-two golden with the soft two-by-three packing. Same area budget for A; different whitespace shape.

## Slide 8 — Softness is constrained freedom

![Softness is constrained freedom](assets/steps/05-takeaway.png)

Soft modules trade aspect for packing quality under area and aspect bounds. Always re-check legality after a resize.

<!-- /algorithm-walkthrough -->


## Slide 9 — Browser lab track

Open soft-module-sizing. Show hard three-by-two, then Reshape A to two by three. Confirm area six and legality true on the soft packing.

## Slide 10 — Implement track

Implement resize_soft that preserves area, then pack. Assert soft A ends at two by three with area six and a legal outline fit.

## Slide 11 — Pitfalls

Changing area when reshaping; ignoring aspect bounds; leaving hard modules soft by mistake.

## Slide 12 — Your turn

Accept a legal soft packing with A at two by three. Next: fix macro D at the origin.
