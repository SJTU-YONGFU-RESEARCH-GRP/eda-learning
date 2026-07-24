# Pin terminals on GCells

**Module id:** module01-03-terminal-gcells
**Lab:** terminal-gcells
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Pins become terminals

A global route starts and ends at GCell terminals—one tile per pin. Legal placement gives you x y coordinates; this module converts them to grid indices using the same floor-and-clamp rule as congestion GCells.

## Slide 2 — The idea

cell_gcell of x y returns column i equals floor of x over cell width clamped, and row j likewise. Cell A at one comma one maps to zero comma zero. Cell D at eight comma five maps to two comma one. Build a dictionary from cell id to GCell for every pin in the netlist.

<!-- algorithm-walkthrough -->

## Slide 3 — Pin → GCell

![Pin → GCell](assets/steps/01-map.png)

Cell centers map to GCells with floor(x/cellW), floor(y/cellH).

## Slide 4 — A → (0,0)

![A → (0,0)](assets/steps/02-a00.png)

Spread A at (1,1) lands in GCell (0,0).

## Slide 5 — D → (2,1)

![D → (2,1)](assets/steps/03-d21.png)

D at (8,5) → (2,1) top row.

## Slide 6 — Routes on graph

![Routes on graph](assets/steps/04-route.png)

Global routes walk GCell edges between terminal tiles.

## Slide 7 — Cluster seed

![Cluster seed](assets/steps/05-cluster.png)

Tight cluster maps many pins to one GCell—zero-length routes.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Open **terminal-gcells**. Hover each cell and read its terminal GCell. Move a pin across a boundary and watch the terminal index flip. Confirm the six cells on tiny_gr match your Track A printout.


## Slide 9 — Implement track

Implement `terminals(positions, data)` returning the map. Assert A through F on spread placement. Print terminals before any routing lab.

## Slide 10 — Pitfalls

Using cell origin instead of pin center. Off-by-one at the right or top chip edge without clamp. Mixing site columns from legalization with GCell columns.

## Slide 11 — Your turn

Complete terminals for all six cells. Next: L-shape pattern routes between two terminals.
