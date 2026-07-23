# GCell grid model — step-by-step (for slides / transcript)

**Module:** `module01-01-gcell-grid`  
**Lab / algo:** `gcell-grid`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=gcell-grid&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Chip and GCells

![Step 1](steps/01-chip.png)

**Caption (transcript):** Twelve by eight chip with a four-by-two GCell overlay. Each tile is three by four.

**Slide bullets:**

- Lower-left origin
- i = floor(x/3)
- j = floor(y/4)

**On-screen metrics:**

```
Grid: 4×2
cellW=3 cellH=4
```

## Step 2 — A lands in (0,0)

![Step 2](steps/02-a00.png)

**Caption (transcript):** Cell A at (1,1) indexes to GCell column 0, row 0.

**Slide bullets:**

- Clamp to last tile on edges

**On-screen metrics:**

```
A → (0,0)
```

## Step 3 — D lands in (2,1)

![Step 3](steps/03-d21.png)

**Caption (transcript):** D at (8,5) → i=2, j=1 (top row).

**Slide bullets:**

- Top row is j=1

**On-screen metrics:**

```
D → (2,1)
```

## Step 4 — Paint all centers

![Step 4](steps/04-paint.png)

**Caption (transcript):** Every cell maps to exactly one GCell; the grid is the router’s coarse map.

**Slide bullets:**

- Used by every estimator

**On-screen metrics:**

```
8 tiles total
```

## Step 5 — Clustered seed

![Step 5](steps/05-seed.png)

**Caption (transcript):** Congested seed piles cells into center tiles—later labs heat those GCells.

**Slide bullets:**

- Same grid, hotter map

**On-screen metrics:**

```
Center columns
```

