# Greedy pair merge — step-by-step (for slides / transcript)

**Module:** `module01-03-greedy-pair-merge`  
**Lab / algo:** `greedy-pair-merge`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=greedy-pair-merge&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Every node starts alone

![Step 1](steps/01-singletons.png)

**Caption (transcript):** Agglomerative clustering begins with K=5 singletons. We repeatedly merge the highest-affinity legal pair until we hit target K.

**Slide bullets:**

- Target here: K=2
- No capacity limit in the reference run
- Priority = current edge-weight ranking

**On-screen metrics:**

```
K=5 → aim for K=2
cutsize (all separate): 18
```

## Step 2 — Merge 1: contract A–B

![Step 2](steps/02-merge-ab.png)

**Caption (transcript):** Heaviest edge is A–B at weight 5, so they merge first into a supernode. That protects the strongest connection immediately.

**Slide bullets:**

- Pick top legal pair on current graph
- Contract into a cluster
- Recompute edges to the new supernode

**On-screen metrics:**

```
merge: A–B @ 5 → C0
clusters: AB | C | D | E
```

## Step 3 — Merge 2: absorb C into AB

![Step 3](steps/03-absorb-c.png)

**Caption (transcript):** After contraction, C connects to {A,B} with combined weight 5. That ties D–E; alphabetical order merges C next, forming {A,B,C}.

**Slide bullets:**

- Supernode edges sum parallel connections
- C joins the A–B community
- Still two merges left toward K=2

**On-screen metrics:**

```
merge: C–C0 @ 5
clusters: ABC | D | E
cutsize now: 8
```

## Step 4 — Merge 3: contract D–E

![Step 4](steps/04-merge-de.png)

**Caption (transcript):** Last merge joins D–E at weight 5. We now have exactly two clusters: {A,B,C} versus {D,E}.

**Slide bullets:**

- Reached target K=2
- Heavy edges sit inside clusters
- Only weak bridge edges remain cut

**On-screen metrics:**

```
merge: D–E @ 5
clusters: ABC | DE
cutsize: 3
```

## Step 5 — Result: cutsize 3

![Step 5](steps/05-final-cut.png)

**Caption (transcript):** Cut edges are C–D (2) and C–E (1). Greedy locked in the natural communities without backtracking—fast, but capacity rules can block this path.

**Slide bullets:**

- Golden: ABC|DE, cut=3
- Capacity=2 would forbid size-3 {A,B,C}
- Refinement labs repair worse seeds later

**On-screen metrics:**

```
Final parts: ABC|DE
cutsize = 2+1 = 3
```

