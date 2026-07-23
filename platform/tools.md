# Platform tools catalog

Browser labs for **eda_learning**. Serve with:

```bash
python -m http.server 8080 --directory platform
```

## Clustering & refinement

Interactive labs: **you assign / flip / merge / run**, then Check. Workspace starts as a seed or unlabeled — **not** the golden.
**Reveal golden (study)** is optional and does not clear challenges. Shared helper: `platform/assets/interactive-graph-lab.js`.

| Tool | Learner actions | Challenges | Status |
|------|-----------------|------------|--------|
| `affinity-metrics` | Pick Edge vs Shared scoring; pin pairs | **10** | **Shipped** |
| `greedy-pair-merge` | Merge to K (or one step); check parts/cut | **10** | **Shipped** |
| `size-constrained-agglomerative` | Run K + capacity; check AB\|C\|DE cut 8 | **10** | **Shipped** |
| `label-propagation` | Run LP or edit labels → cut 3 | **10** | **Shipped** |
| `spectral-bisection` | Assign sides or Run spectral → ABC\|DE cut 3 | **10** | **Shipped** |
| `kernighan-lin` | Swap A↔D / Run KL: seed 12 → cut 3 | **10** | **Shipped** |
| `fiduccia-mattheyses` | Flip D then A / Run FM: 12 → 3 | **10** | **Shipped** |
| `multilevel-clustering` | Run multilevel or edit → P0/P1 cut 3 | **10** | **Shipped** |
| `hypergraph-clustering` | Run hyper greedy → hyper cut 1 | **10** | **Shipped** |
| `congestion-aware-clustering` | Run λ=0 / λ=5; check plain/pen | **10** | **Shipped** |
| `timing-aware-clustering` | Run timing-aware → plain 3, weighted 7 | **10** | **Shipped** |

## Partitioning

Interactive labs: **you assign / flip / swap / run**, then Check. Same pattern as Floorplanning and Clustering.

| Tool | Learner actions | Challenges | Status |
|------|-----------------|------------|--------|
| `cutsize-balance` | Flip seed 12 → cut 3; read balance | **10** | **Shipped** |
| `initial-bipartition` | Grow / greedy / random / Assign | **10** | **Shipped** |
| `kl-partition` | Swap A↔D / Run KL: 12 → 3 | **10** | **Shipped** |
| `fm-partition` | Flip D then A / Run FM: 12 → 3 | **10** | **Shipped** |
| `spectral-partition` | Assign or Run spectral → ABC\|DE cut 3 | **10** | **Shipped** |
| `recursive-bisection` | Run k=3 / k=4 → AB\|C\|DE cut 8 | **10** | **Shipped** |
| `multiway-partition` | Recursive vs round-robin k=3 | **10** | **Shipped** |
| `terminal-propagation` | Locked A/E; Propagate or Assign free | **10** | **Shipped** |
| `hypergraph-partition` | Flip / Run hyper FM: hyper cut 6 → 1 | **10** | **Shipped** |
| `multilevel-partition` | Run V-cycle; inspect stages | **10** | **Shipped** |

Shared helpers: `platform/assets/partitioning-core.js`, `platform/assets/interactive-graph-lab.js` (imports graph utils / KL / FM / spectral from `clustering-core.js`).

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
| `spread-legalize-lite` | Overlap minDist 0 → spacing ≥ **0.5** | **10** | **Shipped** |
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
