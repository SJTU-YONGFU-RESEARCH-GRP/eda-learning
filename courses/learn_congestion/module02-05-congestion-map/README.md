# Module 02-05: Congestion heat map

**Module id:** `module02-05-congestion-map`  
**Kind:** `lab` · Primary lab: `congestion-map` · **ref**

[← Probabilistic](../module02-03-probabilistic-demand/README.md) · [Course README](../README.md) · [Overflow →](../module02-07-overflow-metrics/README.md)

## Outcomes

After this module you can: **Build a congestion heat map as demand/capacity per GCell and name the hottest tile.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **congestion heat map (demand / capacity)** on `examples/tiny_cong.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with demand, congestion, and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 02-05 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/congestion-map/](http://127.0.0.1:8080/tools/congestion-map/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/congestion-map/](https://universal-verification-methodology.github.io/learning/tools/congestion-map/)
3. Tools shelf: open `congestion-map` from the platform tools index
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
module02-05-congestion-map/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
