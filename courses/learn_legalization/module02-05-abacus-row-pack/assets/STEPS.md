# Abacus row packing — step-by-step (for slides / transcript)

**Module:** `module02-05-abacus-row-pack`  
**Lab / algo:** `abacus-row-pack`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=abacus-row-pack&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Start from overlap seed

![Step 1](steps/01-overlap-seed.png)

**Caption (transcript):** Abacus-lite processes movables by increasing original x. From the same overlap seed as overlap removal, it tries each row and picks the placement with minimum L1 displacement.

**Slide bullets:**

- Order: A, B, C, … by x
- Try every row for each cell
- Leftmost legal site on row

**On-screen metrics:**

```
seed: OVERLAP_PLACEMENT
legal: false
```

## Step 2 — Process by x: try each row

![Step 2](steps/02-try-rows.png)

**Caption (transcript):** Cell A tries rows zero, two, four—picks row two at x four (zero displacement). B chooses row zero at x four. C chooses row four at x four. Cross-row spread beats single-row pack.

**Slide bullets:**

- Per-cell row trial
- Min L1 from origin
- Tie-break: smaller x

**On-screen metrics:**

```
A → row 2
B → row 0
C → row 4
```

## Step 3 — Result: A@4,2 B@4,0 C@4,4

![Step 3](steps/03-abacus-result.png)

**Caption (transcript):** Final Abacus layout: A on middle row, B on bottom, C on top—all at x equals four but on different rows. D, E, F stay at their seed coordinates.

**Slide bullets:**

- A @ (4,2)
- B @ (4,0)
- C @ (4,4)

**On-screen metrics:**

```
disp: 4
HPWL: 38
legal: true
```

## Step 4 — Lower displacement than Tetris

![Step 4](steps/04-vs-overlap-removal.png)

**Caption (transcript):** Abacus displacement is four versus six for overlap removal / Tetris on this seed. You pay three HPWL points—thirty-eight versus thirty-two—for staying closer to global targets.

**Slide bullets:**

- abacus disp: 4
- tetris disp: 6
- HPWL tradeoff: 38 vs 32

**On-screen metrics:**

```
abacusDisp: 4
tetrisDisp: 6
abacusHpwl: 38
```

## Step 5 — Abacus minimizes movement

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Abacus is the detailed legalizer in this course: try rows, pick min displacement. Use it when staying near global coordinates matters more than the last HPWL point.

**Slide bullets:**

- Cross-row assignment
- disp 4 golden
- Next: Tetris contrast

**On-screen metrics:**

```
abacusLegal: true
```

