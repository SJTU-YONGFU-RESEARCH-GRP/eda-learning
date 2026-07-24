# Overflow metrics — step-by-step (for slides / transcript)

**Module:** `module02-07-overflow-metrics`  
**Lab / algo:** `overflow-metrics`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=overflow-metrics&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Define overflow

![Step 1](steps/01-def.png)

**Caption (transcript):** ov = max(0, demand−Cap) per tile.

**Slide bullets:**

- Never negative

**On-screen metrics:**

```
Cap=2
```

## Step 2 — Total overflow

![Step 2](steps/02-total.png)

**Caption (transcript):** Sum of per-tile overflow—primary regression number.

**Slide bullets:**

- Seed total = 5

**On-screen metrics:**

```
Spread total higher but flatter
```

## Step 3 — Max overflow

![Step 3](steps/03-max.png)

**Caption (transcript):** Worst tile—catches hotspots even when total is moderate.

**Slide bullets:**

- Seed max = 5

**On-screen metrics:**

```
Hotspot detector
```

## Step 4 — Congested count

![Step 4](steps/04-count.png)

**Caption (transcript):** How many tiles overflow—useful for “how widespread”.

**Slide bullets:**

- count on seed = 1

**On-screen metrics:**

```
Triple report
```

## Step 5 — Hit a target

![Step 5](steps/05-target.png)

**Caption (transcript):** Move cells until total/max/count clear challenge thresholds.

**Slide bullets:**

- Check scores positions

**On-screen metrics:**

```
No reveal required
```

