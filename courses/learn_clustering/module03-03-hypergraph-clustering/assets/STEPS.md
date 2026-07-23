# Hypergraph clustering — step-by-step (for slides / transcript)

**Module:** `module03-03-hypergraph-clustering`  
**Lab / algo:** `hypergraph-clustering`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=hypergraph-clustering&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Nets are hyperedges

![Step 1](steps/01-nets.png)

**Caption (transcript):** TINY_HYPERGRAPH has four nets: multi-pin n1={A,B,C} weight 3, pair n2={D,E}, bridge n3={C,D}, and n4={A,B}. Cut counts whole nets, not pairs.

**Slide bullets:**

- Hyperedge cut if pins span ≥2 clusters
- n1 pulls ABC together
- Graph clique expansion would look different

**On-screen metrics:**

```
4 hyperedges
5 nodes
```

## Step 2 — Affinity = shared pin weight

![Step 2](steps/02-affinity.png)

**Caption (transcript):** Greedy merge scores pairs by summed weights of hyperedges that contain both endpoints. A–B and A–C–B affinities favor the ABC community.

**Slide bullets:**

- pair_affinity(a,b) = Σ w over shared nets
- Contract highest affinity pair
- Rewrite pins onto supernodes

**On-screen metrics:**

```
priority: co-occurrence on nets
```

## Step 3 — Merge down to K=2

![Step 3](steps/03-merge-k2.png)

**Caption (transcript):** Repeated contraction yields two clusters covering ABC and DE. Only bridge net n3 is cut.

**Slide bullets:**

- Target K=2
- ABC stays on one supernode family
- DE on the other

**On-screen metrics:**

```
parts: ABC|DE
hyperedge cut: 1
```

## Step 4 — Hyperedge cut = 1

![Step 4](steps/04-cut-1.png)

**Caption (transcript):** Golden: hyperedge cut 1 (n3 only). Pairwise graph cut on a clique expansion would score differently — that is the teaching contrast.

**Slide bullets:**

- n1, n2, n4 uncut
- n3 cut → +1
- Objective matches netlist reality

**On-screen metrics:**

```
hyperedge cut: 1
parts: ABC|DE
```

## Step 5 — Why hypergraphs in EDA

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Real nets touch many cells. Modeling them as hyperedges keeps the cut objective honest. Browser view clique-expands only for drawing.

**Slide bullets:**

- Cut nets, not just edges
- Multi-pin nets dominate affinity
- Next: congestion / timing objectives

**On-screen metrics:**

```
Starter golden: cut=1
```

