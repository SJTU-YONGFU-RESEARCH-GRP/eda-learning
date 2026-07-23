# Module 03-05: Hard macro / fixed-block placement

**Module id:** `module03-05-macro-placement`  
**Kind:** `lab` · Primary lab: `macro-placement` · **Shipped**

[← Soft modules](../module03-03-soft-module-sizing/README.md) · [Course README](../README.md) · [Hierarchical →](../module04-01-hierarchical-floorplan/README.md)

## Outcomes

After this module you can: **Treat hard macros as fixed-size (and optionally fixed-position) blocks and pack soft/movable modules around them.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **hard-macro / fixed-block constrained packing** on `examples/tiny_modules.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, area, density, and deadspace (plus lab-specific metrics).
3. Optional self-check: `./scripts/module.sh 03-05 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/macro-placement/](http://127.0.0.1:8080/tools/macro-placement/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/macro-placement/](https://universal-verification-methodology.github.io/learning/tools/macro-placement/)
3. Tools shelf: open `macro-placement` from the platform tools index
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
module03-05-macro-placement/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
