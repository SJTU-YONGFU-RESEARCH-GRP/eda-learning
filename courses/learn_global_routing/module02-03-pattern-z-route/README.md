# Module 02-03: Z-shape pattern routes

**Module id:** `module02-03-pattern-z-route`  
**Kind:** `lab` · Primary lab: `pattern-z-route` · **ref**

[← L-route](../module02-01-pattern-l-route/README.md) · [Course README](../README.md) · [Maze route →](../module02-05-maze-gcell-route/README.md)

## Outcomes

After this module you can: **Route two-pin nets with a three-segment Z when possible; fall back to L otherwise.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **Z-shape pattern routing (HZ / VH bends)** on `examples/tiny_gr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with edge usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 02-03 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/pattern-z-route/](http://127.0.0.1:8080/tools/pattern-z-route/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/pattern-z-route/](https://universal-verification-methodology.github.io/learning/tools/pattern-z-route/)
3. Tools shelf: open `pattern-z-route` from the platform tools index
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
module02-03-pattern-z-route/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
