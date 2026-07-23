# Module 03-01: Incremental timing update

**Module id:** `module03-01-incremental-update`  
**Kind:** `lab` · Primary lab: `incremental-update` · **Shipped**

[← Critical path](../module02-03-critical-path/README.md) · [Course README](../README.md) · [False / multicycle →](../module03-03-false-multicycle-lite/README.md)

## Outcomes

After this module you can: **Invalidate and recompute only the cone affected by a local delay change.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **incremental invalidate / recompute on a delay edit** on the tiny timing netlist.
2. Complete [CHECKLIST.md](CHECKLIST.md) with arrivals, required times, and slack (as applicable).
3. Optional self-check: `./scripts/module.sh 03-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/incremental-update/index.html](http://127.0.0.1:8080/tools/incremental-update/index.html)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/incremental-update/](https://universal-verification-methodology.github.io/learning/tools/incremental-update/)
3. Tools shelf: open `incremental-update` from the platform tools index
3. Load the **starter netlist**, run the analysis, inspect path / slack metrics.
4. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach STA literacy on tiny graphs — not foundry sign-off or vendor GUI flows.

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
module03-01-incremental-update/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
