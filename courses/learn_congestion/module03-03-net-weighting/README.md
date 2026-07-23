# Module 03-03: Congestion-aware net weighting

**Module id:** `module03-03-net-weighting`  
**Kind:** `lab` · Primary lab: `net-weighting` · **ref**

[← Inflator](../module03-01-cell-inflator/README.md) · [Course README](../README.md) · [Place feedback →](../module04-01-placement-feedback/README.md)

## Outcomes

After this module you can: **Raise net weights through congested GCells to pull placement away from hotspots.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **congestion-aware net weighting** on `examples/tiny_cong.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with demand, congestion, and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 03-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/net-weighting/](http://127.0.0.1:8080/tools/net-weighting/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/net-weighting/](https://universal-verification-methodology.github.io/learning/tools/net-weighting/)
3. Tools shelf: open `net-weighting` from the platform tools index
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
module03-03-net-weighting/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
