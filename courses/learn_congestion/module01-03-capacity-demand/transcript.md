# Capacity vs demand

**Module id:** module01-03-capacity-demand
**Lab:** capacity-demand
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Supply and load

A GCell has a routing budget—capacity. Estimators deposit demand into the same tiles. When demand exceeds capacity the tile is oversubscribed. On our toy instance capacity is two point zero for every GCell unless you change it.

## Slide 2 — The idea

Surplus equals demand minus capacity. Positive surplus means overflow. List oversubscribed tiles before you trust a heat map. Capacity can later become anisotropic edge capacities; here it is a scalar so goldens stay simple.

<!-- algorithm-walkthrough -->

## Slide 3 — Capacity budget

![Capacity budget](assets/steps/01-cap.png)

Each GCell has capacity 2.0 on the toy instance.

## Slide 4 — Demand arrives

![Demand arrives](assets/steps/02-demand.png)

Estimators deposit demand into tiles; surplus = demand − Cap.

## Slide 5 — Oversubscribed tiles

![Oversubscribed tiles](assets/steps/03-flag.png)

Flag every tile with demand > Cap before trusting a heat map.

## Slide 6 — Lower Cap

![Lower Cap](assets/steps/04-toggle.png)

At Cap=1 more tiles fail—capacity is part of the contract.

## Slide 7 — Spread helps

![Spread helps](assets/steps/05-spread.png)

Moving cells outward reduces how many tiles exceed Cap.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

Open **capacity-demand**. Toggle capacity between one and two while holding a fixed demand seed. Watch which tiles flip. Check challenges that score your capacity choice against overflow counts—not a “show golden” click.

## Slide 9 — Implement track

Given a demand matrix from RUDY (or a hand-filled stub), compute surplus and the oversubscribed set. Print both for capacity equals two and capacity equals one. Keep the API ready for the overflow-metrics lab.

## Slide 10 — Pitfalls

Comparing demand to capacity without documenting units. Treating zero demand as “healthy” while ignoring that neighboring tiles may be hot. Changing capacity mid-challenge without resetting the starter placement.

## Slide 11 — Your turn

Complete Track A or B. Next: RUDY—the classic demand estimator that fills those tiles from net bounding boxes.
