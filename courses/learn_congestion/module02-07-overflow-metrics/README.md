# Module 02-07: Overflow metrics

**Module id:** `module02-07-overflow-metrics`  
**Kind:** `lab` · Primary lab: `overflow-metrics` · **ref**

[← Congestion map](../module02-05-congestion-map/README.md) · [Course README](../README.md) · [Inflator →](../module03-01-cell-inflator/README.md)

## Outcomes

After this module you can: **Report total overflow, max overflow, and congested GCell count from a demand map.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **overflow metrics (total, max, congested count)** on `examples/tiny_cong.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with demand, congestion, and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 02-07 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/overflow-metrics/](http://127.0.0.1:8080/tools/overflow-metrics/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/overflow-metrics/](https://universal-verification-methodology.github.io/learning/tools/overflow-metrics/)
3. Tools shelf: open `overflow-metrics` from the platform tools index
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
module02-07-overflow-metrics/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
