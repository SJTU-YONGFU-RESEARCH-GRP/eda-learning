# Module 00-00: Welcome to detailed routing for EDA

**Module id:** `module00-00-intro`  
**Kind:** `intro` · Dual-track course welcome

← Start · [Course README](../README.md) · [Routing grid →](../module01-01-routing-grid/README.md)

## What this course is

**learn_routing** teaches *detailed routing on a track grid* using **two learning modes** on every lab module:

| Track | Where you practice | Best for |
|-------|--------------------|----------|
| **A — Implement** | Tiny grid instance + `EXAMPLES.md` / `examples/` | Fidelity: maze, A*, tracks, vias, DRC |
| **B — Browser lab** | Interactive lab on the learning platform | Concept literacy, quick visual feedback |

You can do **A only**, **B only**, or **both** (recommended: B for intuition when shipped, then A for fidelity).

**Prerequisite:** [learn_global_routing](../learn_global_routing/README.md) — you need GCell global routes and coarse congestion literacy before assigning tracks and vias.

## Setup (Track A)

1. Open this course under `courses/learn_routing/`.
2. Follow [docs/TWO_TRACKS.md](../docs/TWO_TRACKS.md) and each module’s [EXAMPLES.md](EXAMPLES.md).
3. Optional self-check from course root: `./scripts/module.sh SS-AA --check`.

## Setup (Track B)

1. Serve the platform: `python3 -m http.server 8080 --directory platform` (from monorepo root).
2. Open http://127.0.0.1:8080/tools/
3. Or use the live site: https://universal-verification-methodology.github.io/learning/tools/

## How to move through modules

1. Read the module **README** (outcomes).
2. Pick a track (or both).
3. Check off **CHECKLIST.md**.
4. Optional: skim `outline.yaml` / `transcript.md` for upcoming slides & clips.

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
module00-00-intro/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```

## Next

→ [Module 01-01: Routing grid graph](../module01-01-routing-grid/README.md)
