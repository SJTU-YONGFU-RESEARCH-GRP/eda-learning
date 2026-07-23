# Tetris row packing — step-by-step (for slides / transcript)

**Module:** `module02-07-tetris-row-pack`  
**Lab / algo:** `tetris-row-pack`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=tetris-row-pack&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Same overlap seed

![Step 1](steps/01-overlap-seed.png)

**Caption (transcript):** Tetris-lite assigns each cell to its nearest row, then left-packs within the row—same engine as overlap removal. Start from the triple stack at (4, 2).

**Slide bullets:**

- Nearest row from float y
- Per-row left pack
- No cross-row trial

**On-screen metrics:**

```
seed: OVERLAP
legal: false
```

## Step 2 — Nearest row, then left pack

![Step 2](steps/02-nearest-row.png)

**Caption (transcript):** A, B, and C stay on middle row two after snap. Sort by x and pack: A at four, B at six, C at eight—identical to overlap removal on this instance.

**Slide bullets:**

- Row locked after snap
- Shelf pack left-to-right
- Simpler control flow

**On-screen metrics:**

```
all on y=2
pack order A,B,C
```

## Step 3 — Result: disp 6, HPWL 32

![Step 3](steps/03-tetris-result.png)

**Caption (transcript):** Tetris legalizes with displacement six and HPWL thirty-two—the overlap-removal golden. Same coordinates, same metrics: this is the global legalize path in later labs.

**Slide bullets:**

- legal: true
- disp: 6
- HPWL: 32

**On-screen metrics:**

```
disp: 6
HPWL: 32
measured: 6
```

## Step 4 — Contrast Abacus disp 4

![Step 4](steps/04-contrast-abacus.png)

**Caption (transcript):** Abacus spreads A, B, C across three rows for displacement four. Tetris keeps them on one row and moves farther in x—six total L1 units.

**Slide bullets:**

- Abacus: cross-row, disp 4
- Tetris: single row, disp 6
- HPWL favors Tetris here

**On-screen metrics:**

```
abacusDisp: 4
tetrisDisp: 6
Δ disp: 2
```

## Step 5 — Tradeoff: simpler vs better displacement

![Step 5](steps/05-tradeoff.png)

**Caption (transcript):** Tetris is easier to implement and slightly better on HPWL for this toy. Abacus is the choice when displacement budget is tight—preview the detailed-vs-global lab.

**Slide bullets:**

- Tetris = global legalize lite
- Abacus = detailed legalize lite
- Pick by disp vs HPWL budget

**On-screen metrics:**

```
tetrisHpwl: 32
abacusHpwl: 38
```

