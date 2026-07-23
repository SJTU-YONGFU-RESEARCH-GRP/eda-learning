# Algorithm walkthroughs (for PPT / transcript)

Step frames live under each lab module’s `assets/steps/` with captions in `assets/STEPS.md`.
Transcripts embed them between `<!-- algorithm-walkthrough -->` markers; PPTX rebuilds as full-slide images.

## Interactive viewer

`platform/tools/algorithm-walkthrough/?algo=<lab-id>&step=N`

Serve: `python3 -m http.server 8080 --directory platform`

## Capture + rebuild (WSL)

```bash
cd /mnt/d/proj/designs/eda_learning

# Walkthrough PNGs + inject transcripts (serve platform/ on :8080 first)
python3 -m http.server 8080 --directory platform &
for m in \
  module01-01-cutsize-balance \
  module01-03-initial-bipartition \
  module02-01-kl-partition \
  module02-03-fm-partition \
  module02-05-spectral-partition \
  module02-07-recursive-bisection \
  module03-01-multiway-partition \
  module03-03-terminal-propagation \
  module03-05-hypergraph-partition \
  module04-01-multilevel-partition
do
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
    courses/learn_partitioning/$m --inject-transcript
done

bash courses/learn_partitioning/scripts/build_all_media.sh
```

| Algorithm | Module | Steps |
|-----------|--------|-------|
| `cutsize-balance` | [`module01-01`](../module01-01-cutsize-balance/assets/STEPS.md) | 5 |
| `initial-bipartition` | [`module01-03`](../module01-03-initial-bipartition/assets/STEPS.md) | 5 |
| `kl-partition` | [`module02-01`](../module02-01-kl-partition/assets/STEPS.md) | 5 |
| `fm-partition` | [`module02-03`](../module02-03-fm-partition/assets/STEPS.md) | 5 |
| `spectral-partition` | [`module02-05`](../module02-05-spectral-partition/assets/STEPS.md) | 5 |
| `recursive-bisection` | [`module02-07`](../module02-07-recursive-bisection/assets/STEPS.md) | 5 |
| `multiway-partition` | [`module03-01`](../module03-01-multiway-partition/assets/STEPS.md) | 5 |
| `terminal-propagation` | [`module03-03`](../module03-03-terminal-propagation/assets/STEPS.md) | 5 |
| `hypergraph-partition` | [`module03-05`](../module03-05-hypergraph-partition/assets/STEPS.md) | 5 |
| `multilevel-partition` | [`module04-01`](../module04-01-multilevel-partition/assets/STEPS.md) | 5 |

Intro / offline / wrap modules have PPTX from transcript only (no algorithm step frames).
