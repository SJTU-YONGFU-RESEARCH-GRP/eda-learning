# Probabilistic routing demand — step-by-step (for slides / transcript)

**Module:** `module02-03-probabilistic-demand`  
**Lab / algo:** `probabilistic-demand`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=probabilistic-demand&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — L-shape idea

![Step 1](steps/01-lshape.png)

**Caption (transcript):** Two-pin nets route on L-shapes with half probability each bend.

**Slide bullets:**

- H-then-V and V-then-H

**On-screen metrics:**

```
Corridors not filled boxes
```

## Step 2 — Deposit along legs

![Step 2](steps/02-deposit.png)

**Caption (transcript):** Walk GCells on each leg and share demand along the path.

**Slide bullets:**

- Corner may be shared

**On-screen metrics:**

```
Document scaling
```

## Step 3 — Multi-pin star

![Step 3](steps/03-multi.png)

**Caption (transcript):** Star from bbox center to each pin; deposit like two-pin edges.

**Slide bullets:**

- Toy multi-pin

**On-screen metrics:**

```
Same Cap
```

## Step 4 — Versus RUDY

![Step 4](steps/04-compare.png)

**Caption (transcript):** Probabilistic concentrates on corridors; RUDY paints the bbox.

**Slide bullets:**

- Totals may differ

**On-screen metrics:**

```
Both teach overflow
```

## Step 5 — Spread again

![Step 5](steps/05-cool.png)

**Caption (transcript):** Spreading still reduces probabilistic overflow—feedback is placement.

**Slide bullets:**

- Same push ideas

**On-screen metrics:**

```
Next: heat map
```

