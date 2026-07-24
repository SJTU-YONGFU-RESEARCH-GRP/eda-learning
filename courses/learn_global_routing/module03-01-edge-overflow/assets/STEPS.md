# Edge overflow metrics — step-by-step (for slides / transcript)

**Module:** `module03-01-edge-overflow`  
**Lab / algo:** `edge-overflow`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=edge-overflow&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Overflow

![Step 1](steps/01-def.png)

**Caption (transcript):** ov(e)=max(0, usage(e)−Cap) per edge.

**Slide bullets:**

- Not tile RUDY
- Router metric

**On-screen metrics:**

```
Edge-local
```

## Step 2 — Total overflow

![Step 2](steps/02-total.png)

**Caption (transcript):** Sum over edges—primary regression scalar.

**Slide bullets:**

- Sum ov(e)
- Report every pass

**On-screen metrics:**

```
spread L-HV≈2
```

## Step 3 — Max overflow

![Step 3](steps/03-max.png)

**Caption (transcript):** Worst edge—catches hotspot corridors.

**Slide bullets:**

- Hot corridor
- max metric

**On-screen metrics:**

```
max≈1
```

## Step 4 — Overflow count

![Step 4](steps/04-count.png)

**Caption (transcript):** How many edges exceed Cap.

**Slide bullets:**

- Triple report
- Same idea as congestion labs

**On-screen metrics:**

```
count edges
```

## Step 5 — Hit targets

![Step 5](steps/05-target.png)

**Caption (transcript):** Move pins or switch HV/VH/maze to clear thresholds.

**Slide bullets:**

- Check scores learner
- No golden mode

**On-screen metrics:**

```
Browser challenges
```

