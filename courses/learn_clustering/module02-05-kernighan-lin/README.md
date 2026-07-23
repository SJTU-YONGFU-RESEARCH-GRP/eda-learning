# Module 02-05: Kernighan–Lin refinement

**Module id:** `module02-05-kernighan-lin`  
**Kind:** `lab` · Primary lab: `kernighan-lin` · **Shipped**

[← Spectral bisection](../module02-03-spectral-bisection/README.md) · [Course README](../README.md) · [Fiduccia–Mattheyses →](../module02-07-fiduccia-mattheyses/README.md)

## Outcomes

After this module you can: **Implement full KL pair-swap refinement with gains, locking, and rollback to best prefix.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **Kernighan–Lin (KL) refinement** on the tiny graphs.
2. Complete [CHECKLIST.md](CHECKLIST.md) with metrics (cutsize, balance, objective).
3. Optional self-check: `./scripts/module.sh 02-05 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/kernighan-lin/index.html](http://127.0.0.1:8080/tools/kernighan-lin/index.html)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/kernighan-lin/](https://universal-verification-methodology.github.io/learning/tools/kernighan-lin/)
3. Tools shelf: open `kernighan-lin` from the platform tools index
4. Load the **starter graph**, run the algorithm, inspect metrics.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach algorithm literacy on tiny instances — not production PDK flows.

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
module02-05-kernighan-lin/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
