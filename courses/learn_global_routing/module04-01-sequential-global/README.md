# Module 04-01: Sequential global route

**Module id:** `module04-01-sequential-global`  
**Kind:** `lab` · Primary lab: `sequential-global` · **ref**

[← Rip-up](../module03-03-ripup-reroute/README.md) · [Course README](../README.md) · [Offline compare →](../module05-01-offline-benchmark-compare/README.md)

## Outcomes

After this module you can: **Route all nets in order with L patterns and measure resulting edge congestion.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **sequential global routing (ordered net deposit)** on `examples/tiny_gr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with edge usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 04-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/sequential-global/](http://127.0.0.1:8080/tools/sequential-global/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/sequential-global/](https://universal-verification-methodology.github.io/learning/tools/sequential-global/)
3. Tools shelf: open `sequential-global` from the platform tools index
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
module04-01-sequential-global/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
