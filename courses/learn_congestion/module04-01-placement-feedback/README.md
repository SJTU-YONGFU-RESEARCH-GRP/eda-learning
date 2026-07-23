# Module 04-01: Placement feedback loop

**Module id:** `module04-01-placement-feedback`  
**Kind:** `lab` · Primary lab: `placement-feedback` · **ref**

[← Net weighting](../module03-03-net-weighting/README.md) · [Course README](../README.md) · [Offline compare →](../module05-01-offline-benchmark-compare/README.md)

## Outcomes

After this module you can: **Run one estimate→inflate→push feedback pass and show overflow drop on the tiny instance.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **placement feedback (estimate → inflate → push)** on `examples/tiny_cong.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with demand, congestion, and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 04-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/placement-feedback/](http://127.0.0.1:8080/tools/placement-feedback/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/placement-feedback/](https://universal-verification-methodology.github.io/learning/tools/placement-feedback/)
3. Tools shelf: open `placement-feedback` from the platform tools index
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
module04-01-placement-feedback/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
