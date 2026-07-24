# Module 02-03: A* detailed routing

**Module id:** `module02-03-astar-route`  
**Kind:** `lab` · Primary lab: `astar-route` · **ref**

[← Lee maze](../module02-01-lee-maze/README.md) · [Course README](../README.md) · [Track usage →](../module02-05-track-usage/README.md)

## Outcomes

After this module you can: **Route two-pin nets with A* that penalizes tracks at capacity.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **A* detailed routing (congestion-aware grid search)** on `examples/tiny_dr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with track usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 02-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/astar-route/](http://127.0.0.1:8080/tools/astar-route/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/astar-route/](https://universal-verification-methodology.github.io/learning/tools/astar-route/)
3. Tools shelf: open `astar-route` from the platform tools index
4. Load the **starter detailed routing** instance, run the router, inspect track overflow and vias.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach detailed routing literacy on a tiny M1/M2 grid — not production signoff routers.

## Media

| Artifact | Path |
|----------|------|
| Transcript | [transcript.md](transcript.md) |
| Outline | [outline.yaml](outline.yaml) |
| Slides | [slides.pptx](slides.pptx) · [slides.pdf](slides.pdf) |
| Video | [video.mp4](video.mp4) |
| Quiz | [quiz.json](quiz.json) |

## Files

```
module02-03-astar-route/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
