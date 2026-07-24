# Module 04-01: Sequential detailed route

**Module id:** `module04-01-sequential-detailed`  
**Kind:** `lab` · Primary lab: `sequential-detailed` · **ref**

[← Rip-up DR](../module03-03-ripup-detailed/README.md) · [Course README](../README.md) · [Offline compare →](../module05-01-offline-benchmark-compare/README.md)

## Outcomes

After this module you can: **Route all nets in order with layer-aware paths and measure resulting track congestion.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **sequential detailed routing (ordered net deposit on tracks)** on `examples/tiny_dr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with track usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 04-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/sequential-detailed/](http://127.0.0.1:8080/tools/sequential-detailed/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/sequential-detailed/](https://universal-verification-methodology.github.io/learning/tools/sequential-detailed/)
3. Tools shelf: open `sequential-detailed` from the platform tools index
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
module04-01-sequential-detailed/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
