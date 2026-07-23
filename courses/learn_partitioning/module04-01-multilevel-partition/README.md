# Multilevel partitioning

**Module id:** `module04-01-multilevel-partition`  
**Kind:** `lab` · Primary lab: `multilevel-partition` · **Shipped**

[← Hypergraph](../module03-05-hypergraph-partition/README.md) · [Course README](../README.md) · [Offline compare →](../module05-01-offline-benchmark-compare/README.md)

## Outcomes

After this module you can: **Run a partitioning V-cycle: coarsen, initial partition, project, and refine at each level.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **multilevel coarsen / initial / uncoarsen / refine** on the tiny graphs.
2. Complete [CHECKLIST.md](CHECKLIST.md) with metrics (cutsize, balance, objective).
3. Optional self-check: `./scripts/module.sh 04-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/multilevel-partition/index.html](http://127.0.0.1:8080/tools/multilevel-partition/index.html)
2. Tools shelf: open `multilevel-partition` from the platform tools index
3. Load the **starter graph**, run the algorithm, inspect metrics.
4. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach algorithm literacy on tiny instances — not production PDK flows.

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
module04-01-multilevel-partition/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
