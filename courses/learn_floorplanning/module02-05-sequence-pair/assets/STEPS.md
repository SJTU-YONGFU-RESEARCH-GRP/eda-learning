# Sequence-pair representation — step-by-step (for slides / transcript)

**Module:** `module02-05-sequence-pair`  
**Lab / algo:** `sequence-pair`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=sequence-pair&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Two permutations encode geometry

![Step 1](steps/01-seqs.png)

**Caption (transcript):** Sequence pair uses a positive and a negative permutation of the same modules. Ours are pos A B C E D and neg D A B C E—five ids each, same set.

**Slide bullets:**

- pos + neg are permutations
- Same five module ids
- Constraints → longest-path pack

**On-screen metrics:**

```
pos: A B C E D
neg: D A B C E
```

## Step 2 — Horizontal constraints set x

![Step 2](steps/02-h-rules.png)

**Caption (transcript):** Module i is left of j when i appears before j in both sequences. Longest-path packing pushes each block as far left as those constraints allow.

**Slide bullets:**

- i left of j if pos(i)<pos(j) and neg(i)<neg(j)
- x = longest path over left-of edges

**On-screen metrics:**

```
A tends left
E tends right
```

## Step 3 — Vertical constraints set y

![Step 3](steps/03-v-rules.png)

**Caption (transcript):** Module i is below j when i precedes j in pos but follows in neg. That fills y coordinates without overlaps for a feasible pair.

**Slide bullets:**

- i below j if pos(i)<pos(j) and neg(i)>neg(j)
- y = longest path over below edges

**On-screen metrics:**

```
D.y=3
D can sit above the bottom row
```

## Step 4 — Golden SP packs legally

![Step 4](steps/04-legal.png)

**Caption (transcript):** Evaluating the golden sequences places all five modules with non-negative coordinates and a legal packing inside the outline.

**Slide bullets:**

- Five modules placed
- legal: true
- Coords ≥ 0

**On-screen metrics:**

```
legal: true
ids: A–E
```

## Step 5 — SP neighbors are permutation moves

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Annealing on sequence pair swaps or rotates entries in pos and neg. Feasibility stays geometric; cost can be deadspace plus wirelength.

**Slide bullets:**

- Neighbor = edit permutations
- Pack via longest paths
- Next: SA search on packings

**On-screen metrics:**

```
starter golden: legal SP
```

