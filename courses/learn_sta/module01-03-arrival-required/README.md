# Module 01-03: Arrival and required times

**Module id:** `module01-03-arrival-required`  
**Kind:** `lab` · Primary lab: `arrival-required` · **Planned**

[← Timing graph](../module01-01-timing-graph/README.md) · [Course README](../README.md) · [Slack / setup / hold →](../module02-01-slack-setup-hold/README.md)

## Outcomes

After this module you can: **Propagate arrival forward and required backward on a timing graph with fixed clocks.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **forward arrival and backward required propagation** on the tiny timing netlist.
2. Complete [CHECKLIST.md](CHECKLIST.md) with arrivals, required times, and slack (as applicable).
3. Optional self-check: `./scripts/module.sh 01-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/arrival-required/index.html](http://127.0.0.1:8080/tools/arrival-required/index.html) *(planned)*
2. Tools shelf: open `arrival-required` from the platform tools index when shipped
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
module01-03-arrival-required/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
