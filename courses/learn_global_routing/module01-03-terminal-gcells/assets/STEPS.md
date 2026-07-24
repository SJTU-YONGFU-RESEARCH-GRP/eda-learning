# Pin terminals on GCells — step-by-step (for slides / transcript)

**Module:** `module01-03-terminal-gcells`  
**Lab / algo:** `terminal-gcells`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=terminal-gcells&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Pin → GCell

![Step 1](steps/01-map.png)

**Caption (transcript):** Cell centers map to GCells with floor(x/cellW), floor(y/cellH).

**Slide bullets:**

- Same as congestion grid
- i,j clamped

**On-screen metrics:**

```
Terminals move with cells
```

## Step 2 — A → (0,0)

![Step 2](steps/02-a00.png)

**Caption (transcript):** Spread A at (1,1) lands in GCell (0,0).

**Slide bullets:**

- Lower-left origin
- Clamp edges

**On-screen metrics:**

```
A → (0,0)
```

## Step 3 — D → (2,1)

![Step 3](steps/03-d21.png)

**Caption (transcript):** D at (8,5) → (2,1) top row.

**Slide bullets:**

- Top row j=1

**On-screen metrics:**

```
D → (2,1)
```

## Step 4 — Routes on graph

![Step 4](steps/04-route.png)

**Caption (transcript):** Global routes walk GCell edges between terminal tiles.

**Slide bullets:**

- Not bbox paint
- Edge usage

**On-screen metrics:**

```
L-HV overlay
```

## Step 5 — Cluster seed

![Step 5](steps/05-cluster.png)

**Caption (transcript):** Tight cluster maps many pins to one GCell—zero-length routes.

**Slide bullets:**

- Hot for study
- Spread for overflow

**On-screen metrics:**

```
Same grid
```

