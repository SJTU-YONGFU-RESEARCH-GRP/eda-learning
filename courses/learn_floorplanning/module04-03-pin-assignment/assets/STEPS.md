# Boundary pin / I/O assignment — step-by-step (for slides / transcript)

**Module:** `module04-03-pin-assignment`  
**Lab / algo:** `pin-assignment`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=pin-assignment&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Packing without pins

![Step 1](steps/01-no-pins.png)

**Caption (transcript):** Start from the golden packing with an empty pin list. Pins will sit on outline edges—not inside modules—for I/O literacy.

**Slide bullets:**

- Golden pack shown
- pins: none
- Four sides available

**On-screen metrics:**

```
pins: 0
valid: false (needs 4 sides)
```

## Step 2 — Assign one pin per side

![Step 2](steps/02-assign.png)

**Caption (transcript):** Golden pins place P0 on the left, P1 on the bottom, P2 on the right, and P3 on the top. Offsets stay inside each edge length.

**Slide bullets:**

- P0 left @2
- P1 bottom @4
- P2 right @3
- P3 top @5

**On-screen metrics:**

```
pins: 4
sides: 4
```

## Step 3 — Coverage makes pinsValid true

![Step 3](steps/03-valid.png)

**Caption (transcript):** pinsValid requires every side to appear and offsets to lie on the edge. The golden set covers all four sides—valid returns true.

**Slide bullets:**

- Four distinct sides
- Offsets in range
- valid: true

**On-screen metrics:**

```
valid: true
ids: P0–P3
```

## Step 4 — Empty set is invalid

![Step 4](steps/04-empty-bad.png)

**Caption (transcript):** Clear the pins and validity fails: you no longer cover four sides. Assignment is a first-class constraint, not decoration.

**Slide bullets:**

- Empty → invalid
- Need four sides
- Order/offsets matter later

**On-screen metrics:**

```
pins: 0
valid: false
```

## Step 5 — Pins feed place and route

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Boundary pins shape terminal propagation and routing demand. After floorplan shapes settle, pin assignment is the bridge to placement.

**Slide bullets:**

- One pin per side in the toy
- valid covers left/right/top/bottom
- Next course: learn_placement

**On-screen metrics:**

```
starter: P0–P3 on four sides
```

