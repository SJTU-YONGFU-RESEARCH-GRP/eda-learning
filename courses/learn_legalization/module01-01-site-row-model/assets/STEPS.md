# Site and row model — step-by-step (for slides / transcript)

**Module:** `module01-01-site-row-model`  
**Lab / algo:** `site-row-model`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=site-row-model&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Twelve-by-six chip, three rows

![Step 1](steps/01-empty-chip.png)

**Caption (transcript):** Legalization lives on a discrete canvas: chip width twelve sites, height six (three rows of height two). Row bottoms sit at y equals zero, two, and four. Every movable cell must land on a row and align to site pitch one.

**Slide bullets:**

- CHIP_W = 12 · CHIP_H = 6
- Row bottoms: y = 0, 2, 4
- Lower-left origin for cell coordinates

**On-screen metrics:**

```
chip: 12×6
rows: 3
rowH: 2
```

## Step 2 — Cell widths A–D = 2, E–F = 1

![Step 2](steps/02-cell-widths.png)

**Caption (transcript):** Six cells A through F occupy ten sites total—two sites each for A–D and one each for E and F. Width drives how many consecutive sites a rectangle spans when you pack a row.

**Slide bullets:**

- Widths are integers in site units
- Total width 10 ≤ chip 12
- Same six-cell toy across all labs

**On-screen metrics:**

```
A–D width: 2
E–F width: 1
total width: 10
```

## Step 3 — Site pitch equals one

![Step 3](steps/03-site-pitch.png)

**Caption (transcript):** Each vertical tick is one site. Legal x coordinates are integers; a width-two cell at x equals four covers sites four and five on its row. The golden packing shows legal site alignment.

**Slide bullets:**

- SITE_W = 1
- x must be integer-aligned
- Row lines dashed at y = 0, 2, 4

**On-screen metrics:**

```
site pitch: 1
rows: 0, 2, 4
```

## Step 4 — Golden legal packing

![Step 4](steps/04-golden-pack.png)

**Caption (transcript):** The reference legal layout spreads A and B on row zero, C on row one, and E plus D on row top. No overlap, every cell on-row and site-aligned—this is the teaching golden.

**Slide bullets:**

- Row 0: A@0, B@2, F@10
- Row 2: C@0
- Row 4: E@0, D@8

**On-screen metrics:**

```
legal: true
HPWL: 50
reason: ok
```

## Step 5 — Contrast: illegal overlap stack

![Step 5](steps/05-overlap-contrast.png)

**Caption (transcript):** The overlap seed stacks A, B, and C at (4, 2) on the middle row—same width-two cells fighting for the same sites. Legality fails before you even discuss wirelength.

**Slide bullets:**

- A,B,C @ (4,2) stacked
- First failure: overlap A/B
- Legalization must repair this

**On-screen metrics:**

```
legal: false
reason: overlap A/B
Next: legality metrics
```

