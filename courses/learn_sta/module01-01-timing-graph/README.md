# Module 01-01: Timing graph

**Module id:** `module01-01-timing-graph`  
**Kind:** `lab` · Primary lab: `timing-graph` · **Shipped**

[← Welcome](../module00-00-intro/README.md) · [Course README](../README.md) · [Arrival / required →](../module01-03-arrival-required/README.md)

## Outcomes

After this module you can: **Build a levelized timing graph from a tiny netlist and name pin/net delay arcs.**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **timing-graph construction and levelization** on the tiny timing netlist.
2. Run `python3 common/test_timing_graph.py` from `courses/learn_sta/` (or `cd common && python3 test_timing_graph.py`).
3. Complete [CHECKLIST.md](CHECKLIST.md) with pin/arc counts, levels, and path delay.

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/timing-graph/index.html](http://127.0.0.1:8080/tools/timing-graph/index.html)
2. Live: [https://universal-verification-methodology.github.io/learning/tools/timing-graph/](https://universal-verification-methodology.github.io/learning/tools/timing-graph/)
3. Load the **starter** chain, compare with **Show cyclic**, inspect levels / topo / delay sums.
4. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach STA literacy on tiny graphs — not foundry sign-off or vendor GUI flows.

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
module01-01-timing-graph/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
