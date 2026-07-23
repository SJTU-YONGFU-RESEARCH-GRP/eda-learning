# Module 02-03: Probabilistic routing demand

**Module id:** `module02-03-probabilistic-demand`  
**Kind:** `lab` · Primary lab: `probabilistic-demand` · **ref**

[← RUDY](../module02-01-rudy-estimate/README.md) · [Course README](../README.md) · [Congestion map →](../module02-05-congestion-map/README.md)

## Outcomes

After this module you can: **Estimate demand with L-shape probabilistic routing (half each bend) and compare to RUDY.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **probabilistic L-shape routing demand** on `examples/tiny_cong.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with demand, congestion, and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 02-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/probabilistic-demand/](http://127.0.0.1:8080/tools/probabilistic-demand/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/probabilistic-demand/](https://universal-verification-methodology.github.io/learning/tools/probabilistic-demand/)
3. Tools shelf: open `probabilistic-demand` from the platform tools index
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
module02-03-probabilistic-demand/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
