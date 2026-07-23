# Module 04-01: Detailed vs global legalize

**Module id:** `module04-01-detailed-vs-global`  
**Kind:** `lab` · Primary lab: `detailed-vs-global` · **ref**

[← Displacement / HPWL](../module03-03-displacement-hpwl/README.md) · [Course README](../README.md) · [Offline compare →](../module05-01-offline-benchmark-compare/README.md)

## Outcomes

After this module you can: **Contrast a fast global snap/pack pass with a detailed multi-row legalization flow.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **global vs detailed legalization pipeline contrast** on `examples/tiny_legal.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, displacement, and HPWL when relevant.
3. Optional self-check: `./scripts/module.sh 04-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/detailed-vs-global/](http://127.0.0.1:8080/tools/detailed-vs-global/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/detailed-vs-global/](https://universal-verification-methodology.github.io/learning/tools/detailed-vs-global/)
3. Tools shelf: open `detailed-vs-global` from the platform tools index
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
module04-01-detailed-vs-global/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
