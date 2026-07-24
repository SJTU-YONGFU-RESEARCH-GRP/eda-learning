# L-shape pattern routes — step-by-step (for slides / transcript)

**Module:** `module02-01-pattern-l-route`  
**Lab / algo:** `pattern-l-route`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=pattern-l-route&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — L-shape

![Step 1](steps/01-idea.png)

**Caption (transcript):** Two-pin nets use one bend: HV (horizontal first) or VH.

**Slide bullets:**

- Manhattan
- One corner

**On-screen metrics:**

```
Pattern router
```

## Step 2 — Route L-HV

![Step 2](steps/02-hv.png)

**Caption (transcript):** Spread placement L-HV yields documented overflow.

**Slide bullets:**

- All six nets
- Shared corridors

**On-screen metrics:**

```
total≈2
```

## Step 3 — Route L-VH

![Step 3](steps/03-vh.png)

**Caption (transcript):** Swapping bend order changes which edges saturate.

**Slide bullets:**

- Same pins
- Different edges

**On-screen metrics:**

```
VH total≈1
```

## Step 4 — Edge usage

![Step 4](steps/04-edges.png)

**Caption (transcript):** Thicker edges show usage; red dash marks overflow.

**Slide bullets:**

- usage vs cap
- max/count

**On-screen metrics:**

```
Heat on edges
```

## Step 5 — Move pins

![Step 5](steps/05-move.png)

**Caption (transcript):** Moving cells changes terminal GCells and L paths.

**Slide bullets:**

- Learner state
- Check scores routes

**On-screen metrics:**

```
Browser lab next
```

