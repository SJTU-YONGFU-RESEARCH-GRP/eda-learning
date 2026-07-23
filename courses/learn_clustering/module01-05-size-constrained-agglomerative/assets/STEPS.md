# Size-constrained agglomerative clustering — step-by-step (for slides / transcript)

**Module:** `module01-05-size-constrained-agglomerative`  
**Lab / algo:** `size-constrained-agglomerative`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=size-constrained-agglomerative&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Capacity blocks illegal merges

![Step 1](steps/01-capacity-rule.png)

**Caption (transcript):** Same greedy heaviest-edge merge, but refuse any pair whose sizes sum above capacity. With capacity=2 on unit nodes, size-3 clusters are illegal.

**Slide bullets:**

- Target K=2 with capacity=2
- Legal merges: size ≤ 2
- Unconstrained would absorb C into AB

**On-screen metrics:**

```
capacity=2
K=2
start: five singletons
```

## Step 2 — Merge A–B (still legal)

![Step 2](steps/02-merge-ab.png)

**Caption (transcript):** Heaviest edge A–B at weight 5 merges first. Combined size is 2 — exactly at capacity. C cannot join next.

**Slide bullets:**

- First merge identical to unconstrained
- AB size = 2
- Next heaviest legal pair is D–E

**On-screen metrics:**

```
merge: A–B @ 5
clusters: AB | C | D | E
```

## Step 3 — Merge D–E; C stays alone

![Step 3](steps/03-merge-de.png)

**Caption (transcript):** D–E merges at weight 5. Absorbing C into AB would create size 3 and is rejected, so we stop with three clusters even though target K=2.

**Slide bullets:**

- Capacity stalls further merges
- Stuck at K=3 > target
- C is an isolated bridge node

**On-screen metrics:**

```
merge: D–E @ 5
parts: AB|C|DE
cutsize: 8
```

## Step 4 — Result: cutsize 8

![Step 4](steps/04-cut-8.png)

**Caption (transcript):** Cut edges include A–C, B–C, C–D, C–E. Capacity cost is +5 versus the unconstrained cut of 3.

**Slide bullets:**

- Golden: AB|C|DE, cut=8
- Trade balance for worse cut
- Relax capacity to 3 to recover ABC|DE

**On-screen metrics:**

```
cutsize: 8
vs unconstrained: 3
```

## Step 5 — Why capacity matters in EDA

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Floorplanning and clustering often cap cluster area. Teaching point: constraints change the greedy path — you may never reach the unconstrained communities.

**Slide bullets:**

- Capacity is a hard filter on merges
- May miss global cut optima
- Refinement / multilevel can help later

**On-screen metrics:**

```
Starter golden: cut=8 with cap=2
```

