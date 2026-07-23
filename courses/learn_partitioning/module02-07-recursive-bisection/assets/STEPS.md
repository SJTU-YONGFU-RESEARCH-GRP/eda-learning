# Recursive bisection — step-by-step (for slides / transcript)

**Module:** `module02-07-recursive-bisection`  
**Lab / algo:** `recursive-bisection`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=recursive-bisection&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Start: one part, k=4 target

![Step 1](steps/01-start.png)

**Caption (transcript):** Recursive bisection builds k-way partitions by repeated 2-way splits. Target k=4 on TINY_GRAPH: bisect the largest part until four labels exist.

**Slide bullets:**

- Always split the largest current part
- Inner split uses spectral bisection
- History logs each bisection step

**On-screen metrics:**

```
target k=4
step 0: ABCDE cut=0
```

## Step 2 — Bisect 1: ABC|DE cut 3

![Step 2](steps/02-split-1.png)

**Caption (transcript):** First spectral split on the whole graph yields ABC|DE — same golden bipartition with cutsize 3. Two parts remain; need two more splits.

**Slide bullets:**

- Largest part = all five nodes
- Spectral → ABC vs DE
- Heavy edges A–B, D–E internal

**On-screen metrics:**

```
step 1: ABC|DE
cutsize: 3
k=2 so far
```

## Step 3 — Bisect 2: split ABC → AB|C

![Step 3](steps/03-split-2.png)

**Caption (transcript):** Largest part ABC (size 3) is bisected next. A and B stay together (w=5); C becomes its own part. Three parts: AB, C, DE.

**Slide bullets:**

- Split ABC via induced spectral
- A–B heavy edge survives
- cutsize rises to 8

**On-screen metrics:**

```
step 2: AB|C|DE
cutsize: 8
k=3
```

## Step 4 — Bisect 3: split DE → D|E

![Step 4](steps/04-split-3.png)

**Caption (transcript):** Largest remaining part DE is bisected, cutting the weight-5 D–E edge. Final four parts: AB, C, D, E singleton aside from AB pair.

**Slide bullets:**

- Split DE — pays the heavy edge
- k=4 reached
- AB still uncut

**On-screen metrics:**

```
step 3: AB|C|D|E
cutsize: 13
k=4
```

## Step 5 — Recursive bisection tradeoff

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** k=4 costs cut 13 because splitting DE destroys the weight-5 edge. k=3 stops earlier at AB|C|DE cut 8 — fewer splits can mean lower total cut.

**Slide bullets:**

- Largest-part-first scheduling
- Each split is local spectral
- Compare k=3 (cut 8) vs k=4 (cut 13)

**On-screen metrics:**

```
Final: AB|C|D|E cut=13
k=3 reference: cut=8
```

