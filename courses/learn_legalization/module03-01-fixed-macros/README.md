# Module 03-01: Fixed macros during legalization

**Module id:** `module03-01-fixed-macros`  
**Kind:** `lab` · Primary lab: `fixed-macros` · **ref**

[← Tetris pack](../module02-07-tetris-row-pack/README.md) · [Course README](../README.md) · [Displacement / HPWL →](../module03-03-displacement-hpwl/README.md)

## Outcomes

After this module you can: **Legalize movable standard cells around fixed macro obstacles locked at (x, y).**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **legalization with fixed macro obstacles** on `examples/tiny_legal.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, displacement, and HPWL when relevant.
3. Optional self-check: `./scripts/module.sh 03-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/fixed-macros/](http://127.0.0.1:8080/tools/fixed-macros/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/fixed-macros/](https://universal-verification-methodology.github.io/learning/tools/fixed-macros/)
3. Tools shelf: open `fixed-macros` from the platform tools index
4. Load the **starter legalization**, run the algorithm, inspect legality and metrics.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach legalization literacy on tiny site/row grids — not production OpenROAD legalizers.

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
module03-01-fixed-macros/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
