# Algorithm walkthroughs (for PPT / transcript)

Step frames live under each lab module’s `assets/steps/` with captions in `assets/STEPS.md`.
Transcripts embed them between `<!-- algorithm-walkthrough -->` markers; PPTX rebuilds as full-slide images.

## Interactive viewer

`platform/tools/algorithm-walkthrough/?algo=<lab-id>&step=N`

Serve: `python3 -m http.server 8080 --directory platform`

## Capture + rebuild (WSL)

```bash
cd /mnt/d/proj/designs/eda_learning
python3 -m http.server 8080 --directory platform &
# then, per lab (or loop):
python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
  courses/learn_floorplanning/module01-01-fixed-outline --inject-transcript
bash courses/learn_floorplanning/scripts/build_all_media.sh
```

| Algorithm | Module | Steps |
|-----------|--------|-------|
| `fixed-outline` | [`01-01`](../module01-01-fixed-outline/assets/STEPS.md) | 5 |
| `area-deadspace` | [`01-03`](../module01-03-area-deadspace/assets/STEPS.md) | 5 |
| `slicing-floorplan` | [`02-01`](../module02-01-slicing-floorplan/assets/STEPS.md) | 5 |
| `bstar-tree` | [`02-03`](../module02-03-bstar-tree/assets/STEPS.md) | 5 |
| `sequence-pair` | [`02-05`](../module02-05-sequence-pair/assets/STEPS.md) | 5 |
| `simulated-annealing-fp` | [`03-01`](../module03-01-simulated-annealing-fp/assets/STEPS.md) | 5 |
| `soft-module-sizing` | [`03-03`](../module03-03-soft-module-sizing/assets/STEPS.md) | 5 |
| `macro-placement` | [`03-05`](../module03-05-macro-placement/assets/STEPS.md) | 5 |
| `hierarchical-floorplan` | [`04-01`](../module04-01-hierarchical-floorplan/assets/STEPS.md) | 5 |
| `pin-assignment` | [`04-03`](../module04-03-pin-assignment/assets/STEPS.md) | 5 |

Intro / offline / wrap modules have PPTX from transcript only (no algorithm step frames).
