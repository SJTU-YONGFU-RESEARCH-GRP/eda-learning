# learn_clustering — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.
Published ids are **stable keys**; order below is the teaching path.

Status: **ref** = reference solver + goldens in `common/` (all algorithm modules).

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
| `module00-00-intro` | `intro` | [Welcome to clustering for EDA](../module00-00-intro/README.md) | — | — |
| `module01-01-affinity-metrics` | `lab` | [Affinity metrics](../module01-01-affinity-metrics/README.md) | `affinity-metrics` | **ref** |
| `module01-03-greedy-pair-merge` | `lab` | [Greedy pair merge](../module01-03-greedy-pair-merge/README.md) | `greedy-pair-merge` | **ref** |
| `module01-05-size-constrained-agglomerative` | `lab` | [Size-constrained agglomerative clustering](../module01-05-size-constrained-agglomerative/README.md) | `size-constrained-agglomerative` | **ref** |
| `module02-01-label-propagation` | `lab` | [Label propagation clustering](../module02-01-label-propagation/README.md) | `label-propagation` | **ref** |
| `module02-03-spectral-bisection` | `lab` | [Spectral bisection](../module02-03-spectral-bisection/README.md) | `spectral-bisection` | **ref** |
| `module02-05-kernighan-lin` | `lab` | [Kernighan–Lin refinement](../module02-05-kernighan-lin/README.md) | `kernighan-lin` | **ref** |
| `module02-07-fiduccia-mattheyses` | `lab` | [Fiduccia–Mattheyses refinement](../module02-07-fiduccia-mattheyses/README.md) | `fiduccia-mattheyses` | **ref** |
| `module03-01-multilevel-clustering` | `lab` | [Multilevel clustering](../module03-01-multilevel-clustering/README.md) | `multilevel-clustering` | **ref** |
| `module03-03-hypergraph-clustering` | `lab` | [Hypergraph clustering](../module03-03-hypergraph-clustering/README.md) | `hypergraph-clustering` | **ref** |
| `module04-01-congestion-aware-clustering` | `lab` | [Congestion-aware clustering](../module04-01-congestion-aware-clustering/README.md) | `congestion-aware-clustering` | **ref** |
| `module04-03-timing-aware-clustering` | `lab` | [Timing-aware clustering](../module04-03-timing-aware-clustering/README.md) | `timing-aware-clustering` | **ref** |
| `module05-01-offline-benchmark-compare` | `offline` | [Offline benchmark compare](../module05-01-offline-benchmark-compare/README.md) | offline harness | **ref** |
| `module99-00-wrap` | `wrap` | [Clustering path complete](../module99-00-wrap/README.md) | — | — |

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (affinity, greedy, constrained agglomerative) |
| `02` | Classic methods (LP, spectral, KL, FM) |
| `03` | Multilevel + hypergraph |
| `04` | EDA-aware objectives (congestion, timing) |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs (PPT / transcript)

Step frames + captions for **all 11 algorithm labs**: [WALKTHROUGHS.md](WALKTHROUGHS.md).
Each lab module has `assets/STEPS.md`, `assets/steps/*.png`, and media (`slides.pptx` / `.pdf` / `audio/`).

**Build media in WSL** (LibreOffice + edge-tts + ffmpeg):

```bash
cd /mnt/d/proj/designs/eda_learning   # or your repo path in WSL
bash courses/learn_clustering/scripts/build_all_media.sh
# PPTX+PDF+audio only (skip video):  bash …/build_all_media.sh --no-video
```

Or one module via the skill:

```bash
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  courses/learn_clustering/module02-07-fiduccia-mattheyses
```
