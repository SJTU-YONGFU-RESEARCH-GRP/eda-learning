# B*-tree floorplan representation — step-by-step (for slides / transcript)

**Module:** `module02-03-bstar-tree`  
**Lab / algo:** `bstar-tree`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=bstar-tree&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Root A at the origin

![Step 1](steps/01-root.png)

**Caption (transcript):** B-star packing places the root at the lower left. A lands at zero comma zero with size three by two. Left children go right-of; right children go above via the contour.

**Slide bullets:**

- Root = lower-left
- Left child = right-of parent
- Right child = above on contour

**On-screen metrics:**

```
A at (0,0)
tree root: A
```

## Step 2 — Left chain B→C→E

![Step 2](steps/02-left-chain.png)

**Caption (transcript):** The left spine walks rightward: B at x equals three, then C, then E. Contour heights track the skyline so later modules sit tightly.

**Slide bullets:**

- B.x = A.x + A.w = 3
- C and E continue right
- Contour updates each place

**On-screen metrics:**

```
B at (3,0)
C at (5,0)
E at (7,0)
```

## Step 3 — Right child D above A

![Step 3](steps/03-right-d.png)

**Caption (transcript):** D is the right child of A, so it packs above A on the contour. Its y is at least two—A's height—keeping the tree geometry honest.

**Slide bullets:**

- D.y >= A.h
- Same x as A branch
- Still non-overlapping

**On-screen metrics:**

```
D at (0,2)
A.h=2
```

## Step 4 — Full B* pack is legal

![Step 4](steps/04-legal.png)

**Caption (transcript):** All five modules are placed. The packing is legal inside ten by eight. Perturbing the tree—swap, rotate, move—will feed simulated annealing later.

**Slide bullets:**

- Five modules placed
- legal: true
- Tree is a packing code, not netlist

**On-screen metrics:**

```
legal: true
modules: A–E
```

## Step 5 — B* is compact and mutable

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** B-star stores adjacency for packing, not connectivity. Get left and right semantics right, keep the contour correct, and you have a fast neighbor generator for search.

**Slide bullets:**

- Left/right geometry is the bug magnet
- Contour must update on place
- Next: sequence-pair alternative

**On-screen metrics:**

```
starter golden: legal B* pack
```

