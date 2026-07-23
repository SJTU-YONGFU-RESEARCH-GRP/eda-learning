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

Interactive labs: **you place / edit**, then Check. Workspace starts empty or seeded — **not** the golden.
**Reveal golden (study)** is optional and does not clear challenges.

| Tool | Learner actions | Challenges | Status |
|------|-----------------|------------|--------|
| `fixed-outline` | Place A–E on 10×8 grid; legality | **10** | **Shipped** |
| `area-deadspace` | Legal pack → read 23 / 80 / 57 / 0.2875 | **10** | **Shipped** |
| `slicing-floorplan` | Build polish tokens → Evaluate | **10** | **Shipped** |
| `bstar-tree` | Pack B*-tree (then inspect) | **10** | **Shipped** |
| `sequence-pair` | Build pos/neg → Pack | **10** | **Shipped** |
| `simulated-annealing-fp` | Fix bad seed / swap until cost &lt; 1000 | **10** | **Shipped** |
| `soft-module-sizing` | Reshape A 3×2↔2×3, then pack | **10** | **Shipped** |
| `macro-placement` | D locked; place around macro | **10** | **Shipped** |
| `hierarchical-floorplan` | Pack hierarchy or place AB \| CDE | **10** | **Shipped** |
| `pin-assignment` | Add pins on four sides | **10** | **Shipped** |

Shared helpers: `platform/assets/floorplanning-core.js`, `platform/assets/floorplanning-lab.js`.

## Placement

| Tool | Starter (reference) | Challenges | Status |
|------|---------------------|------------|--------|
| `hpwl-metrics` | Starter HPWL **52**; golden **14** | **10** | **Shipped** |
| `net-models` | Golden ABCD bbox 4; clique **16**; star-from-A **8** | **10** | **Shipped** |
| `force-directed-place` | Starter 52 → force ≈ **18.7** | **10** | **Shipped** |
| `quadratic-place` | Pads A,D fixed → HPWL **48** | **10** | **Shipped** |
| `analytical-place` | Force/quad + density spread → ≈ **48.1** | **10** | **Shipped** |
| `sa-placement` | Seed 42 best ≈ **49.6** (acc 44 / rej 16) | **10** | **Shipped** |
| `density-bins` | 2×2 cap1 overflow **2**; golden cap2 overflow **1** | **10** | **Shipped** |
| `spread-legalize-lite` | Overlap minDist 0 → spread ≥ **0.5** | **10** | **Shipped** |
| `timing-driven-place` | Timing HPWL **116** → golden **30** (net4×5) | **10** | **Shipped** |

Shared helpers: `platform/assets/placement-core.js`, `platform/assets/placement-ui.js` (reuses `createChallengeLab` from `clustering-ui.js`).

## Static timing analysis (STA)

| Tool | Starter (reference) | Challenges | Status |
|------|---------------------|------------|--------|
| `timing-graph` | 6 pins / 5 arcs; levels 0…5; path Σ 3.2; cycle fails | **10** | **Shipped** |

Shared helpers: `platform/assets/sta-core.js`, `platform/assets/sta-ui.js`.

## Algorithm walkthroughs (PPT / transcript)

Step-by-step teaching frames (graph + caption + bullets):

- Viewer: [`tools/algorithm-walkthrough/`](tools/algorithm-walkthrough/) — `?algo=<lab-id>&step=N`
- Media rebuild **in WSL**: `bash courses/learn_clustering/scripts/build_all_media.sh`
- Index: [`courses/learn_clustering/docs/WALKTHROUGHS.md`](../courses/learn_clustering/docs/WALKTHROUGHS.md)
