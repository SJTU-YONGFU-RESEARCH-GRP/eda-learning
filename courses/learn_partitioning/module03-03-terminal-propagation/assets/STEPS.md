# Terminal propagation — step-by-step (for slides / transcript)

**Module:** `module03-03-terminal-propagation`  
**Lab / algo:** `terminal-propagation`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=terminal-propagation&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Fix pads A and E to opposite sides

![Step 1](steps/01-fixed-terminals.png)

**Caption (transcript):** I/O terminals are pinned: A→side 0, E→side 1. Free nodes B, C, D propagate by taking the side of the strongest neighboring fixed/assigned node.

**Slide bullets:**

- Terminals never flip
- Free nodes vote by edge weight
- Iterate until stable

**On-screen metrics:**

```
fixed: A=0, E=1
free: B, C, D
```

## Step 2 — B joins A (w=5)

![Step 2](steps/02-b-joins-a.png)

**Caption (transcript):** B hears A strongly on side 0 (A–B weight 5) versus weak pull from E. B adopts side 0 immediately.

**Slide bullets:**

- vote(side) = Σ w to neighbors on that side
- Heavy A–B affinity wins
- Fixed A anchors the ABC community

**On-screen metrics:**

```
B → side 0
A–B internal
```

## Step 3 — D joins E (w=5)

![Step 3](steps/03-d-joins-e.png)

**Caption (transcript):** D hears E on side 1 (D–E weight 5). D adopts side 1, forming the DE block opposite ABC.

**Slide bullets:**

- Symmetric to B joining A
- Fixed E anchors DE
- Two communities emerging

**On-screen metrics:**

```
D → side 1
D–E internal
```

## Step 4 — C bridges by neighbor vote

![Step 4](steps/04-c-bridge.png)

**Caption (transcript):** C connects to both communities. Neighbor vote sums favor joining A/B side (w=4+1 vs w=2+1). C lands on side 0 with A,B.

**Slide bullets:**

- Bridge node follows stronger pull
- Cut edges: C–D, C–E only
- cutsize = 3

**On-screen metrics:**

```
C → side 0
parts: ABC|DE
cutsize: 3
```

## Step 5 — Fixed I/O drives partition

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Terminal propagation converges in 2 iterations on this graph. Real designs pin hundreds of pads — free logic follows connectivity to terminals.

**Slide bullets:**

- A/E terminals → ABC|DE
- Same golden as spectral/grow
- Cheap seed before FM refine

**On-screen metrics:**

```
iters: 2
cutsize: 3
```

