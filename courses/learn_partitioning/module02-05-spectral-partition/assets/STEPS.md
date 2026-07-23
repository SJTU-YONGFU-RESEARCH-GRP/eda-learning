# Spectral bipartition — step-by-step (for slides / transcript)

**Module:** `module02-05-spectral-partition`  
**Lab / algo:** `spectral-partition`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=spectral-partition&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Build the Laplacian

![Step 1](steps/01-laplacian.png)

**Caption (transcript):** Spectral methods read connectivity from the graph Laplacian L = D − A. The Fiedler vector (second eigenvector) encodes a soft cut.

**Slide bullets:**

- Tiny n → pure shifted inverse iteration
- No external linear-algebra library
- Same TINY_GRAPH as other labs

**On-screen metrics:**

```
nodes: 5
edges: 6
```

## Step 2 — Sort by Fiedler value

![Step 2](steps/02-fiedler-order.png)

**Caption (transcript):** After iteration, nodes order low→high as E, D, C, B, A. E is most negative; A is most positive — natural bipartition candidates.

**Slide bullets:**

- Order endpoints: E lowest, A highest
- Values are continuous soft memberships
- Balance filter rejects lopsided prefixes

**On-screen metrics:**

```
order: E < D < C < B < A
```

## Step 3 — Sweep prefixes for best cut

![Step 3](steps/03-sweep-cut.png)

**Caption (transcript):** Try every balanced prefix of the order as side 0. The winning split is {D,E} vs {A,B,C} with cutsize 3.

**Slide bullets:**

- Balance window ≈ 20–80% size
- Pick minimum cut among legal splits
- Golden cut = 3

**On-screen metrics:**

```
best parts: DE | ABC
cutsize: 3
```

## Step 4 — Result ABC|DE

![Step 4](steps/04-final.png)

**Caption (transcript):** Spectral recovers the same communities as unconstrained greedy and grow-from-D. Global eigenvectors find the cut without greedy merges.

**Slide bullets:**

- parts: ABC|DE
- Heavy edges internal
- Bridge C–D/C–E cut

**On-screen metrics:**

```
cutsize: 3
parts: ABC|DE
```

## Step 5 — When spectral helps

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Spectral is a strong initializer for bipartition. On larger chips it pairs with multilevel; here the tiny instance grades against golden cut 3.

**Slide bullets:**

- Good seed for KL/FM
- Balance via sweep, not afterthought
- Used inside recursive bisection too

**On-screen metrics:**

```
Golden: cut=3, E lowest / A highest
```

