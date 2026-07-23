# Legality metrics — step-by-step (for slides / transcript)

**Module:** `module01-03-legality-metrics`  
**Lab / algo:** `legality-metrics`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=legality-metrics&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Overlap seed is illegal

![Step 1](steps/01-overlap-illegal.png)

**Caption (transcript):** Starting from the overlap placement, the checker reports overlap A/B first—three cells share the middle row at x equals four. That single reason is enough to fail legality.

**Slide bullets:**

- Pairwise overlap on same row
- First reason wins the report
- Golden overlapIllegal: true

**On-screen metrics:**

```
legal: false
reason: overlap A/B
all reasons: 3
```

## Step 2 — Four legality checks

![Step 2](steps/02-checks.png)

**Caption (transcript):** A legal placement must be on-row, site-aligned, inside the chip, and overlap-free. Fixed macros add a fifth check later—did the macro move off its lock?

**Slide bullets:**

- On-row: y ∈ {0, 2, 4}
- Site-aligned: integer x
- In-chip: x + width ≤ 12
- No area overlap on a row

**On-screen metrics:**

```
rows: 3
chip width: 12
edge-touch OK, area overlap not
```

## Step 3 — Golden placement passes

![Step 3](steps/03-golden-ok.png)

**Caption (transcript):** The golden reference satisfies every check: reason ok, legal true. Use it as the positive control when you unit-test your legality reporter.

**Slide bullets:**

- All cells on valid rows
- Integer site coordinates
- No pairwise overlap

**On-screen metrics:**

```
legal: true
reason: ok
goldenLegal: true
```

## Step 4 — Displacement: L1 from origin

![Step 4](steps/04-displacement.png)

**Caption (transcript):** Displacement sums Manhattan distance per cell from a reference layout—here the overlap seed. Abacus later moves cells only four total units; overlap removal moves six.

**Slide bullets:**

- L1: |Δx| + |Δy| per cell
- Sum over all movables
- Lower is closer to global place

**On-screen metrics:**

```
overlap-removal disp: 6
abacus disp: 4
Report after legalize
```

## Step 5 — HPWL after legalize

![Step 5](steps/05-hpwl-after.png)

**Caption (transcript):** Wirelength still matters: Abacus lands at HPWL thirty-eight with displacement four; Tetris-style packing hits HPWL thirty-two with displacement six. Always pair legality with both metrics.

**Slide bullets:**

- Same nets as placement course
- Cell centers for HPWL bbox
- Legal ≠ optimal HPWL

**On-screen metrics:**

```
abacus HPWL: 38
tetris HPWL: 32
abacus disp: 4
```

