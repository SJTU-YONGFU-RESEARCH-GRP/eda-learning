# RUDY congestion estimate — step-by-step (for slides / transcript)

**Module:** `module02-01-rudy-estimate`  
**Lab / algo:** `rudy-estimate`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=rudy-estimate&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Net bounding box

![Step 1](steps/01-bbox.png)

**Caption (transcript):** RUDY starts from each net’s axis-aligned pin bbox and HPWL.

**Slide bullets:**

- HPWL = width+height

**On-screen metrics:**

```
6 nets
```

## Step 2 — Uniform share

![Step 2](steps/02-share.png)

**Caption (transcript):** Density = HPWL / #overlapping GCells; add to each overlapping tile.

**Slide bullets:**

- At least one tile

**On-screen metrics:**

```
Deterministic
```

## Step 3 — Sum over nets

![Step 3](steps/03-sum.png)

**Caption (transcript):** Demand is the sum across nets—center tiles collect many contributions on a cluster.

**Slide bullets:**

- Matrix 4×2

**On-screen metrics:**

```
Seed max ov ≈ 5
```

## Step 4 — Overflow appears

![Step 4](steps/04-overflow.png)

**Caption (transcript):** ov = max(0, demand−Cap). Seed shows a clear hotspot.

**Slide bullets:**

- total/max/count

**On-screen metrics:**

```
Cap=2
```

## Step 5 — Spread cools total pattern

![Step 5](steps/05-spread.png)

**Caption (transcript):** Long nets paint many tiles; cluster spikes max. Both are useful views.

**Slide bullets:**

- Compare seeds

**On-screen metrics:**

```
Use max for hotspots
```

