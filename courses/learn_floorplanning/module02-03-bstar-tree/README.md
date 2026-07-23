# Module 02-03: B*-tree floorplan representation

**Module id:** `module02-03-bstar-tree`  
**Kind:** `lab` · Primary lab: `bstar-tree` · **Shipped**

[← Slicing](../module02-01-slicing-floorplan/README.md) · [Course README](../README.md) · [Sequence pair →](../module02-05-sequence-pair/README.md)

## Outcomes

After this module you can: **Represent a packing with a B*-tree (left-child / right-child geometry) and reconstruct module coordinates.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **B*-tree packing (left = right-of, right = above)** on `examples/tiny_modules.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, area, density, and deadspace (plus lab-specific metrics).
3. Optional self-check: `./scripts/module.sh 02-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/bstar-tree/](http://127.0.0.1:8080/tools/bstar-tree/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/bstar-tree/](https://universal-verification-methodology.github.io/learning/tools/bstar-tree/)
3. Tools shelf: open `bstar-tree` from the platform tools index
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
module02-03-bstar-tree/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
