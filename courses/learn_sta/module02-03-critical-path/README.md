# Module 02-03: Critical path

**Module id:** `module02-03-critical-path`  
**Kind:** `lab` · Primary lab: `critical-path` · **Planned**

[← Slack / setup / hold](../module02-01-slack-setup-hold/README.md) · [Course README](../README.md) · [Incremental update →](../module03-01-incremental-update/README.md)

## Outcomes

After this module you can: **Trace the worst (most critical) path from an endpoint back through arrival tags.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **critical-path traceback from worst slack** on the tiny timing netlist.
2. Complete [CHECKLIST.md](CHECKLIST.md) with arrivals, required times, and slack (as applicable).
3. Optional self-check: `./scripts/module.sh 02-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/critical-path/index.html](http://127.0.0.1:8080/tools/critical-path/index.html) *(planned)*
2. Tools shelf: open `critical-path` from the platform tools index when shipped
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
module02-03-critical-path/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
