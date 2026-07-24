# Maze routing on GCells — step-by-step (for slides / transcript)

**Module:** `module02-05-maze-gcell-route`  
**Lab / algo:** `maze-gcell-route`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=maze-gcell-route&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Edge cost

![Step 1](steps/01-cost.png)

**Caption (transcript):** Maze adds penalty when usage ≥ capacity.

**Slide bullets:**

- Search on GCells
- Detour allowed

**On-screen metrics:**

```
Cost = 1 + penalty
```

## Step 2 — L overflow

![Step 2](steps/02-l-ov.png)

**Caption (transcript):** L-HV on spread overflows on shared corridors.

**Slide bullets:**

- Pattern first
- Then maze

**On-screen metrics:**

```
total=2
```

## Step 3 — Route maze

![Step 3](steps/03-maze.png)

**Caption (transcript):** Sequential maze routing considers current usage.

**Slide bullets:**

- Six nets
- Finite cost

**On-screen metrics:**

```
maze≈2
```

## Step 4 — Compare totals

![Step 4](steps/04-compare.png)

**Caption (transcript):** Maze may match or beat L overflow on the toy.

**Slide bullets:**

- Not magic
- Still Cap=2

**On-screen metrics:**

```
Compare L vs maze
```

## Step 5 — When to maze

![Step 5](steps/05-use.png)

**Caption (transcript):** Use maze when pattern routes saturate edges.

**Slide bullets:**

- Global stage
- Rip-up next

**On-screen metrics:**

```
Next modules
```

