# Module 04-03: Boundary pin / I/O assignment

**Module id:** `module04-03-pin-assignment`  
**Kind:** `lab` · Primary lab: `pin-assignment` · **Shipped**

[← Hierarchical](../module04-01-hierarchical-floorplan/README.md) · [Course README](../README.md) · [Offline compare →](../module05-01-offline-benchmark-compare/README.md)

## Outcomes

After this module you can: **Assign I/O pins to chip edges (N/E/S/W) and relate pin sides to module abutments and wirelength hints.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **boundary pin / I/O edge assignment** on `examples/tiny_modules.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, area, density, and deadspace (plus lab-specific metrics).
3. Optional self-check: `./scripts/module.sh 04-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/pin-assignment/](http://127.0.0.1:8080/tools/pin-assignment/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/pin-assignment/](https://universal-verification-methodology.github.io/learning/tools/pin-assignment/)
3. Tools shelf: open `pin-assignment` from the platform tools index
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
module04-03-pin-assignment/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
