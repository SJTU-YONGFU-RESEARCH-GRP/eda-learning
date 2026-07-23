# Timing-driven placement

**Module id:** `module04-01-timing-driven-place`  
**Kind:** `lab` · Primary lab: `timing-driven-place` · **Shipped**

[← Spread / legalize](../module03-03-spread-legalize-lite/README.md) · [Course README](../README.md) · [Offline compare →](../module05-01-offline-benchmark-compare/README.md)

## Outcomes

After this module you can: **Weight critical nets in the HPWL objective and compare plain vs timing-weighted wirelength.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **timing-weighted HPWL placement objective** on the tiny placement.
2. Complete [CHECKLIST.md](CHECKLIST.md) with metrics (HPWL, density / overflow when relevant).
3. Optional self-check: `./scripts/module.sh 04-01 --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/timing-driven-place/index.html](http://127.0.0.1:8080/tools/timing-driven-place/index.html)
2. Tools shelf: open `timing-driven-place` from the platform tools index
3. Load the **starter placement**, run the algorithm, inspect metrics.
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
module04-01-timing-driven-place/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
