# Module 02-05: Maze routing on GCells

**Module id:** `module02-05-maze-gcell-route`  
**Kind:** `lab` · Primary lab: `maze-gcell-route` · **ref**

[← Z-route](../module02-03-pattern-z-route/README.md) · [Course README](../README.md) · [Multipin tree →](../module02-07-multipin-tree/README.md)

## Outcomes

After this module you can: **Find a shortest GCell path with BFS while skipping edges at capacity.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **maze routing (BFS with edge capacity)** on `examples/tiny_gr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with edge usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh 02-05 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/maze-gcell-route/](http://127.0.0.1:8080/tools/maze-gcell-route/)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/maze-gcell-route/](https://universal-verification-methodology.github.io/learning/tools/maze-gcell-route/)
3. Tools shelf: open `maze-gcell-route` from the platform tools index
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
module02-05-maze-gcell-route/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
