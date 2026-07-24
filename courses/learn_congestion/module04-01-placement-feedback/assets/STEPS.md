# Placement feedback loop — step-by-step (for slides / transcript)

**Module:** `module04-01-placement-feedback`  
**Lab / algo:** `placement-feedback`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=placement-feedback&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Hot starter

![Step 1](steps/01-seed.png)

**Caption (transcript):** Congested seed starts with total overflow 5 at Cap=2.

**Slide bullets:**

- RUDY demand

**On-screen metrics:**

```
Need a loop
```

## Step 2 — Estimate

![Step 2](steps/02-estimate.png)

**Caption (transcript):** Run RUDY → congestion → overflow per tile.

**Slide bullets:**

- Same estimators

**On-screen metrics:**

```
Matrix in hand
```

## Step 3 — Push outward

![Step 3](steps/03-push.png)

**Caption (transcript):** Cells in overflowing tiles step toward the quietest neighbor GCell.

**Slide bullets:**

- Clamp to chip

**On-screen metrics:**

```
Toy one-pass
```

## Step 4 — Overflow drops

![Step 4](steps/04-after.png)

**Caption (transcript):** After one feedback pass, total overflow falls (often to ~0 on this toy).

**Slide bullets:**

- Remeasure demand

**On-screen metrics:**

```
Assert after < before
```

## Step 5 — Toward routing

![Step 5](steps/05-next.png)

**Caption (transcript):** Real flows iterate with global routing; next course deepens GCell edges.

**Slide bullets:**

- learn_global_routing

**On-screen metrics:**

```
CTS also next
```

