# Algorithm walkthroughs (for PPT / transcript)

Step frames live under each lab module’s `assets/steps/` with captions in `assets/STEPS.md`.
Transcripts embed them between `<!-- algorithm-walkthrough -->` markers.

## Interactive viewer

`platform/tools/algorithm-walkthrough/?algo=<lab-id>&step=N`

Serve: `python3 -m http.server 8080 --directory platform`

## Capture + rebuild (WSL)

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_legalization/scripts/capture_all_walkthroughs.sh
bash courses/learn_legalization/scripts/build_all_media.sh
```

| Algorithm | Module | Steps |
|-----------|--------|-------|
| `site-row-model` | [`module01-01-site-row-model`](../module01-01-site-row-model/README.md) | **5** frames |
| `legality-metrics` | [`module01-03-legality-metrics`](../module01-03-legality-metrics/README.md) | **5** frames |
| `greedy-snap` | [`module02-01-greedy-snap`](../module02-01-greedy-snap/README.md) | **5** frames |
| `overlap-removal` | [`module02-03-overlap-removal`](../module02-03-overlap-removal/README.md) | **5** frames |
| `abacus-row-pack` | [`module02-05-abacus-row-pack`](../module02-05-abacus-row-pack/README.md) | **5** frames |
| `tetris-row-pack` | [`module02-07-tetris-row-pack`](../module02-07-tetris-row-pack/README.md) | **5** frames |
| `fixed-macros` | [`module03-01-fixed-macros`](../module03-01-fixed-macros/README.md) | **5** frames |
| `displacement-hpwl` | [`module03-03-displacement-hpwl`](../module03-03-displacement-hpwl/README.md) | **5** frames |
| `detailed-vs-global` | [`module04-01-detailed-vs-global`](../module04-01-detailed-vs-global/README.md) | **5** frames |

Step definitions: `platform/tools/algorithm-walkthrough/legalization-algos.js` (**45** PNGs captured).

Browser labs are **interactive** (place/snap/nudge; Reveal study-only) via `interactive-legalization-lab.js`.

Intro / offline / wrap modules have PPTX from transcript only (no algorithm step frames).
