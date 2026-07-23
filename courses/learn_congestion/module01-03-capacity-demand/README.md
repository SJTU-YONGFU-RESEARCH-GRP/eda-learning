# Module 01-03: Capacity vs demand

**Module id:** `module01-03-capacity-demand`  
**Kind:** `lab` · Primary lab: `capacity-demand` · **ref**

[← GCell grid](../module01-01-gcell-grid/README.md) · [Course README](../README.md) · [RUDY →](../module02-01-rudy-estimate/README.md)

## Outcomes

After this module you can: **Contrast per-GCell routing capacity with estimated demand and flag oversubscribed tiles.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **capacity vs demand comparison per GCell** on `examples/tiny_cong.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with demand, congestion, and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 01-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/capacity-demand/](http://127.0.0.1:8080/tools/capacity-demand/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/capacity-demand/](https://universal-verification-methodology.github.io/learning/tools/capacity-demand/)
3. Tools shelf: open `capacity-demand` from the platform tools index
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
module01-03-capacity-demand/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
