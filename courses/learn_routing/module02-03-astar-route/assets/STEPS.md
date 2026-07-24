# A* detailed routing — step-by-step (for slides / transcript)

**Module:** `module02-03-astar-route`  
**Lab / algo:** `astar-route`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=astar-route&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Track cost

![Step 1](steps/01-cost.png)

**Caption (transcript):** A* adds penalty when usage ≥ capacity.

**Slide bullets:**

- Manhattan h
- Detour allowed

**On-screen metrics:**

```
Penalize hot tracks
```

## Step 2 — Layered overflow

![Step 2](steps/02-l-ov.png)

**Caption (transcript):** Layered L-HV on spread overflows shared tracks.

**Slide bullets:**

- Shared M1/M2

**On-screen metrics:**

```
total=3
```

## Step 3 — Route A*

![Step 3](steps/03-astar.png)

**Caption (transcript):** Sequential A* considers current usage.

**Slide bullets:**

- Six nets

**On-screen metrics:**

```
total≈0
```

## Step 4 — Compare totals

![Step 4](steps/04-compare.png)

**Caption (transcript):** A* may clear overflow on the toy spread.

**Slide bullets:**

- Not magic

**On-screen metrics:**

```
Still Cap=2
```

## Step 5 — Move pins

![Step 5](steps/05-move.png)

**Caption (transcript):** Moving cells changes pin grid and paths.

**Slide bullets:**

- Learner state

**On-screen metrics:**

```
Check scores routes
```

