# Routing grid graph — step-by-step (for slides / transcript)

**Module:** `module01-01-routing-grid`  
**Lab / algo:** `routing-grid`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=routing-grid&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — 12×8 grid

![Step 1](steps/01-grid.png)

**Caption (transcript):** Detailed routes walk grid points; M1 horizontal, M2 vertical.

**Slide bullets:**

- Cap=2 per track
- Blockage 2×2

**On-screen metrics:**

```
12×8
```

## Step 2 — Two layers

![Step 2](steps/02-layers.png)

**Caption (transcript):** Horizontal moves on M1; vertical on M2; via switches at grid point.

**Slide bullets:**

- M1 / M2
- Layer rules

**On-screen metrics:**

```
Not GCell
```

## Step 3 — Blockage

![Step 3](steps/03-block.png)

**Caption (transcript):** Cells (5–6, 2–3) are blocked—maze must detour.

**Slide bullets:**

- 2×2 macro
- Pin nudge

**On-screen metrics:**

```
Lee lab
```

## Step 4 — Neighbors

![Step 4](steps/04-neigh.png)

**Caption (transcript):** Free grid points have up to four neighbors.

**Slide bullets:**

- Four-connected

**On-screen metrics:**

```
mid=4
```

## Step 5 — Capacity

![Step 5](steps/05-cap.png)

**Caption (transcript):** Track usage vs capacity drives overflow and rip-up.

**Slide bullets:**

- Cap=2

**On-screen metrics:**

```
Document goldens
```

