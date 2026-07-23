# Multiway partitioning — step-by-step (for slides / transcript)

**Module:** `module03-01-multiway-partition`  
**Lab / algo:** `multiway-partition`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=multiway-partition&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — k-way vs naive assignment

![Step 1](steps/01-problem.png)

**Caption (transcript):** Real placers need k>2 parts. Recursive bisection respects graph structure; naive round-robin assigns nodes by index mod k — often catastrophic cut.

**Slide bullets:**

- k=3 on TINY_GRAPH
- Recursive: repeated bisection
- Round-robin: A→0, B→1, C→2, …

**On-screen metrics:**

```
target k=3
same graph, two strategies
```

## Step 2 — Recursive: AB|C|DE cut 8

![Step 2](steps/02-recursive.png)

**Caption (transcript):** Recursive bisection to k=3 first splits ABC|DE (cut 3), then bisects ABC → AB|C|DE. A–B and D–E stay uncut; total cutsize is 8.

**Slide bullets:**

- Structure-aware splits
- A,B share a part
- D,E share a part

**On-screen metrics:**

```
parts: AB|C|DE
cutsize: 8
3 labels
```

## Step 3 — Round-robin: AD|BE|C cut 18

![Step 3](steps/03-roundrobin.png)

**Caption (transcript):** Alphabetical round-robin puts A,D on part 0; B,E on part 1; C alone on part 2. Almost every edge crosses — cutsize 18.

**Slide bullets:**

- A and B on different parts
- D and E on different parts
- Ignores connectivity entirely

**On-screen metrics:**

```
parts: AD|BE|C
cutsize: 18
gap vs recursive: 10
```

## Step 4 — Structure beats indexing

![Step 4](steps/04-compare.png)

**Caption (transcript):** Round-robin cuts A–B(5) and D–E(5) — the two strongest edges. Recursive keeps them internal and pays only bridge cuts through C.

**Slide bullets:**

- 18 − 8 = 10 cut gap
- Same k, wildly different quality
- Why tools use recursive / multilevel

**On-screen metrics:**

```
recursive: 8
round-robin: 18
```

## Step 5 — Multiway literacy

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Direct k-way FM exists in production tools, but recursive bisection is the teaching baseline: global structure emerges from local 2-way splits.

**Slide bullets:**

- Never round-robin a netlist
- Recursive k=3: AB|C|DE
- Multilevel wraps the same idea

**On-screen metrics:**

```
Starter golden: recursive cut=8
```

