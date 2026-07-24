# Module 01-03: Pin terminals on GCells

**Module id:** `module01-03-terminal-gcells`  
**Kind:** `lab` · Primary lab: `terminal-gcells` · **ref**

[← Routing graph](../module01-01-routing-graph/README.md) · [Course README](../README.md) · [L-route →](../module02-01-pattern-l-route/README.md)

## Outcomes

After this module you can: **Map each pin placement to its owning GCell terminal for routing.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **pin terminal GCell assignment** on `examples/tiny_gr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with edge usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 01-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/terminal-gcells/](http://127.0.0.1:8080/tools/terminal-gcells/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/terminal-gcells/](https://universal-verification-methodology.github.io/learning/tools/terminal-gcells/)
3. Tools shelf: open `terminal-gcells` from the platform tools index
4. Load the **starter global routing** instance, run the router, inspect edge overflow.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach global routing literacy on a tiny GCell graph — not production detailed routers.

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
module01-03-terminal-gcells/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
