# Module 03-03: Rip-up and reroute

**Module id:** `module03-03-ripup-reroute`  
**Kind:** `lab` · Primary lab: `ripup-reroute` · **ref**

[← Edge overflow](../module03-01-edge-overflow/README.md) · [Course README](../README.md) · [Sequential GR →](../module04-01-sequential-global/README.md)

## Outcomes

After this module you can: **Rip the hottest congested net and maze-reroute it to reduce edge overflow.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **rip-up and maze reroute** on `examples/tiny_gr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with edge usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 03-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/ripup-reroute/](http://127.0.0.1:8080/tools/ripup-reroute/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/ripup-reroute/](https://universal-verification-methodology.github.io/learning/tools/ripup-reroute/)
3. Tools shelf: open `ripup-reroute` from the platform tools index
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
module03-03-ripup-reroute/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
