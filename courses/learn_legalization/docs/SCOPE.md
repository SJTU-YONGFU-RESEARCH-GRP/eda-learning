# Scope — learn_legalization

## In scope

- Site and row geometry model (sites, rowH, cell width in sites)
- Legality checking: row alignment, site snapping, non-overlap
- Greedy site/row snap from global-place floats
- In-row overlap removal
- Abacus and Tetris-style row packing (educational lite versions)
- Fixed macro obstacles during legalization
- Displacement vs HPWL tradeoff metrics
- Global vs detailed legalization pipeline contrast
- Offline compare habits on shared tiny instances

## Out of scope (v1)

- Production OpenROAD or commercial legalizer sign-off
- Vendor GUI workflows (Innovus / ICC2 click-paths)
- Full detailed placement optimization beyond scoped lite flows
- Foundry PDK certification

## Reference instance

[`common/tiny_legal.json`](../common/tiny_legal.json): W=12 sites, H=6 (3 rows), siteW=1, rowH=2, row bottoms y=0,2,4. Cells A–D width 2 sites; E,F width 1. Nets match learn_placement. Fixed macro D at (8,4). Starters: `starter_illegal` (overlap on middle row) and `starter_float` (global-place floats).

## “Full implementation” means

Complete and correct for the **scoped problem size** (six cells on a tiny site grid): parse input, legalize, emit coordinates + legality/displacement/HPWL—not a production-scale engine.
