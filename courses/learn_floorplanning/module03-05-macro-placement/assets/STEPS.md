# Hard macro / fixed-block placement — step-by-step (for slides / transcript)

**Module:** `module03-05-macro-placement`  
**Lab / algo:** `macro-placement`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=macro-placement&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Free golden has movable D

![Step 1](steps/01-free.png)

**Caption (transcript):** In the free golden packing, D sits at zero comma two above A. Nothing is flagged as a hard macro yet.

**Slide bullets:**

- D at (0,2)
- All blocks movable
- legal: true

**On-screen metrics:**

```
mode: free
D@(0,2)
```

## Step 2 — Fix macro D at (0,0)

![Step 2](steps/02-fix-d.png)

**Caption (transcript):** Macro mode pins hard block D at the origin and marks it macro true. Soft and standard cells must pack around that fixed rectangle.

**Slide bullets:**

- D fixed at (0,0)
- D.macro = true
- Size stays 3×1

**On-screen metrics:**

```
D@(0,0)
macro: true
```

## Step 3 — Pack A–E around the macro

![Step 3](steps/03-pack-rest.png)

**Caption (transcript):** A stacks above D; B, C, and E fill to the right. The macro packing differs from the free golden—D no longer sits at zero comma two.

**Slide bullets:**

- A.y >= D.h
- Differs from free D position
- Five modules still present

**On-screen metrics:**

```
A@(0,1)
legal check next
```

## Step 4 — Macro packing is legal

![Step 4](steps/04-legal.png)

**Caption (transcript):** Despite the fixed block, the packing stays legal: no overflow, no overlaps. Fixed macros constrain search but do not excuse illegality.

**Slide bullets:**

- legal: true
- D remains 3×1
- Macro flag preserved

**On-screen metrics:**

```
legal: true
```

## Step 5 — Macros first, then cells

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Industrial flows often place large macros before standard cells. Treat fixed rectangles as hard constraints, then optimize the rest.

**Slide bullets:**

- Fix macros early
- Pack around them
- Next: hierarchical clusters

**On-screen metrics:**

```
starter: D macro @ (0,0)
```

