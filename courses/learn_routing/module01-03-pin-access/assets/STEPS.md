# Pin access points — step-by-step (for slides / transcript)

**Module:** `module01-03-pin-access`  
**Lab / algo:** `pin-access`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=pin-access&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Pin → grid

![Step 1](steps/01-map.png)

**Caption (transcript):** Cell centers round to grid indices.

**Slide bullets:**

- Same spread as global

**On-screen metrics:**

```
Clamp on-chip
```

## Step 2 — A → (1,1)

![Step 2](steps/02-a11.png)

**Caption (transcript):** Spread A lands on grid (1,1).

**Slide bullets:**

- Terminals move with cells

**On-screen metrics:**

```
A 1,1
```

## Step 3 — D → (8,5)

![Step 3](steps/03-d85.png)

**Caption (transcript):** D at (8,5) top row.

**Slide bullets:**

- Top row y=5

**On-screen metrics:**

```
D 8,5
```

## Step 4 — Blocked pins

![Step 4](steps/04-nudge.png)

**Caption (transcript):** E/F on blockage nudge to nearest free neighbor.

**Slide bullets:**

- Access point
- Toy only

**On-screen metrics:**

```
Pin access
```

## Step 5 — Routes from pins

![Step 5](steps/05-route.png)

**Caption (transcript):** Sequential routes start/end at terminal grid points.

**Slide bullets:**

- Not bbox

**On-screen metrics:**

```
Track usage
```

