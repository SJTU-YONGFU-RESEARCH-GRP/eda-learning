# Cell inflation

**Module id:** module03-01-cell-inflator
**Lab:** cell-inflator
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Make hot cells larger

Inflators tell the placer that cells in congested GCells should act bigger, encouraging spreading on the next pass. On the toy grid we scale width: width prime equals width times one plus alpha times congestion minus one, when congestion is above one.

## Slide 2 — The idea

Map each cell center to a GCell. If that tile’s congestion exceeds one, inflate; otherwise leave width alone. Alpha around zero point five keeps the demo visible without exploding geometry. Coordinates stay put—this lab changes widths, not x y.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **cell-inflator**. Run inflate on congested_seed and read which cells grew. Challenges verify inflated widths from your congestion state.

## Slide 4 — Implement track

Implement `inflate_cells` with alpha equals zero point five. Print before/after widths for cells sitting in oversubscribed tiles.

## Slide 5 — Pitfalls

Inflating every cell when only some GCells are hot. Inflating height when the placer model only tracks width. Applying inflation twice without resetting to base widths.

## Slide 6 — Your turn

Clear the inflator challenges. Next: net weighting—the wirelength-side knob.
