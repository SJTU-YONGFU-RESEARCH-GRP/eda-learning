# Cell inflation — step-by-step (for slides / transcript)

**Module:** `module03-01-cell-inflator`  
**Lab / algo:** `cell-inflator`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=cell-inflator&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Why inflate

![Step 1](steps/01-idea.png)

**Caption (transcript):** Make cells in hot GCells act larger so the next place pass spreads.

**Slide bullets:**

- Width scale

**On-screen metrics:**

```
Coords unchanged here
```

## Step 2 — Scale rule

![Step 2](steps/02-rule.png)

**Caption (transcript):** If cong>1: w' = w·(1+α(c−1)), α=0.5.

**Slide bullets:**

- Else keep w

**On-screen metrics:**

```
Center cells grow
```

## Step 3 — Apply once

![Step 3](steps/03-run.png)

**Caption (transcript):** Compute congestion from RUDY, then inflate widths once.

**Slide bullets:**

- Don’t double-apply

**On-screen metrics:**

```
Reset to base widths
```

## Step 4 — Quiet tiles

![Step 4](steps/04-quiet.png)

**Caption (transcript):** Cells in tiles with cong≤1 stay at base width.

**Slide bullets:**

- Selective

**On-screen metrics:**

```
E may stay 1
```

## Step 5 — Link to place

![Step 5](steps/05-link.png)

**Caption (transcript):** Widths feed the next placer—estimation alone is not enough.

**Slide bullets:**

- Feedback course arc

**On-screen metrics:**

```
Net weights next
```

