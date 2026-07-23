# Overlap removal — step-by-step (for slides / transcript)

**Module:** `module02-03-overlap-removal`  
**Lab / algo:** `overlap-removal`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=overlap-removal&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — A, B, C stacked at (4, 2)

![Step 1](steps/01-overlap-seed.png)

**Caption (transcript):** The overlap seed piles three width-two cells on the middle row at x equals four. Greedy snap would leave the same conflict—overlap removal snaps first, then packs each row left-to-right.

**Slide bullets:**

- A,B,C @ (4,2)
- illegal: overlap A/B
- D@8,4 · E@0,4 · F@10,0

**On-screen metrics:**

```
legal: false
reason: overlap A/B
```

## Step 2 — After snap: still stacked

![Step 2](steps/02-after-snap.png)

**Caption (transcript):** Snapping the overlap seed does not separate A, B, and C—they remain on (4, 2). Overlap removal keeps their row assignment and resolves x conflicts by packing.

**Slide bullets:**

- Snap preserves row intent
- Overlap is an x problem on-row
- Pack by increasing x order

**On-screen metrics:**

```
snap legal: false
middle row crowded
```

## Step 3 — Per-row pack: A@4, B@6, C@8

![Step 3](steps/03-row-pack.png)

**Caption (transcript):** On row y equals two, sort by x and place left without overlap: A at four, B at six, C at eight. Each width-two cell occupies two consecutive sites—now legal on that row.

**Slide bullets:**

- Preserve sort order from snap
- Left pack within row
- No cross-row moves

**On-screen metrics:**

```
A @ (4,2)
B @ (6,2)
C @ (8,2)
```

## Step 4 — Legal: disp 6, HPWL 32

![Step 4](steps/04-legal-metrics.png)

**Caption (transcript):** Full overlap removal on the seed is legal with total displacement six and HPWL thirty-two. D, E, and F never moved from their overlap-seed roles.

**Slide bullets:**

- legal: true
- L1 disp from overlap origin
- Report HPWL with same nets

**On-screen metrics:**

```
disp: 6
HPWL: 32
measured disp: 6
```

## Step 5 — D, E, F unchanged

![Step 5](steps/05-unchanged.png)

**Caption (transcript):** Macro-sized D stays at (8, 4), E at (0, 4), F at (10, 0). Overlap removal only repacked the crowded middle row—fixed-looking cells on other rows are untouched.

**Slide bullets:**

- D top row @ 8
- E top row @ 0
- F bottom row @ 10

**On-screen metrics:**

```
movables repacked: A,B,C
others held row
```

