# Module 04-01: Hierarchical floorplanning

**Module id:** `module04-01-hierarchical-floorplan`  
**Kind:** `lab` · Primary lab: `hierarchical-floorplan` · **Shipped**

[← Macros](../module03-05-macro-placement/README.md) · [Course README](../README.md) · [Pin assignment →](../module04-03-pin-assignment/README.md)

## Outcomes

After this module you can: **Floorplan nested clusters: pack sub-floorplans inside parent regions, then compose the top outline.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **hierarchical / recursive sub-floorplan packing** on `examples/tiny_modules.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, area, density, and deadspace (plus lab-specific metrics).
3. Optional self-check: `./scripts/module.sh 04-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/hierarchical-floorplan/](http://127.0.0.1:8080/tools/hierarchical-floorplan/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/hierarchical-floorplan/](https://universal-verification-methodology.github.io/learning/tools/hierarchical-floorplan/)
3. Tools shelf: open `hierarchical-floorplan` from the platform tools index
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
module04-01-hierarchical-floorplan/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
