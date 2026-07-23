# Slicing tree / polish expression packing — step-by-step (for slides / transcript)

**Module:** `module02-01-slicing-floorplan`  
**Lab / algo:** `slicing-floorplan`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=slicing-floorplan&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Polish expression encodes cuts

![Step 1](steps/01-polish.png)

**Caption (transcript):** A slicing floorplan is a tree of through-cuts. Postfix polish A D H B V C V E V stacks A under D, then places B, C, and E to the right with vertical cuts.

**Slide bullets:**

- Operands = modules
- H = horizontal cut (stack)
- V = vertical cut (side by side)

**On-screen metrics:**

```
polish: A D H B V C V E V
tokens: 9
```

## Step 2 — A D H stacks height 3

![Step 2](steps/02-stack-ad.png)

**Caption (transcript):** A is three by two; D is three by one. An H cut stacks D above A into a three by three block at the lower left.

**Slide bullets:**

- A at (0,0)
- D at (0,2)
- composite 3×3

**On-screen metrics:**

```
after A D H: w=3 h=3
```

## Step 3 — V attaches B on the right

![Step 3](steps/03-attach-b.png)

**Caption (transcript):** Next V places B beside the A–D stack. Bounding width becomes five; height stays three.

**Slide bullets:**

- B at x=3
- BB width 5
- height still 3

**On-screen metrics:**

```
after … B V: w=5 h=3
```

## Step 4 — Full polish packs BB 9×3

![Step 4](steps/04-full.png)

**Caption (transcript):** Adding C and E with more V cuts finishes the golden polish. Bounding box is nine by three—legal inside the ten-by-eight outline.

**Slide bullets:**

- Final BB: 9×3
- Fits outline 10×8
- Five modules placed

**On-screen metrics:**

```
bb: 9×3
legal: true
```

## Step 5 — Slicing cannot make wheels

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Not every packing is slicing. Wheel topologies need non-slicing codes like B-star or sequence pair—next labs. For slicing, polish plus H/V evaluation is enough.

**Slide bullets:**

- Golden polish → BB 9×3
- legal: true
- Non-slicing needs other reps

**On-screen metrics:**

```
starter golden: BB 9×3
```

