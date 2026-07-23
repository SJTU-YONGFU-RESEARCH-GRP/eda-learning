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
  module01-01-hpwl-metrics \
  module01-03-net-models \
  module02-01-force-directed-place \
  module02-03-quadratic-place \
  module02-05-analytical-place \
  module02-07-sa-placement \
  module03-01-density-bins \
  module03-03-spread-legalize-lite \
  module04-01-timing-driven-place
do
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
    courses/learn_placement/$m --inject-transcript
done

bash courses/learn_placement/scripts/build_all_media.sh
```

| Algorithm | Module | Steps |
|-----------|--------|-------|
| `hpwl-metrics` | [`module01-01-hpwl-metrics`](../module01-01-hpwl-metrics/assets/STEPS.md) | (capture later) |
| `net-models` | [`module01-03-net-models`](../module01-03-net-models/assets/STEPS.md) | (capture later) |
| `force-directed-place` | [`module02-01-force-directed-place`](../module02-01-force-directed-place/assets/STEPS.md) | (capture later) |
| `quadratic-place` | [`module02-03-quadratic-place`](../module02-03-quadratic-place/assets/STEPS.md) | (capture later) |
| `analytical-place` | [`module02-05-analytical-place`](../module02-05-analytical-place/assets/STEPS.md) | (capture later) |
| `sa-placement` | [`module02-07-sa-placement`](../module02-07-sa-placement/assets/STEPS.md) | (capture later) |
| `density-bins` | [`module03-01-density-bins`](../module03-01-density-bins/assets/STEPS.md) | (capture later) |
| `spread-legalize-lite` | [`module03-03-spread-legalize-lite`](../module03-03-spread-legalize-lite/assets/STEPS.md) | (capture later) |
| `timing-driven-place` | [`module04-01-timing-driven-place`](../module04-01-timing-driven-place/assets/STEPS.md) | (capture later) |

Intro / offline / wrap modules have PPTX from transcript only (no algorithm step frames).
