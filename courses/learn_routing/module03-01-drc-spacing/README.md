# Module 03-01: DRC spacing lite

**Module id:** `module03-01-drc-spacing`  
**Kind:** `lab` · Primary lab: `drc-spacing` · **ref**

[← Via assign](../module02-07-via-assignment/README.md) · [Course README](../README.md) · [Rip-up DR →](../module03-03-ripup-detailed/README.md)

## Outcomes

After this module you can: **Detect same-layer parallel segments that violate minimum spacing on the toy grid.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **DRC spacing lite (parallel same-layer distance check)** on `examples/tiny_dr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with track usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 03-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/drc-spacing/](http://127.0.0.1:8080/tools/drc-spacing/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/drc-spacing/](https://universal-verification-methodology.github.io/learning/tools/drc-spacing/)
3. Tools shelf: open `drc-spacing` from the platform tools index
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
module03-01-drc-spacing/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
