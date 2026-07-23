# Platform tools catalog

Browser labs for **eda_learning**. Serve with:

```bash
python -m http.server 8080 --directory platform
```

## Clustering & refinement

| Tool | Starter (reference) | Challenges | Status |
|------|---------------------|------------|--------|
| `affinity-metrics` | Edge-weight top A–B@5; shared A–B@6 | **10** | **Shipped** |
| `greedy-pair-merge` | K=2 → cutsize 3, {A,B,C}/{D,E} | **10** | **Shipped** |
| `size-constrained-agglomerative` | K=2 capacity=2 → AB\|C\|DE cut 8 | **10** | **Shipped** |
| `label-propagation` | Async LP → iters 2, cutsize 3 | **10** | **Shipped** |
| `spectral-bisection` | Fiedler → cutsize 3, ABC\|DE | **10** | **Shipped** |
| `kernighan-lin` | Bad seed 12 → KL → 3 via (A,D) | **10** | **Shipped** |
| `fiduccia-mattheyses` | Same seed → FM → 3 | **10** | **Shipped** |
| `multilevel-clustering` | Coarsen+FM → P0/P1 cut 3 | **10** | **Shipped** |
| `hypergraph-clustering` | K=2 hyper cut 1, ABC\|DE | **10** | **Shipped** |
| `congestion-aware-clustering` | λ=5 → plain 5, pen 0 | **10** | **Shipped** |
| `timing-aware-clustering` | Timing FM → plain 3, weighted 7 | **10** | **Shipped** |

Each tool **auto-loads the starter example** as a worked reference. Challenges use **Start / Hint / Check / Next**; **Load starter example** restores the reference at any time.

## Partitioning

| Tool | Starter (reference) | Challenges | Status |
|------|---------------------|------------|--------|
| `cutsize-balance` | Bad seed cut 12, ratio 2/3; golden cut 3 | **10** | **Shipped** |
| `initial-bipartition` | Grow from D → ABC\|DE cut 3 | **10** | **Shipped** |
| `kl-partition` | Bad seed 12 → KL → 3 via (A,D) | **10** | **Shipped** |
| `fm-partition` | Same seed → FM → 3 via D then A | **10** | **Shipped** |
| `spectral-partition` | Fiedler → cutsize 3, ABC\|DE | **10** | **Shipped** |
| `recursive-bisection` | k=3 → AB\|C\|DE cut 8 | **10** | **Shipped** |
| `multiway-partition` | Recursive cut 8 vs round-robin 18 | **10** | **Shipped** |
| `terminal-propagation` | Terminals A/E → ABC\|DE cut 3 | **10** | **Shipped** |
| `hypergraph-partition` | Seed hyper cut 6 → FM → 1 | **10** | **Shipped** |
| `multilevel-partition` | V-cycle → P0/P1 cut 3 | **10** | **Shipped** |

Shared helpers: `platform/assets/partitioning-core.js` (imports graph utils / KL / FM / spectral from `clustering-core.js`).

## Floorplanning

| Tool | Starter (reference) | Challenges | Status |
|------|---------------------|------------|--------|
| `fixed-outline` | Bad overflow vs golden legal 10×8 | **10** | **Shipped** |
| `area-deadspace` | Area 23, outline 80, deadspace 57, density 0.2875 | **10** | **Shipped** |
| `slicing-floorplan` | Polish `A D H B V C V E V` → BB 9×3 | **10** | **Shipped** |
| `bstar-tree` | A root; left B→C→E; right D above | **10** | **Shipped** |
| `sequence-pair` | pos `A B C E D` / neg `D A B C E` | **10** | **Shipped** |
| `simulated-annealing-fp` | Bad cost ≥1000 → improve to golden | **10** | **Shipped** |
| `soft-module-sizing` | Soft A 3×2 → reshape 2×3 area 6 | **10** | **Shipped** |
| `macro-placement` | Macro D fixed (0,0) then pack rest | **10** | **Shipped** |
| `hierarchical-floorplan` | Clusters AB \| CDE @ x=5 | **10** | **Shipped** |
| `pin-assignment` | Golden pins on all four sides | **10** | **Shipped** |

Shared helpers: `platform/assets/floorplanning-core.js`.

## Algorithm walkthroughs (PPT / transcript)

Step-by-step teaching frames (graph + caption + bullets):

- Viewer: [`tools/algorithm-walkthrough/`](tools/algorithm-walkthrough/) — `?algo=<lab-id>&step=N`
- Media rebuild **in WSL**: `bash courses/learn_clustering/scripts/build_all_media.sh`
- Index: [`courses/learn_clustering/docs/WALKTHROUGHS.md`](../courses/learn_clustering/docs/WALKTHROUGHS.md)
