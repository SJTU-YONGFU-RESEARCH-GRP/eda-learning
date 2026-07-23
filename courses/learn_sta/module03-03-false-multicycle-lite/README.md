# Module 03-03: False and multicycle paths (engine view)

**Module id:** `module03-03-false-multicycle-lite`  
**Kind:** `lab` · Primary lab: `false-multicycle-lite` · **Shipped**

[← Incremental update](../module03-01-incremental-update/README.md) · [Course README](../README.md) · [Offline compare →](../module05-01-offline-benchmark-compare/README.md)

## Outcomes

After this module you can: **Apply engine-facing false-path and multicycle exceptions that change which endpoints are timed.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **false-path and multicycle exceptions as STA engine data** on the tiny timing netlist.
2. Complete [CHECKLIST.md](CHECKLIST.md) with arrivals, required times, and slack (as applicable).
3. Optional self-check: `./scripts/module.sh 03-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/false-multicycle-lite/index.html](http://127.0.0.1:8080/tools/false-multicycle-lite/index.html)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/false-multicycle-lite/](https://universal-verification-methodology.github.io/learning/tools/false-multicycle-lite/)
3. Tools shelf: open `false-multicycle-lite` from the platform tools index
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
module03-03-false-multicycle-lite/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
