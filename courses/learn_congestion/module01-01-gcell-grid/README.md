# Module 01-01: GCell grid model

**Module id:** `module01-01-gcell-grid`  
**Kind:** `lab` · Primary lab: `gcell-grid` · **ref**

[← Welcome](../module00-00-intro/README.md) · [Course README](../README.md) · [Capacity / demand →](../module01-03-capacity-demand/README.md)

## Outcomes

After this module you can: **Map chip coordinates onto a 4×2 GCell grid and report which tile owns a cell center.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **GCell grid indexing (nx×ny tiles over chip W×H)** on `examples/tiny_cong.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with demand, congestion, and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 01-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/gcell-grid/](http://127.0.0.1:8080/tools/gcell-grid/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/gcell-grid/](https://universal-verification-methodology.github.io/learning/tools/gcell-grid/)
3. Tools shelf: open `gcell-grid` from the platform tools index
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
module01-01-gcell-grid/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
