# Module 03-03: Rip-up and reroute (detailed)

**Module id:** `module03-03-ripup-detailed`  
**Kind:** `lab` · Primary lab: `ripup-detailed` · **ref**

[← DRC spacing](../module03-01-drc-spacing/README.md) · [Course README](../README.md) · [Sequential DR →](../module04-01-sequential-detailed/README.md)

## Outcomes

After this module you can: **Rip the hottest congested net and A*-reroute it to reduce track overflow.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **rip-up and A* reroute on track usage** on `examples/tiny_dr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with track usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 03-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/ripup-detailed/](http://127.0.0.1:8080/tools/ripup-detailed/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/ripup-detailed/](https://universal-verification-methodology.github.io/learning/tools/ripup-detailed/)
3. Tools shelf: open `ripup-detailed` from the platform tools index
4. Load the **starter detailed routing** instance, run the router, inspect track overflow and vias.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach detailed routing literacy on a tiny M1/M2 grid — not production signoff routers.

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
module03-03-ripup-detailed/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
