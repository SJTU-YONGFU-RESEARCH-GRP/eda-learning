# Examples — Fixed macros during legalization

Track A (implement). Use the tiny legalization instance first (`examples/tiny_legal.json`).

## Algorithm

**legalization with fixed macro obstacles**

## Starter prompts

1. Restate the idea in five bullets (inputs → row/site model → algorithm loop → legality → metrics).
2. Load cells A–F on the 12-site × 6-height grid (3 rows, rowH=2, bottoms y=0,2,4).
3. Pick `starter_float` or `starter_illegal` depending on the lab; confirm cell widths in sites.
4. Produce legal site-aligned coordinates; report legality boolean and total displacement from float start.
5. Change one knob (macro lock, pack order, snap rounding) and report HPWL or displacement delta.

## Expected artifacts

- Legal (x, y) per cell on site grid
- Legality boolean + displacement / HPWL summary
- Short note: why this idea belongs on the legalization shelf

## Stretch

Lock macro D at (8,4) or add a second fixed block; keep the same metrics API.
