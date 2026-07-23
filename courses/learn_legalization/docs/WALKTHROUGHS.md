# Algorithm walkthroughs (for PPT / transcript)

Step frames will live under each lab module’s `assets/steps/` with captions in `assets/STEPS.md`.
Transcripts embed them between `<!-- algorithm-walkthrough -->` markers when captured.

## Interactive viewer

`platform/tools/algorithm-walkthrough/?algo=<lab-id>&step=N`

Serve: `python3 -m http.server 8080 --directory platform`

## Capture + rebuild (WSL)

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_legalization/scripts/build_all_media.sh
bash courses/learn_legalization/scripts/capture_all_walkthroughs.sh
```

| Algorithm | Module | Steps |
|-----------|--------|-------|
| `site-row-model` | [`module01-01-site-row-model`](../module01-01-site-row-model/README.md) | ALGOS ready (5) |
| `legality-metrics` | [`module01-03-legality-metrics`](../module01-03-legality-metrics/README.md) | ALGOS ready (5) |
| `greedy-snap` | [`module02-01-greedy-snap`](../module02-01-greedy-snap/README.md) | ALGOS ready (5) |
| `overlap-removal` | [`module02-03-overlap-removal`](../module02-03-overlap-removal/README.md) | ALGOS ready (5) |
| `abacus-row-pack` | [`module02-05-abacus-row-pack`](../module02-05-abacus-row-pack/README.md) | ALGOS ready (5) |
| `tetris-row-pack` | [`module02-07-tetris-row-pack`](../module02-07-tetris-row-pack/README.md) | ALGOS ready (5) |
| `fixed-macros` | [`module03-01-fixed-macros`](../module03-01-fixed-macros/README.md) | ALGOS ready (5) |
| `displacement-hpwl` | [`module03-03-displacement-hpwl`](../module03-03-displacement-hpwl/README.md) | ALGOS ready (5) |
| `detailed-vs-global` | [`module04-01-detailed-vs-global`](../module04-01-detailed-vs-global/README.md) | ALGOS ready (5) |

Step definitions live in `platform/tools/algorithm-walkthrough/legalization-algos.js`. PNG capture and transcript injection are **pending** (run `capture_all_walkthroughs.sh` after serving `platform/`).

Intro / offline / wrap modules have PPTX from transcript only (no algorithm step frames).
