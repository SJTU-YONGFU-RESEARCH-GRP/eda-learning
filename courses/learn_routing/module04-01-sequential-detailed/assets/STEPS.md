# Sequential detailed route — step-by-step (for slides / transcript)

**Module:** `module04-01-sequential-detailed`  
**Lab / algo:** `sequential-detailed`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=sequential-detailed&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Net order

![Step 1](steps/01-order.png)

**Caption (transcript):** Route nets 0..5 in order; later nets see earlier usage.

**Slide bullets:**

- Six nets

**On-screen metrics:**

```
NETS array
```

## Step 2 — Layered pass

![Step 2](steps/02-layer-all.png)

**Caption (transcript):** Layered L all nets documents baseline overflow.

**Slide bullets:**

- Pattern route

**On-screen metrics:**

```
total≈3
```

## Step 3 — Lee pass

![Step 3](steps/03-lee-all.png)

**Caption (transcript):** Sequential Lee may redistribute usage.

**Slide bullets:**

- Maze mode

**On-screen metrics:**

```
Lee≈0
```

## Step 4 — Clear overflow

![Step 4](steps/04-clear.png)

**Caption (transcript):** Goal: total overflow 0 after A* or moves.

**Slide bullets:**

- Challenge lab

**On-screen metrics:**

```
HPWL optional
```

## Step 5 — Handoff

![Step 5](steps/05-done.png)

**Caption (transcript):** Detailed routing feeds signoff DRC and extraction.

**Slide bullets:**

- Tracks + vias

**On-screen metrics:**

```
learn_drc next
```

