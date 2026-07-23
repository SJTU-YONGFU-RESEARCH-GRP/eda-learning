# Multilevel partitioning — step-by-step (for slides / transcript)

**Module:** `module04-01-multilevel-partition`  
**Lab / algo:** `multilevel-partition`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=multilevel-partition&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Coarsen with greedy merge

![Step 1](steps/01-coarsen.png)

**Caption (transcript):** Multilevel V-cycle contracts the graph via greedy pair merge to coarseK=2. Supernodes C1={A,B,C} and C2={D,E} capture community structure.

**Slide bullets:**

- Greedy heaviest-edge merges
- Log each contraction
- Coarse graph has 2 clusters

**On-screen metrics:**

```
coarseK=2
labels: C1, C2
```

## Step 2 — Project to fine bipartition

![Step 2](steps/02-project.png)

**Caption (transcript):** Map coarse clusters to sides 0/1: ABC→0, DE→1. Projected seed ABC|DE already has cutsize 3 — unlike BAD_SEED's cut of 12.

**Slide bullets:**

- Projection preserves membership
- Good global seed from coarsening
- Ready for local FM refine

**On-screen metrics:**

```
project: ABC|DE
cutsize: 3
BAD_SEED cut: 12
```

## Step 3 — FM refine on fine graph

![Step 3](steps/03-refine.png)

**Caption (transcript):** FM polishes the projected seed. On TINY_GRAPH the projection is already optimal — refine keeps ABC|DE at cutsize 3.

**Slide bullets:**

- Single-vertex moves with rollback
- Local search on fine graph
- No improvement needed here

**On-screen metrics:**

```
refine: ABC|DE
cutsize: 3
```

## Step 4 — Final P0/P1 labels

![Step 4](steps/04-final.png)

**Caption (transcript):** Output renames sides to P0/P1 for placers. Final communities ABC|DE with cutsize 3 — multilevel beats refining a random bad seed alone.

**Slide bullets:**

- P0 = ABC, P1 = DE
- cutsize: 3
- V-cycle complete

**On-screen metrics:**

```
final: ABC|DE
cutsize: 3
labels: P0, P1
```

## Step 5 — Multilevel V-cycle mindset

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Coarsen for global structure, project, refine locally. Real placers nest this in repeated V-cycles with hyperedges and balance — this lab is the skeleton.

**Slide bullets:**

- coarsen → project → refine
- Beats BAD_SEED cut 12 → 3
- Industry default for large netlists

**On-screen metrics:**

```
Starter golden: cut=3
```

