# Boundary pin / I/O assignment

**Module id:** module04-03-pin-assignment
**Lab:** pin-assignment
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Boundary pin / I/O assignment

Pins sit on outline edges. Golden assignment places P0 left, P1 bottom, P2 right, P3 top—four sides covered so pinsValid is true. An empty list is invalid.


## Slide 2 — Pseudocode

Pin assignment validates boundary I/O. Pseudocode checks side and offset ranges and requires all four outline sides to appear.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 3 — Algorithm sketch

Golden pins cover left, bottom, right, and top and return valid true. An empty list fails validity.

```text
INPUT: outline, pin list {side, offset}
OUTPUT: pinsValid?
each pin on left|right|top|bottom edge
offset in range for that side
require all four sides represented
GOLDEN 4 pins (one/side) → valid true
empty list → valid false
```


<!-- algorithm-walkthrough -->

## Slide 4 — Packing without pins

![Packing without pins](assets/steps/01-no-pins.png)

Start from the golden packing with an empty pin list. Pins will sit on outline edges—not inside modules—for I/O literacy.

## Slide 5 — Assign one pin per side

![Assign one pin per side](assets/steps/02-assign.png)

Golden pins place P0 on the left, P1 on the bottom, P2 on the right, and P3 on the top. Offsets stay inside each edge length.

## Slide 6 — Coverage makes pinsValid true

![Coverage makes pinsValid true](assets/steps/03-valid.png)

pinsValid requires every side to appear and offsets to lie on the edge. The golden set covers all four sides—valid returns true.

## Slide 7 — Empty set is invalid

![Empty set is invalid](assets/steps/04-empty-bad.png)

Clear the pins and validity fails: you no longer cover four sides. Assignment is a first-class constraint, not decoration.

## Slide 8 — Pins feed place and route

![Pins feed place and route](assets/steps/05-takeaway.png)

Boundary pins shape terminal propagation and routing demand. After floorplan shapes settle, pin assignment is the bridge to placement.

<!-- /algorithm-walkthrough -->


## Slide 9 — Browser lab track

Open pin-assignment. Assign golden pins, confirm four sides and valid true. Clear pins and watch validity fail.

## Slide 10 — Implement track

Implement pinsValid requiring all four sides and in-range offsets. Assert golden pins pass and the empty list fails.

## Slide 11 — Pitfalls

Putting pins inside modules; offsets past edge length; claiming validity with only two sides covered.

## Slide 12 — Your turn

Ship a valid four-side assignment. Offline compare is next; then the wrap points to learn_placement.
