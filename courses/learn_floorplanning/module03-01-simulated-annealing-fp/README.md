# Module 03-01: Simulated annealing floorplan search

**Module id:** `module03-01-simulated-annealing-fp`  
**Kind:** `lab` · Primary lab: `simulated-annealing-fp` · **Shipped**

[← Sequence pair](../module02-05-sequence-pair/README.md) · [Course README](../README.md) · [Soft modules →](../module03-03-soft-module-sizing/README.md)

## Outcomes

After this module you can: **Run SA moves on a floorplan representation (swap, rotate, perturb) under a fixed outline cost.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **simulated annealing over floorplan moves (rep + cost)** on `examples/tiny_modules.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, area, density, and deadspace (plus lab-specific metrics).
3. Optional self-check: `./scripts/module.sh 03-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/simulated-annealing-fp/](http://127.0.0.1:8080/tools/simulated-annealing-fp/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/simulated-annealing-fp/](https://universal-verification-methodology.github.io/learning/tools/simulated-annealing-fp/)
3. Tools shelf: open `simulated-annealing-fp` from the platform tools index
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
module03-01-simulated-annealing-fp/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
