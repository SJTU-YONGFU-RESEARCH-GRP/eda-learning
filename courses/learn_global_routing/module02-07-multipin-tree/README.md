# Module 02-07: Multi-pin tree (Steiner-lite)

**Module id:** `module02-07-multipin-tree`  
**Kind:** `lab` · Primary lab: `multipin-tree` · **ref**

[← Maze route](../module02-05-maze-gcell-route/README.md) · [Course README](../README.md) · [Edge overflow →](../module03-01-edge-overflow/README.md)

## Outcomes

After this module you can: **Connect multi-pin nets with a star from the bbox-center GCell via L legs.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **multipin star tree (bbox-center Steiner-lite)** on `examples/tiny_gr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with edge usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 02-07 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/multipin-tree/](http://127.0.0.1:8080/tools/multipin-tree/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/multipin-tree/](https://universal-verification-methodology.github.io/learning/tools/multipin-tree/)
3. Tools shelf: open `multipin-tree` from the platform tools index
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
module02-07-multipin-tree/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
