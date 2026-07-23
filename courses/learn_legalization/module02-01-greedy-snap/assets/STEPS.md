# Greedy snap — step-by-step (for slides / transcript)

**Module:** `module02-01-greedy-snap`  
**Lab / algo:** `greedy-snap`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=greedy-snap&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Float placement from global place

![Step 1](steps/01-float-seed.png)

**Caption (transcript):** After global placement, cells sit at fractional coordinates—A near (3.7, 1.2), B near (4.1, 1.4). Nothing is site-aligned yet; that is the float seed for greedy snap.

**Slide bullets:**

- Fractional x and y
- Middle row target for A–C
- D, E, F also float

**On-screen metrics:**

```
starter: FLOAT_PLACEMENT
legal before snap: false
```

## Step 2 — Snap every cell to nearest site

![Step 2](steps/02-snap-all.png)

**Caption (transcript):** Greedy snap rounds x to the nearest site and y to the nearest row. A lands at (4, 2)—same as B. C snaps to (5, 2). D, E, and F snap to their row neighbors.

**Slide bullets:**

- snapX with cell width clamp
- snapY to nearest ROW_YS
- No overlap repair yet

**On-screen metrics:**

```
A → (4, 2)
B → (4, 2)
C → (5, 2)
```

## Step 3 — Still illegal: A/B overlap

![Step 3](steps/03-still-overlap.png)

**Caption (transcript):** After snap, A and B still share (4, 2). The legality report again says overlap A/B. Snap alone does not legalize—it only quantizes coordinates.

**Slide bullets:**

- floatSnapLegal: false
- Same failure as overlap seed
- C nearby but not stacked

**On-screen metrics:**

```
legal: false
reason: overlap A/B
A,B @ (4,2)
```

## Step 4 — Teaching point: snap ≠ legal

![Step 4](steps/04-snap-not-legal.png)

**Caption (transcript):** Students often assume rounding fixes everything. On this instance greedy snap creates the same middle-row pile as the integer overlap seed. Legalization needs a second phase.

**Slide bullets:**

- Snap is necessary, not sufficient
- Check legality after snap
- Next: overlap removal or Abacus

**On-screen metrics:**

```
greedy snap only
overlap remains
```

## Step 5 — Next: overlap removal / Abacus

![Step 5](steps/05-next-phase.png)

**Caption (transcript):** Follow snap with per-row packing or Abacus row assignment. Overlap removal spreads A, B, C along row two; Abacus spreads them across rows with lower displacement.

**Slide bullets:**

- overlap-removal: disp 6
- abacus: disp 4
- Both start from overlap or float snap

**On-screen metrics:**

```
overlapRemovalDisp: 6
abacusDisp: 4
```

