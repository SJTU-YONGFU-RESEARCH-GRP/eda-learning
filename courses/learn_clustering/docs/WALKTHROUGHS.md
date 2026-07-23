# Algorithm walkthroughs (for PPT / transcript)

Step frames live under each lab module’s `assets/steps/` with captions in `assets/STEPS.md`.
Transcripts embed them between `<!-- algorithm-walkthrough -->` markers; PPTX rebuilds as full-slide images.

## Interactive viewer

`platform/tools/algorithm-walkthrough/?algo=<lab-id>&step=N`

Serve: `python -m http.server 8080 --directory platform`

## Capture + rebuild (WSL)

Media builds run **in WSL** (matches module-slides: `soffice`, `edge-tts`, `ffmpeg`).

```bash
cd /mnt/d/proj/designs/eda_learning   # adjust drive/path

# Full course: outline → PPTX → PDF → audio → video
bash courses/learn_clustering/scripts/build_all_media.sh

# Or skill one-liner for all modules:
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  --course-dir courses/learn_clustering

# Walkthrough PNGs only (serve platform/ on :8080 first):
bash courses/learn_clustering/scripts/build_all_media.sh --capture
```

Interactive viewer: `platform/tools/algorithm-walkthrough/?algo=<lab-id>&step=N`

| Algorithm | Module | Steps |
|-----------|--------|-------|
| `affinity-metrics` | [`module01-01`](../module01-01-affinity-metrics/assets/STEPS.md) | 5 |
| `greedy-pair-merge` | [`module01-03`](../module01-03-greedy-pair-merge/assets/STEPS.md) | 5 |
| `size-constrained-agglomerative` | [`module01-05`](../module01-05-size-constrained-agglomerative/assets/STEPS.md) | 5 |
| `label-propagation` | [`module02-01`](../module02-01-label-propagation/assets/STEPS.md) | 5 |
| `spectral-bisection` | [`module02-03`](../module02-03-spectral-bisection/assets/STEPS.md) | 5 |
| `kernighan-lin` | [`module02-05`](../module02-05-kernighan-lin/assets/STEPS.md) | 5 |
| `fiduccia-mattheyses` | [`module02-07`](../module02-07-fiduccia-mattheyses/assets/STEPS.md) | 5 |
| `multilevel-clustering` | [`module03-01`](../module03-01-multilevel-clustering/assets/STEPS.md) | 5 |
| `hypergraph-clustering` | [`module03-03`](../module03-03-hypergraph-clustering/assets/STEPS.md) | 5 |
| `congestion-aware-clustering` | [`module04-01`](../module04-01-congestion-aware-clustering/assets/STEPS.md) | 5 |
| `timing-aware-clustering` | [`module04-03`](../module04-03-timing-aware-clustering/assets/STEPS.md) | 5 |

Intro / offline / wrap modules have PPTX from transcript only (no algorithm step frames).
