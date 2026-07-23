# Hypergraph partitioning — step-by-step (for slides / transcript)

**Module:** `module03-05-hypergraph-partition`  
**Lab / algo:** `hypergraph-partition`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=hypergraph-partition&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Nets are hyperedges

![Step 1](steps/01-nets.png)

**Caption (transcript):** TINY_HYPERGRAPH has four nets: n1={A,B,C} w=3, n2={D,E}, n3={C,D}, n4={A,B}. Cut counts whole nets spanning ≥2 sides — not pairwise edges alone.

**Slide bullets:**

- Hyperedge cut if pins span sides
- n1 pulls ABC together
- Drawing uses clique expansion

**On-screen metrics:**

```
4 hyperedges
5 nodes
```

## Step 2 — Bad seed: hyperedge cut 6

![Step 2](steps/02-bad-seed.png)

**Caption (transcript):** BAD_SEED AE|BCD cuts nets n1(3), n2(2), and n4(1) — hyperedge cut 6. Same seed as graph labs, worse hyper objective.

**Slide bullets:**

- n1 spans A vs B,C
- n2 spans D,E vs B,C,D
- Pairwise cut ≠ hyper cut

**On-screen metrics:**

```
seed: AE|BCD
hyperedge cut: 6
```

## Step 3 — FM on clique expansion

![Step 3](steps/03-fm-run.png)

**Caption (transcript):** Hypergraph FM clique-expands nets to pair edges, then runs standard FM from the bad seed. Objective reports hyperedge cut on the original nets.

**Slide bullets:**

- Clique expansion for moves
- Score hyperedge cut after moves
- Same FM kernel as graph labs

**On-screen metrics:**

```
engine: FM on expansion
seed hyper cut: 6
```

## Step 4 — Refined ABC|DE: hyper cut 1

![Step 4](steps/04-refined.png)

**Caption (transcript):** FM reaches ABC|DE. Only bridge net n3={C,D} crosses sides — hyperedge cut 1. n1, n2, n4 stay uncut.

**Slide bullets:**

- n1 ABC internal
- n2 DE internal
- n3 is the sole cut net

**On-screen metrics:**

```
parts: ABC|DE
hyperedge cut: 1
pair cut: 1
```

## Step 5 — Why hypergraphs in partition

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Real netlists are hypergraphs. Modeling nets honestly changes the cut objective — clique expansion is for moves, hyper cut is for scoring.

**Slide bullets:**

- 6 → 1 hyper cut improvement
- Multi-pin nets dominate affinity
- Production tools use native hyper FM

**On-screen metrics:**

```
Starter golden: hyper cut=1
```

