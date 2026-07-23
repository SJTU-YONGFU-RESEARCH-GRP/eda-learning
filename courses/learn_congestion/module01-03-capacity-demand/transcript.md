# Capacity vs demand

**Module id:** module01-03-capacity-demand
**Lab:** capacity-demand
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Supply and load

A GCell has a routing budget—capacity. Estimators deposit demand into the same tiles. When demand exceeds capacity the tile is oversubscribed. On our toy instance capacity is two point zero for every GCell unless you change it.

## Slide 2 — The idea

Surplus equals demand minus capacity. Positive surplus means overflow. List oversubscribed tiles before you trust a heat map. Capacity can later become anisotropic edge capacities; here it is a scalar so goldens stay simple.

## Slide 3 — Browser lab track

Open **capacity-demand**. Toggle capacity between one and two while holding a fixed demand seed. Watch which tiles flip. Check challenges that score your capacity choice against overflow counts—not a “show golden” click.

## Slide 4 — Implement track

Given a demand matrix from RUDY (or a hand-filled stub), compute surplus and the oversubscribed set. Print both for capacity equals two and capacity equals one. Keep the API ready for the overflow-metrics lab.

## Slide 5 — Pitfalls

Comparing demand to capacity without documenting units. Treating zero demand as “healthy” while ignoring that neighboring tiles may be hot. Changing capacity mid-challenge without resetting the starter placement.

## Slide 6 — Your turn

Complete Track A or B. Next: RUDY—the classic demand estimator that fills those tiles from net bounding boxes.
