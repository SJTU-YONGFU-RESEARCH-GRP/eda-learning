# Lee maze routing — step-by-step (for slides / transcript)

**Module:** `module02-01-lee-maze`  
**Lab / algo:** `lee-maze`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=lee-maze&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Breadth-first

![Step 1](steps/01-bfs.png)

**Caption (transcript):** Lee expands uniformly—first arrival is shortest hop count.

**Slide bullets:**

- Grid graph
- Blockage aware

**On-screen metrics:**

```
BFS layers
```

## Step 2 — Around macro

![Step 2](steps/02-detour.png)

**Caption (transcript):** Path (4,1)→(7,1) detours below blockage.

**Slide bullets:**

- Avoid blocked cells

**On-screen metrics:**

```
len=4
```

## Step 3 — Route Lee

![Step 3](steps/03-lee.png)

**Caption (transcript):** Sequential Lee assigns layers per step.

**Slide bullets:**

- Six nets

**On-screen metrics:**

```
Finite cost
```

## Step 4 — vs layered

![Step 4](steps/04-compare.png)

**Caption (transcript):** Lee may differ from L overflow totals.

**Slide bullets:**

- Compare totals

**On-screen metrics:**

```
Lee total≈0
```

## Step 5 — When to maze

![Step 5](steps/05-use.png)

**Caption (transcript):** Use maze when pattern routes hit blockages or hot tracks.

**Slide bullets:**

- Detailed stage

**On-screen metrics:**

```
A* next
```

