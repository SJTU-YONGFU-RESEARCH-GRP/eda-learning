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

Interactive labs: **you move cells** (and/or apply force/SA/quad helpers), then Check.
Workspace starts at the high-HPWL seed — **not** the golden. **Reveal golden (study)** is optional.

| Tool | Learner actions | Challenges | Status |
|------|-----------------|------------|--------|
| `hpwl-metrics` | Move cells; starter HPWL 52 → golden 14 | **10** | **Shipped** |
| `net-models` | Move / inspect clique vs star nets | **10** | **Shipped** |
| `force-directed-place` | Move or Apply force step → ≈18.7 | **10** | **Shipped** |
| `quadratic-place` | Pads A,D fixed; place rest → HPWL 48 | **10** | **Shipped** |
| `analytical-place` | Force/quad + density spread | **10** | **Shipped** |
| `sa-placement` | Swap/move or SA steps | **10** | **Shipped** |
| `density-bins` | Move cells; read bin overflow | **10** | **Shipped** |
| `spread-legalize-lite` | Spread overlaps → minDist ≥ 0.5 | **10** | **Shipped** |
| `timing-driven-place` | Move critical nets → timing HPWL 30 | **10** | **Shipped** |

Shared helpers: `platform/assets/placement-core.js`, `platform/assets/interactive-placement-lab.js`.

## Legalization

Interactive labs: **you move cells on the site/row grid** (and/or Apply snap/Abacus/Tetris), then Check.
Overlap/float seeds — **not** the golden. **Reveal golden (study)** is optional.

| Tool | Learner actions | Challenges | Status |
|------|-----------------|------------|--------|
| `site-row-model` | Snap to sites/rows; read grid model | **10** | **Shipped** |
| `legality-metrics` | Fix overlaps; legalityReport | **10** | **Shipped** |
| `greedy-snap` | Float → Snap all (may still overlap) | **10** | **Shipped** |
| `overlap-removal` | Move or Apply overlap-removal | **10** | **Shipped** |
| `abacus-row-pack` | Apply Abacus / pack by hand | **10** | **Shipped** |
| `tetris-row-pack` | Apply Tetris / pack by hand | **10** | **Shipped** |
| `fixed-macros` | D locked; Abacus respects macros | **10** | **Shipped** |
| `displacement-hpwl` | Legalize; cost = HPWL + λ·disp | **10** | **Shipped** |
| `detailed-vs-global` | Compare global vs detailed disp | **10** | **Shipped** |

Shared helpers: `platform/assets/legalization-core.js`, `platform/assets/interactive-legalization-lab.js`.

## Static timing analysis (STA)

Interactive labs: **you assign levels / values / path / cone / exceptions**, then Check.
Workspace starts empty or seeded — **not** the golden. **Reveal golden (study)** is optional.
Helpers (Levelize / Propagate / Trace) are optional accelerators.

| Tool | Learner actions | Challenges | Status |
|------|-----------------|------------|--------|
| `timing-graph` | Assign levels or Run levelize; try cycle edge | **10** | **Shipped** |
| `arrival-required` | Enter A/R or Propagate | **10** | **Shipped** |
| `slack-setup-hold` | Enter slack or Compute setup/hold | **10** | **Shipped** |
| `critical-path` | Click path pins or Trace | **10** | **Shipped** |
| `incremental-update` | Bump delay; mark fanout cone | **10** | **Shipped** |
| `false-multicycle-lite` | Disable arcs; set multicycle | **10** | **Shipped** |

Shared helpers: `platform/assets/sta-core.js`, `platform/assets/interactive-sta-lab.js`.

## Algorithm walkthroughs (PPT / transcript)

Step-by-step teaching frames (graph + caption + bullets):

- Viewer: [`tools/algorithm-walkthrough/`](tools/algorithm-walkthrough/) — `?algo=<lab-id>&step=N`
- Media rebuild **in WSL**: e.g. `bash courses/learn_legalization/scripts/build_all_media.sh`
- Indexes: [`learn_clustering/docs/WALKTHROUGHS.md`](../courses/learn_clustering/docs/WALKTHROUGHS.md) · [`learn_legalization/docs/WALKTHROUGHS.md`](../courses/learn_legalization/docs/WALKTHROUGHS.md)
