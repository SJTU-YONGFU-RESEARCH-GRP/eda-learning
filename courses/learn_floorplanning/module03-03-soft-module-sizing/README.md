# Module 03-03: Soft module aspect sizing

**Module id:** `module03-03-soft-module-sizing`  
**Kind:** `lab` · Primary lab: `soft-module-sizing` · **Shipped**

[← Simulated annealing](../module03-01-simulated-annealing-fp/README.md) · [Course README](../README.md) · [Macros →](../module03-05-macro-placement/README.md)

## Outcomes

After this module you can: **Resize soft modules within aspect-ratio bounds while preserving area and keeping the packing legal.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **soft-module aspect-ratio sizing under fixed outline** on `examples/tiny_modules.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, area, density, and deadspace (plus lab-specific metrics).
3. Optional self-check: `./scripts/module.sh 03-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/soft-module-sizing/](http://127.0.0.1:8080/tools/soft-module-sizing/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/soft-module-sizing/](https://universal-verification-methodology.github.io/learning/tools/soft-module-sizing/)
3. Tools shelf: open `soft-module-sizing` from the platform tools index
4. Load the **starter modules**, run the packing / search, inspect outline metrics.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach floorplan literacy on tiny outlines — not production place-and-route.

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
module03-03-soft-module-sizing/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
