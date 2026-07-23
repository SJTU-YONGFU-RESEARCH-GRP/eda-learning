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

## Algorithm walkthroughs (PPT / transcript)

Step-by-step teaching frames (graph + caption + bullets):

- Viewer: [`tools/algorithm-walkthrough/`](tools/algorithm-walkthrough/) — `?algo=<lab-id>&step=N`
- Media rebuild **in WSL**: `bash courses/learn_clustering/scripts/build_all_media.sh`
- Index: [`courses/learn_clustering/docs/WALKTHROUGHS.md`](../courses/learn_clustering/docs/WALKTHROUGHS.md)
