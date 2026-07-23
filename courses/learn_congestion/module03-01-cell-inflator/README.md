# Module 03-01: Cell inflation

**Module id:** `module03-01-cell-inflator`  
**Kind:** `lab` · Primary lab: `cell-inflator` · **ref**

[← Overflow](../module02-07-overflow-metrics/README.md) · [Course README](../README.md) · [Net weighting →](../module03-03-net-weighting/README.md)

## Outcomes

After this module you can: **Inflate cell widths in oversubscribed GCells so the next place pass spreads demand.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **cell inflation from congestion (width scale)** on `examples/tiny_cong.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with demand, congestion, and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 03-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/cell-inflator/](http://127.0.0.1:8080/tools/cell-inflator/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/cell-inflator/](https://universal-verification-methodology.github.io/learning/tools/cell-inflator/)
3. Tools shelf: open `cell-inflator` from the platform tools index
4. Load the **starter congestion** instance, run the estimator, inspect overflow metrics.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach congestion literacy on a tiny GCell grid — not production global routers.

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
module03-01-cell-inflator/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
