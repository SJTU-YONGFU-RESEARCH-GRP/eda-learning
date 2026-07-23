# Label propagation clustering — step-by-step (for slides / transcript)

**Module:** `module02-01-label-propagation`  
**Lab / algo:** `label-propagation`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=label-propagation&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Initialize: each node is its own label

![Step 1](steps/01-init.png)

**Caption (transcript):** Label propagation starts with five communities. Every node votes using weighted neighbor labels; async updates walk nodes in order A…E.

**Slide bullets:**

- labels[v] = v initially
- No global objective—local majority votes
- Order matters for ties

**On-screen metrics:**

```
labels: A,B,C,D,E
num_clusters: 5
```

## Step 2 — Each node adopts the winning neighbor label

![Step 2](steps/02-vote-idea.png)

**Caption (transcript):** For a node v, sum edge weights by neighbor label and take the best. Dense A–B–C and D–E pull neighbors onto shared labels quickly.

**Slide bullets:**

- vote(label) = Σ w(v, nbr) for nbrs with that label
- Ties broken lexicographically
- One sweep = one iteration

**On-screen metrics:**

```
Focus: A hears B strongly (w=5)
D hears E strongly (w=5)
```

## Step 3 — After iteration 1: already clustered

![Step 3](steps/03-after-iter1.png)

**Caption (transcript):** One async sweep flips A and C onto B, and D onto E. Communities {A,B,C} and {D,E} appear immediately on this tiny graph.

**Slide bullets:**

- 3 labels changed in iter 1
- A,B,C → label B
- D,E → label E

**On-screen metrics:**

```
labels: {"A":"B","B":"B","C":"B","D":"E","E":"E"}
cutsize: 3
```

## Step 4 — Iteration 2: no changes → stop

![Step 4](steps/04-iter2-stable.png)

**Caption (transcript):** A second sweep finds zero flips, so the algorithm reports iters_to_stable=2. Stability, not a cutsize objective, is the stopping rule.

**Slide bullets:**

- changed == 0 ⇒ halt
- Golden: iters=2, cutsize=3
- Same communities greedy found

**On-screen metrics:**

```
iters_to_stable: 2
num_clusters: 2
cutsize: 3
```

## Step 5 — When LP helps in EDA flows

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** LP is a cheap community detector—great as a seed or coarsening hint. It does not enforce balance or timing; refinement (KL/FM) still matters on hard instances.

**Slide bullets:**

- Fast local updates
- Sensitive to node order
- Use with capacity / cut objectives downstream

**On-screen metrics:**

```
Reference communities: ABC | DE
```

