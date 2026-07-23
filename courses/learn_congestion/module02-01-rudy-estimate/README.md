# Module 02-01: RUDY congestion estimate

**Module id:** `module02-01-rudy-estimate`  
**Kind:** `lab` · Primary lab: `rudy-estimate` · **ref**

[← Capacity / demand](../module01-03-capacity-demand/README.md) · [Course README](../README.md) · [Probabilistic →](../module02-03-probabilistic-demand/README.md)

## Outcomes

After this module you can: **Estimate routing demand with RUDY: distribute each net's HPWL density over GCells under its bbox.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **RUDY (Rectangular Uniform wire DensitY) demand estimate** on `examples/tiny_cong.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with demand, congestion, and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 02-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/rudy-estimate/](http://127.0.0.1:8080/tools/rudy-estimate/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/rudy-estimate/](https://universal-verification-methodology.github.io/learning/tools/rudy-estimate/)
3. Tools shelf: open `rudy-estimate` from the platform tools index
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
module02-01-rudy-estimate/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
