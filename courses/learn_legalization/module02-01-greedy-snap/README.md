# Module 02-01: Greedy site/row snap

**Module id:** `module02-01-greedy-snap`  
**Kind:** `lab` · Primary lab: `greedy-snap` · **ref**

[← Legality](../module01-03-legality-metrics/README.md) · [Course README](../README.md) · [Overlap removal →](../module02-03-overlap-removal/README.md)

## Outcomes

After this module you can: **Snap floating global-place coordinates to the nearest legal site and row bottom.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **greedy site/row snap from float coordinates** on `examples/tiny_legal.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, displacement, and HPWL when relevant.
3. Optional self-check: `./scripts/module.sh 02-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/greedy-snap/](http://127.0.0.1:8080/tools/greedy-snap/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/greedy-snap/](https://universal-verification-methodology.github.io/learning/tools/greedy-snap/)
3. Tools shelf: open `greedy-snap` from the platform tools index
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
module02-01-greedy-snap/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
