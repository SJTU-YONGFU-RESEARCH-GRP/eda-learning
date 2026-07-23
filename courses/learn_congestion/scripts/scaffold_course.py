#!/usr/bin/env python3
"""Scaffold learn_congestion (hierarchical SS-AA ids) with module-slides stubs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "learn_congestion"
LIVE_TOOLS = "https://universal-verification-methodology.github.io/learning/tools"

MODULES = [
    {
        "id": "module00-00-intro",
        "kind": "intro",
        "title": "Welcome to congestion for EDA",
        "short": "Welcome",
        "lab": None,
        "status": "—",
        "section": "00",
        "outcomes": "Explain why congestion estimation sits between legalization and routing, and what GCells measure.",
        "algorithm": None,
    },
    {
        "id": "module01-01-gcell-grid",
        "kind": "lab",
        "title": "GCell grid model",
        "short": "GCell grid",
        "lab": "gcell-grid",
        "status": "**ref**",
        "section": "01",
        "outcomes": "Map chip coordinates onto a 4×2 GCell grid and report which tile owns a cell center.",
        "algorithm": "GCell grid indexing (nx×ny tiles over chip W×H)",
    },
    {
        "id": "module01-03-capacity-demand",
        "kind": "lab",
        "title": "Capacity vs demand",
        "short": "Capacity / demand",
        "lab": "capacity-demand",
        "status": "**ref**",
        "section": "01",
        "outcomes": "Contrast per-GCell routing capacity with estimated demand and flag oversubscribed tiles.",
        "algorithm": "capacity vs demand comparison per GCell",
    },
    {
        "id": "module02-01-rudy-estimate",
        "kind": "lab",
        "title": "RUDY congestion estimate",
        "short": "RUDY",
        "lab": "rudy-estimate",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Estimate routing demand with RUDY: distribute each net's HPWL density over GCells under its bbox.",
        "algorithm": "RUDY (Rectangular Uniform wire DensitY) demand estimate",
    },
    {
        "id": "module02-03-probabilistic-demand",
        "kind": "lab",
        "title": "Probabilistic routing demand",
        "short": "Probabilistic",
        "lab": "probabilistic-demand",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Estimate demand with L-shape probabilistic routing (half each bend) and compare to RUDY.",
        "algorithm": "probabilistic L-shape routing demand",
    },
    {
        "id": "module02-05-congestion-map",
        "kind": "lab",
        "title": "Congestion heat map",
        "short": "Congestion map",
        "lab": "congestion-map",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Build a congestion heat map as demand/capacity per GCell and name the hottest tile.",
        "algorithm": "congestion heat map (demand / capacity)",
    },
    {
        "id": "module02-07-overflow-metrics",
        "kind": "lab",
        "title": "Overflow metrics",
        "short": "Overflow",
        "lab": "overflow-metrics",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Report total overflow, max overflow, and congested GCell count from a demand map.",
        "algorithm": "overflow metrics (total, max, congested count)",
    },
    {
        "id": "module03-01-cell-inflator",
        "kind": "lab",
        "title": "Cell inflation",
        "short": "Inflator",
        "lab": "cell-inflator",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Inflate cell widths in oversubscribed GCells so the next place pass spreads demand.",
        "algorithm": "cell inflation from congestion (width scale)",
    },
    {
        "id": "module03-03-net-weighting",
        "kind": "lab",
        "title": "Congestion-aware net weighting",
        "short": "Net weighting",
        "lab": "net-weighting",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Raise net weights through congested GCells to pull placement away from hotspots.",
        "algorithm": "congestion-aware net weighting",
    },
    {
        "id": "module04-01-placement-feedback",
        "kind": "lab",
        "title": "Placement feedback loop",
        "short": "Place feedback",
        "lab": "placement-feedback",
        "status": "**ref**",
        "section": "04",
        "outcomes": "Run one estimate→inflate→push feedback pass and show overflow drop on the tiny instance.",
        "algorithm": "placement feedback (estimate → inflate → push)",
    },
    {
        "id": "module05-01-offline-benchmark-compare",
        "kind": "offline",
        "title": "Offline benchmark compare",
        "short": "Offline compare",
        "lab": None,
        "status": "P",
        "section": "05",
        "outcomes": "Compare toy congestion estimators on shared instances (overflow, runtime, notes).",
        "algorithm": "benchmark harness vs reference congestion maps",
    },
    {
        "id": "module99-00-wrap",
        "kind": "wrap",
        "title": "Congestion path complete",
        "short": "Wrap",
        "lab": None,
        "status": "—",
        "section": "99",
        "outcomes": "Recap GCells, RUDY, overflow, inflators; choose global routing or CTS next.",
        "algorithm": None,
    },
]


def prev_next(i: int) -> tuple[dict | None, dict | None]:
    prev_m = MODULES[i - 1] if i > 0 else None
    next_m = MODULES[i + 1] if i + 1 < len(MODULES) else None
    return prev_m, next_m


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def ss_aa(m: dict) -> str:
    parts = m["id"].replace("module", "", 1).split("-")
    return f"{parts[0]}-{parts[1]}"


def nav_line(prev_m, next_m) -> str:
    left = f"[← {prev_m['short']}](../{prev_m['id']}/README.md)" if prev_m else "← Start"
    right = f"[{next_m['short']} →](../{next_m['id']}/README.md)" if next_m else "End →"
    return f"{left} · [Course README](../README.md) · {right}"


def lab_badge(m: dict) -> str:
    if m["kind"] == "lab":
        return f"**Kind:** `lab` · Primary lab: `{m['lab']}` · **ref**"
    if m["kind"] == "offline":
        return "**Kind:** `offline` · Primary activity: local benchmark harness · **Planned**"
    if m["kind"] == "intro":
        return "**Kind:** `intro` · Dual-track course welcome"
    return f"**Kind:** `{m['kind']}`"


def tiny_cong() -> dict:
    return {
        "chip": {"W": 12, "H": 8},
        "gcell": {"nx": 4, "ny": 2, "cellW": 3, "cellH": 4},
        "capacity": 2.0,
        "cells": [
            {"id": "A", "width": 2, "height": 1},
            {"id": "B", "width": 2, "height": 1},
            {"id": "C", "width": 2, "height": 1},
            {"id": "D", "width": 2, "height": 1},
            {"id": "E", "width": 1, "height": 1},
            {"id": "F", "width": 1, "height": 1},
        ],
        "nets": [
            ["A", "B"],
            ["C", "D"],
            ["A", "C"],
            ["B", "D"],
            ["A", "B", "C", "D"],
            ["E", "F"],
        ],
        "placement": {
            "A": {"x": 1, "y": 1},
            "B": {"x": 8, "y": 1},
            "C": {"x": 1, "y": 5},
            "D": {"x": 8, "y": 5},
            "E": {"x": 5, "y": 3},
            "F": {"x": 6, "y": 3},
        },
        "congested_seed": {
            "A": {"x": 4, "y": 2},
            "B": {"x": 5, "y": 2},
            "C": {"x": 4, "y": 3},
            "D": {"x": 5, "y": 3},
            "E": {"x": 4.5, "y": 2.5},
            "F": {"x": 5.5, "y": 2.5},
        },
        "notes": "4×2 GCells over 12×8 chip. placement=spread; congested_seed=center cluster.",
    }


def tiny_cong_json() -> str:
    return json.dumps(tiny_cong(), indent=2) + "\n"


PSEUDO: dict[str, str] = {
    "gcell-grid": """## Pseudocode

```text
Input: chip W×H, gcell nx×ny (cellW=W/nx, cellH=H/ny), point (x,y)
i ← clamp(floor(x / cellW), 0, nx-1)
j ← clamp(floor(y / cellH), 0, ny-1)
Output: GCell index (i, j)  # column i, row j from lower-left
Golden: A at (1,1) → (0,0); D at (8,5) → (2,1)
```
""",
    "capacity-demand": """## Pseudocode

```text
Input: demand[nx][ny], capacity Cap (scalar or per-tile)
for each GCell (i,j):
  surplus[i][j] ← demand[i][j] − Cap
  oversubscribed ← surplus[i][j] > 0
Output: surplus map + list of oversubscribed tiles
```
""",
    "rudy-estimate": """## Pseudocode

```text
Input: nets, positions, GCell grid, Cap
demand ← zeros(nx, ny)
for each net N:
  bbox ← axis-aligned box of pin positions
  hpwl ← width(bbox) + height(bbox)
  tiles ← GCells overlapping bbox (at least 1)
  area ← max(1, #tiles)          # toy uniform share
  dens ← hpwl / area
  for each tile t in tiles:
    demand[t] ← demand[t] + dens
Output: demand matrix; overflow = max(0, demand−Cap)
```
""",
    "probabilistic-demand": """## Pseudocode

```text
Input: nets, positions, GCell grid
demand ← zeros(nx, ny)
for each 2-pin net (u,v):
  add 0.5 demand along L-shape H-then-V through GCells
  add 0.5 demand along L-shape V-then-H through GCells
for each multi-pin net:
  c ← bbox center; star edges c→pin; deposit like 2-pin
Output: demand matrix (compare to RUDY on same placement)
```
""",
    "congestion-map": """## Pseudocode

```text
Input: demand[nx][ny], Cap
for each (i,j):
  cong[i][j] ← demand[i][j] / Cap
hottest ← argmax cong
Output: congestion heat map + hottest GCell
```
""",
    "overflow-metrics": """## Pseudocode

```text
Input: demand, Cap
ov[i][j] ← max(0, demand[i][j] − Cap)
total ← sum(ov);  maxov ← max(ov);  count ← #{ov>0}
Output: {total, max, count, perCell: ov}
```
""",
    "cell-inflator": """## Pseudocode

```text
Input: positions, widths, congestion, alpha (e.g. 0.5)
for each cell c:
  (i,j) ← GCell of center(c)
  if cong[i][j] > 1:
    widths'[c] ← widths[c] * (1 + alpha*(cong[i][j]−1))
  else:
    widths'[c] ← widths[c]
Output: inflated widths (placement coords unchanged)
```
""",
    "net-weighting": """## Pseudocode

```text
Input: nets, positions, congestion, beta (e.g. 1.0)
for each net N:
  tiles ← GCells under bbox(N)
  mean ← average cong over tiles
  w[N] ← 1 + beta * mean
Output: weight per net (hot nets get larger w)
```
""",
    "placement-feedback": """## Pseudocode

```text
Input: positions, Cap, alpha
demand ← RUDY(positions)
cong ← demand / Cap
widths' ← inflate(positions, cong, alpha)
# push: move each cell from high-ov GCell toward lowest-ov neighbor
for each movable cell c:
  if overflow(center(c)) > 0:
    step c toward neighbor GCell with least overflow
positions' ← updated coords
Output: positions' with lower total overflow (toy one-pass)
```
""",
}


def readme(m: dict, i: int) -> str:
    prev_m, next_m = prev_next(i)
    mid = m["id"]
    key = ss_aa(m)
    header = (
        f"# Module {key}: {m['title']}\n\n"
        f"**Module id:** `{mid}`  \n"
        f"{lab_badge(m)}\n\n"
        f"{nav_line(prev_m, next_m)}\n"
    )
    if m["kind"] == "lab":
        lab = m["lab"]
        body = f"""
## Outcomes

After this module you can: **{m['outcomes']}**

## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **{m['algorithm']}** on `examples/tiny_cong.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with demand, congestion, and overflow when relevant.
3. Optional self-check: `./scripts/module.sh {key} --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/{lab}/](http://127.0.0.1:8080/tools/{lab}/)
2. Live: [{LIVE_TOOLS}/{lab}/]({LIVE_TOOLS}/{lab}/)
3. Tools shelf: open `{lab}` from the platform tools index
4. Load the **starter congestion** instance, run the estimator, inspect overflow metrics.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach congestion literacy on a tiny GCell grid — not production global routers.
"""
    elif m["kind"] == "offline":
        body = f"""
## Outcomes

After this module you can: **{m['outcomes']}**

## Offline track

1. Follow [EXAMPLES.md](EXAMPLES.md) to run the local compare harness.
2. Record overflow totals and runtime against at least one reference when available.
3. Complete [CHECKLIST.md](CHECKLIST.md).
"""
    elif m["kind"] == "intro":
        body = """
## What this course is

**learn_congestion** teaches *routing demand estimation and placement feedback* using **two learning modes** on every lab module:

| Track | Where you practice | Best for |
|-------|--------------------|----------|
| **A — Implement** | Tiny GCell instance + `EXAMPLES.md` / `examples/` | Fidelity: RUDY, overflow, inflators |
| **B — Browser lab** | Interactive lab on the learning platform | Concept literacy, quick visual feedback |

You can do **A only**, **B only**, or **both** (recommended: B for intuition when shipped, then A for fidelity).

**Prerequisite:** [learn_placement](../learn_placement/README.md) / [learn_legalization](../learn_legalization/README.md) — you need a placed (or legalized) netlist before estimating congestion.

## Setup (Track A)

1. Open this course under `courses/learn_congestion/`.
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
"""
    else:
        body = """
## You can now

- Index cells onto a GCell grid and compare capacity vs demand
- Estimate demand with RUDY and probabilistic L-shapes
- Build congestion maps and report overflow metrics
- Inflate cells / reweight nets and run a one-pass placement feedback

## Dual-track recap

If you mainly used **browser labs**, spend a short session on Track A for RUDY and overflow metrics.
If you mainly used **Track A**, skim any skipped shipped browser labs for visual heat maps.

## Next course

Prereqs done: **learn_placement** / **learn_legalization**.

→ **learn_global_routing** or **learn_clock_tree** (see parent [`eda.md`](../../../eda.md))

## Checklist

- [ ] I completed Track A and/or Track B for the lab modules I care about
- [ ] I can explain RUDY vs overflow vs inflators in my own words
- [ ] I know which next course to open
"""

    media = f"""
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
{mid}/
├── README.md
├── CHECKLIST.md
├── EXAMPLES.md
├── outline.yaml
├── transcript.md
├── quiz.json
└── (optional) examples/ · assets/
```
"""
    if m["kind"] == "intro":
        nxt = MODULES[1]
        media += f"\n## Next\n\n→ [Module {ss_aa(nxt)}: {nxt['title']}](../{nxt['id']}/README.md)\n"
    return header + body + media


def checklist(m: dict) -> str:
    if m["kind"] == "lab":
        return f"""# Checklist — {m['title']}

## Track A — Implement

- [ ] Worked through the prompts in [EXAMPLES.md](EXAMPLES.md)
- [ ] Implemented **{m['algorithm']}** end-to-end on `examples/tiny_cong.json`
- [ ] Reported demand / congestion / overflow when relevant
- [ ] Can explain the algorithm without the UI

## Track B — Browser lab (`{m['lab']}`)

- [ ] Opened the lab (local or live)
- [ ] Loaded the starter congestion instance
- [ ] Ran the estimator and inspected overflow metrics

## Done when

- [ ] I can reproduce the result on paper/code **or** I finished the browser challenges (preferably both)
"""
    if m["kind"] == "offline":
        return f"""# Checklist — {m['title']}

## Offline harness

- [ ] Ran the compare script on at least one shared instance
- [ ] Recorded toy-engine vs reference metrics (or documented tool missing)
- [ ] Named one discrepancy and a hypothesis

## Done when

- [ ] I can explain how to judge congestion quality across estimators
"""
    if m["kind"] == "intro":
        return f"""# Checklist — {m['title']}

- [ ] I understand the course map (sections 01–05 + wrap)
- [ ] I know Track A (implement) vs Track B (browser lab)
- [ ] I opened [docs/MODULES.md](../docs/MODULES.md) once
- [ ] I finished learn_placement / learn_legalization or know why congestion follows place
- [ ] Ready for the GCell grid model
"""
    return f"""# Checklist — {m['title']}

- [ ] I can name the main congestion ideas from sections 01–04
- [ ] I know when RUDY vs probabilistic vs inflators fits
- [ ] I picked a next course (`learn_global_routing` or `learn_clock_tree`)
"""


def examples(m: dict) -> str:
    if m["kind"] == "lab":
        lab = m["lab"]
        pseudo = PSEUDO.get(lab, "## Pseudocode\n\n```text\n(see common/solvers.py)\n```\n")
        return f"""# Examples — {m['title']}

Track A (implement). Use the tiny congestion instance first (`examples/tiny_cong.json`).

## Algorithm

**{m['algorithm']}**

{pseudo}

## Track A API

```bash
# from courses/learn_congestion/
python3 -c "from common.solvers import *; from common.congestionutil import load; d=load('common/tiny_cong.json'); print(d['chip'])"
```

Prefer helpers in `common/congestionutil.py` and `common/solvers.py` over ad-hoc scripts.

## Starter prompts

1. Load `placement` and `congested_seed` from `tiny_cong.json`; print the 4×2 GCell layout.
2. Run the algorithm for this lab; print demand or congestion matrices with two decimals.
3. Compare spread `placement` vs `congested_seed` on total overflow.
4. Change capacity from 2.0 to 1.0 and report which GCells flip oversubscribed.
5. Write one sentence: why this idea belongs before detailed global routing.

## Expected artifacts

- Demand and/or congestion matrix for the 4×2 grid
- Overflow summary (total, max, count) when relevant
- Short note tying the metric to placement feedback
"""
    if m["kind"] == "offline":
        return """# Examples — Offline benchmark compare

1. Export the same tiny_cong instance used in RUDY / overflow labs.
2. Run your toy estimator; record total overflow, max overflow, wall time.
3. If available, compare against a reference congestion map.
4. Fill a comparison table: quality, overflow, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
"""
    if m["kind"] == "intro":
        return """# Examples — Welcome

No coding yet.

1. Sketch the PD path: place → legalize → **congestion estimate** → CTS / global route.
2. Write one sentence: “Congestion maps exist because …”
3. Name one difference between density bins (placement) and GCell demand (routing).
"""
    return """# Examples — Wrap

1. List three congestion algorithms from this course and one strength each.
2. For a center-clustered placement, which module’s idea do you reach for first?
3. Write the bridge sentence you’ll need for global routing next.
"""


LAB_TRANSCRIPTS: dict[str, str] = {
    "gcell-grid": """# GCell grid model

**Module id:** module01-01-gcell-grid
**Lab:** gcell-grid
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Why GCells

After legalization you have legal cell sites, but routers still think in coarser tiles called GCells. Our toy chip is twelve by eight. We overlay a four by two grid: each GCell is three wide and four tall. Congestion literacy starts by naming which tile owns a point.

## Slide 2 — The idea

Index with lower-left origin. Column i is floor of x over cell width, clamped to zero through three. Row j is floor of y over cell height, clamped to zero or one. Cell A at one comma one lands in GCell zero comma zero. Cell D at eight comma five lands in two comma one. Memorize that mapping—every estimator reuses it.

## Slide 3 — Browser lab track

Open the **gcell-grid** lab. Move a cell and read the GCell index in the metrics panel. Paint the grid lines so the four-by-two tiling is obvious. Then encode the same clamp-and-floor rule in Track A.

## Slide 4 — Implement track

Parse `tiny_cong.json`. Print nx, ny, cellW, cellH. Write `cell_gcell(x, y)` returning (i, j). Assert A→(0,0) and D→(2,1) on the spread placement. No demand yet—this module is pure geometry.

## Slide 5 — Pitfalls

Using upper-left image coordinates instead of chip lower-left. Forgetting to clamp points on the right or top edge into the last tile. Mixing site columns from legalization with GCell columns—different grids.

## Slide 6 — Your turn

Finish the checklist. Be able to sketch the eight GCells from memory. Next: capacity versus demand—the supply side of the map.
""",
    "capacity-demand": """# Capacity vs demand

**Module id:** module01-03-capacity-demand
**Lab:** capacity-demand
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Supply and load

A GCell has a routing budget—capacity. Estimators deposit demand into the same tiles. When demand exceeds capacity the tile is oversubscribed. On our toy instance capacity is two point zero for every GCell unless you change it.

## Slide 2 — The idea

Surplus equals demand minus capacity. Positive surplus means overflow. List oversubscribed tiles before you trust a heat map. Capacity can later become anisotropic edge capacities; here it is a scalar so goldens stay simple.

## Slide 3 — Browser lab track

Open **capacity-demand**. Toggle capacity between one and two while holding a fixed demand seed. Watch which tiles flip. Check challenges that score your capacity choice against overflow counts—not a “show golden” click.

## Slide 4 — Implement track

Given a demand matrix from RUDY (or a hand-filled stub), compute surplus and the oversubscribed set. Print both for capacity equals two and capacity equals one. Keep the API ready for the overflow-metrics lab.

## Slide 5 — Pitfalls

Comparing demand to capacity without documenting units. Treating zero demand as “healthy” while ignoring that neighboring tiles may be hot. Changing capacity mid-challenge without resetting the starter placement.

## Slide 6 — Your turn

Complete Track A or B. Next: RUDY—the classic demand estimator that fills those tiles from net bounding boxes.
""",
    "rudy-estimate": """# RUDY congestion estimate

**Module id:** module02-01-rudy-estimate
**Lab:** rudy-estimate
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Uniform wire density

RUDY—Rectangular Uniform wire DensitY—spreads each net’s wirelength evenly across GCells under its bounding box. It is fast, deterministic, and good enough to teach overflow before you build a full global router.

## Slide 2 — The idea

For each net, take the axis-aligned bbox of pin positions. Half-perimeter wirelength is width plus height. Collect overlapping GCells—at least one. Density equals HPWL divided by the tile count. Add that density into every overlapping tile. Sum across nets for the demand map.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **rudy-estimate**. Start from the spread placement, then load the congested seed and watch center tiles heat up. Check challenges against your demand totals. Reveal golden is study-only.

## Slide 4 — Implement track

Implement `rudy_demand(positions)` in `common/solvers.py`. On `congested_seed`, print the four-by-two demand matrix and total overflow at capacity two. Match the browser golden within a small rounding tolerance.

## Slide 5 — Pitfalls

Dividing by bbox area in continuous units while depositing into discrete tiles inconsistently. Skipping nets with coincident pins—still touch one GCell. Mutating the demand matrix in place across calls without zeroing.

## Slide 6 — Your turn

Ship Track A RUDY and clear the browser challenges. Next: probabilistic L-shapes for a different demand signature.
""",
    "probabilistic-demand": """# Probabilistic routing demand

**Module id:** module02-03-probabilistic-demand
**Lab:** probabilistic-demand
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — L-shape routes

RUDY paints the whole bbox. Probabilistic demand instead assumes two-pin nets route on L-shapes: half the probability goes horizontal-then-vertical, half the other bend. That concentrates demand on corridors instead of the filled rectangle.

## Slide 2 — The idea

For a two-pin net, walk GCells along each L and add one half unit of demand per walk (toy scaling). Multi-pin nets: star from the bbox center to each pin and deposit like two-pin edges. Compare the resulting matrix to RUDY on the same placement.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **probabilistic-demand**. Toggle RUDY versus probabilistic overlays. Note which center tiles differ. Challenges score your placement’s probabilistic overflow, not which button you clicked.

## Slide 4 — Implement track

Implement `probabilistic_demand`. On spread placement, print both RUDY and probabilistic totals. Explain one tile where they disagree and why.

## Slide 5 — Pitfalls

Double-counting the corner GCell on both L legs. Forgetting multi-pin nets. Scaling probabilistic deposits so differently from RUDY that overflow comparisons become meaningless—document your unit choice.

## Slide 6 — Your turn

Clear the checklist. Next: turn demand into a congestion heat map.
""",
    "congestion-map": """# Congestion heat map

**Module id:** module02-05-congestion-map
**Lab:** congestion-map
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Demand over capacity

Congestion is a ratio: demand divided by capacity. A heat map paints that ratio per GCell so you can point at the hottest tile without reading a matrix of floats aloud.

## Slide 2 — The idea

cong[i][j] equals demand[i][j] over Cap. Values above one are oversubscribed. The hottest GCell is the argmax. On the congested seed, expect the center columns to light up first.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **congestion-map**. Read the heat legend. Move cells until a different GCell becomes hottest, then Check. Study reveal shows a reference map—do not rely on it to pass.

## Slide 4 — Implement track

Build `congestion_map(demand, capacity)` returning the ratio matrix and hottest index. Print hottest for both placement seeds.

## Slide 5 — Pitfalls

Dividing by zero capacity. Coloring by raw demand while labeling the plot “congestion.” Breaking ties in argmax nondeterministically—pick a fixed scan order.

## Slide 6 — Your turn

Finish the lab. Next: overflow metrics compress the map into totals you can regress.
""",
    "overflow-metrics": """# Overflow metrics

**Module id:** module02-07-overflow-metrics
**Lab:** overflow-metrics
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Numbers that regress

Overflow is demand above capacity. Sum it, take the max, and count how many GCells overflow. Those three numbers become your regression bar for estimators and feedback loops.

## Slide 2 — The idea

ov equals max of zero and demand minus Cap, per tile. Total is the sum. Max is the worst tile. Count is how many tiles have positive overflow. Report all three every time you change placement.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **overflow-metrics**. Start from congested_seed. Move cells outward until total overflow drops below a challenge threshold. Check reads your positions through RUDY—not a mode flag.

## Slide 4 — Implement track

Implement `overflow_metrics`. Assert congested_seed has higher total overflow than spread placement at Cap equals two. Print the triple (total, max, count).

## Slide 5 — Pitfalls

Reporting negative “overflow.” Counting tiles with congestion greater than one while computing overflow from a different Cap. Comparing totals across estimators with incompatible demand units.

## Slide 6 — Your turn

Hit the overflow targets. Next: cell inflation—the first feedback knob.
""",
    "cell-inflator": """# Cell inflation

**Module id:** module03-01-cell-inflator
**Lab:** cell-inflator
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Make hot cells larger

Inflators tell the placer that cells in congested GCells should act bigger, encouraging spreading on the next pass. On the toy grid we scale width: width prime equals width times one plus alpha times congestion minus one, when congestion is above one.

## Slide 2 — The idea

Map each cell center to a GCell. If that tile’s congestion exceeds one, inflate; otherwise leave width alone. Alpha around zero point five keeps the demo visible without exploding geometry. Coordinates stay put—this lab changes widths, not x y.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **cell-inflator**. Run inflate on congested_seed and read which cells grew. Challenges verify inflated widths from your congestion state.

## Slide 4 — Implement track

Implement `inflate_cells` with alpha equals zero point five. Print before/after widths for cells sitting in oversubscribed tiles.

## Slide 5 — Pitfalls

Inflating every cell when only some GCells are hot. Inflating height when the placer model only tracks width. Applying inflation twice without resetting to base widths.

## Slide 6 — Your turn

Clear the inflator challenges. Next: net weighting—the wirelength-side knob.
""",
    "net-weighting": """# Congestion-aware net weighting

**Module id:** module03-03-net-weighting
**Lab:** net-weighting
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Pull soft from hotspots

Net weighting raises the cost of nets that cross congested GCells so a weighted placer pulls those pins apart. Weight equals one plus beta times mean congestion under the net bbox.

## Slide 2 — The idea

For each net, average congestion over GCells under its bbox. Scale with beta—one point zero is a clear demo. The four-pin net on a clustered seed should outrank the short E–F net.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **net-weighting**. Compare weights on spread versus congested seeds. Challenges check that a hot net’s weight exceeds a cool net’s weight on your map.

## Slide 4 — Implement track

Implement `net_weights_from_congestion`. Print the six weights for congested_seed. Confirm net index four is among the highest.

## Slide 5 — Pitfalls

Averaging over the whole chip instead of the net bbox. Using demand instead of congestion ratios. Updating weights but forgetting the placer still optimizes unweighted HPWL in the toy lab.

## Slide 6 — Your turn

Finish weighting. Next: one full placement feedback pass.
""",
    "placement-feedback": """# Placement feedback loop

**Module id:** module04-01-placement-feedback
**Lab:** placement-feedback
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Close the loop

Congestion estimation matters when it changes placement. One toy pass: RUDY → congestion → inflate → push cells from overflowing GCells toward quieter neighbors → remeasure overflow.

## Slide 2 — The idea

After inflation, each movable cell in an overflowing tile takes a step toward the neighbor GCell with least overflow. Clamp to the chip. Recompute RUDY. On congested_seed you should see total overflow drop after one pass—not to zero, but clearly down.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **placement-feedback**. Run the feedback helper, then nudge further if needed to clear challenges. Check scores post-feedback overflow from your positions.

## Slide 4 — Implement track

Implement `placement_feedback_lite`. Print overflow before and after on congested_seed. Assert after is strictly less than before at Cap equals two.

## Slide 5 — Pitfalls

Pushing macros that should stay fixed. Infinite oscillation from oversized steps—use a fraction of GCell size. Declaring victory without recomputing demand after the move.

## Slide 6 — Your turn

Complete the feedback lab and offline compare next. Then the wrap points you to global routing.
""",
}


def transcript_lab(m: dict) -> str:
    return LAB_TRANSCRIPTS.get(
        m["lab"],
        f"""# {m['title']}

**Module id:** {m['id']}
**Lab:** {m['lab']}
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Title

{m['outcomes']}

## Slide 2 — The idea

{m['algorithm']}

## Slide 3 — Browser lab track

Open the **{m['lab']}** lab and explore the starter.

## Slide 4 — Implement track

Work through EXAMPLES.md on tiny_cong.json.

## Slide 5 — Pitfalls

Watch units, clamping, and deterministic goldens.

## Slide 6 — Your turn

Complete the checklist for at least one track.
""",
    )


def transcript_intro() -> str:
    return """# Welcome to congestion for EDA

**Module id:** module00-00-intro
**Lab:** none
**Tracks:** intro (dual-track welcome)

## Slide 1 — Congestion in the stack

You placed and legalized cells. Routers still need room in each GCell. This course teaches how to estimate demand, read overflow, and feed congestion back into placement—before you open a full global router.

## Slide 2 — Two tracks

Track B is the browser lab: drag cells, watch heat maps, clear challenges. Track A is implement: Python solvers on a tiny JSON instance. Use either or both. Browser first for intuition is fine.

## Slide 3 — Course map

Foundations cover GCells and capacity. Estimation covers RUDY, probabilistic demand, heat maps, and overflow metrics. Feedback covers inflators, net weights, and one placement loop. Offline compare and wrap close the path.

## Slide 4 — Prerequisites

Finish learn_placement or learn_legalization first so float versus legal coordinates already make sense. Density bins from placement are cousins—not the same as routing GCells.

## Slide 5 — How to move

Read each module README, pick a track, check the checklist, then skim the clip when media is available. Odd module slots leave room to insert algorithms later without renumbering.

## Slide 6 — Next

Open the GCell grid model and learn the four-by-two tiling by heart.
"""


def transcript_wrap() -> str:
    return """# Congestion path complete

**Module id:** module99-00-wrap
**Lab:** none
**Tracks:** recap · next course

## Slide 1 — You can now

You can index GCells, compare capacity to demand, estimate with RUDY and L-shapes, report overflow, inflate cells, reweight nets, and run a one-pass placement feedback on a tiny chip.

## Slide 2 — Dual-track recap

If you stayed in the browser, implement RUDY and overflow once in Python. If you stayed in Track A, skim the heat-map lab so the colors match your matrices.

## Slide 3 — Pitfalls to remember

Units between estimators, clamp-and-floor GCell indexing, and never treating “reveal golden” as the solve path.

## Slide 4 — Next course

Natural next steps are learn_global_routing—GCells with real edge capacities—or learn_clock_tree if you continue the PD spine toward CTS.

## Slide 5 — Checklist

Name three algorithms and one strength each. Say which idea you reach for on a center-clustered seed. Pick your next course README.

## Slide 6 — Close

When you are ready, take the short quiz, then open the next course.
"""


def transcript_offline() -> str:
    return """# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none
**Tracks:** offline harness

## Slide 1 — Why compare

Toy estimators need a harness: same JSON in, overflow and runtime out. Comparing engines teaches you what “better congestion” means beyond a pretty heat map.

## Slide 2 — The idea

Fix the instance. Run RUDY and probabilistic. Record total overflow, max overflow, wall time. Optionally compare to a reference map. Write one discrepancy hypothesis.

## Slide 3 — Harness shape

A small Python driver loading tiny_cong.json is enough. Print a markdown table. Missing external tools are OK—document blockers and still validate I/O.

## Slide 4 — Pitfalls

Changing Cap between rows of the table. Comparing incompatible demand units. Optimizing runtime before correctness.

## Slide 5 — Your turn

Fill one comparison table for spread versus congested seeds. Then open the wrap.
"""


def outline_stub(m: dict) -> str:
    return f"""# outline — {m['id']}
# Regenerated from transcript.md via transcript_to_outline.py
course: {COURSE_ID}
module: {m['id']}
title: {m['title']}
slides: []
"""


def quiz(m: dict) -> list:
    if m["kind"] == "lab":
        lab = m["lab"]
        return [
            {
                "id": f"{lab}-q1",
                "type": "mcq",
                "prompt": f"This lab’s primary algorithm is best described as…",
                "choices": [
                    m["algorithm"],
                    "Detailed maze routing with rip-up",
                    "Abacus row packing",
                    "Liberty timing arcs",
                ],
                "answer": 0,
            },
            {
                "id": f"{lab}-q2",
                "type": "mcq",
                "prompt": "Our toy chip GCell grid is…",
                "choices": ["4×2 over 12×8", "2×2 over 8×8", "3 rows of sites", "16×16 GCells"],
                "answer": 0,
            },
            {
                "id": f"{lab}-q3",
                "type": "mcq",
                "prompt": "Overflow on a GCell is…",
                "choices": [
                    "max(0, demand − capacity)",
                    "demand × capacity",
                    "HPWL only",
                    "Always zero after legalization",
                ],
                "answer": 0,
            },
        ]
    if m["kind"] == "intro":
        return [
            {
                "id": "intro-q1",
                "type": "mcq",
                "prompt": "Congestion estimation typically sits…",
                "choices": [
                    "After place/legalize, before or with global routing",
                    "Before synthesis",
                    "Only inside SPICE",
                    "Instead of STA",
                ],
                "answer": 0,
            },
            {
                "id": "intro-q2",
                "type": "mcq",
                "prompt": "Track B in this course means…",
                "choices": [
                    "Browser lab challenges on the platform",
                    "Vendor GUI certification",
                    "Only PDF reading",
                    "FPGA bitstream gen",
                ],
                "answer": 0,
            },
            {
                "id": "intro-q3",
                "type": "mcq",
                "prompt": "A GCell is…",
                "choices": [
                    "A coarse routing tile on the chip grid",
                    "A Liberty cell arc",
                    "A scan flop",
                    "A PDK layer stack",
                ],
                "answer": 0,
            },
        ]
    if m["kind"] == "wrap":
        return [
            {
                "id": "wrap-q1",
                "type": "mcq",
                "prompt": "RUDY estimates demand by…",
                "choices": [
                    "Spreading net HPWL density over GCells under the bbox",
                    "Running A* on every net",
                    "Legalizing to sites",
                    "Building BDDs",
                ],
                "answer": 0,
            },
            {
                "id": "wrap-q2",
                "type": "mcq",
                "prompt": "A natural next course after congestion is…",
                "choices": [
                    "learn_global_routing or learn_clock_tree",
                    "learn_unix only",
                    "learn_spice first always",
                    "Skip to ML-EDA",
                ],
                "answer": 0,
            },
            {
                "id": "wrap-q3",
                "type": "mcq",
                "prompt": "Cell inflation responds to congestion by…",
                "choices": [
                    "Scaling widths in hot GCells for the next place pass",
                    "Deleting nets",
                    "Changing the PDK",
                    "Disabling RUDY",
                ],
                "answer": 0,
            },
        ]
    return [
        {
            "id": "offline-q1",
            "type": "mcq",
            "prompt": "A fair estimator compare keeps constant…",
            "choices": ["Instance and capacity", "Random Cap per row", "Different netlists silently", "Wall-clock only"],
            "answer": 0,
        },
        {
            "id": "offline-q2",
            "type": "mcq",
            "prompt": "Useful regression metrics include…",
            "choices": [
                "Total overflow, max overflow, runtime",
                "Only screenshot brightness",
                "Git commit hash alone",
                "Font size",
            ],
            "answer": 0,
        },
        {
            "id": "offline-q3",
            "type": "mcq",
            "prompt": "If a reference tool is missing you should…",
            "choices": [
                "Document blockers and still validate harness I/O",
                "Skip the module silently",
                "Invent fake golden numbers",
                "Delete the JSON",
            ],
            "answer": 0,
        },
    ]


def write_docs() -> None:
    write(
        ROOT / "docs" / "SCOPE.md",
        f"""# {COURSE_ID} — scope

## In scope

- GCell grid model on a tiny chip (4×2 over 12×8)
- Capacity vs demand literacy
- RUDY and probabilistic L-shape demand estimates
- Congestion heat maps and overflow metrics (total, max, count)
- Cell inflation and congestion-aware net weighting
- One-pass placement feedback (estimate → inflate → push)
- Offline compare harness on shared JSON

## Out of scope (v1)

- Production global routers / OpenROAD congestion reports as the syllabus spine
- Full rip-up-and-reroute detailed routing (see `learn_routing`)
- Vendor GUI certification
- Foundry PDK capacity tables

## Shared instance

`common/tiny_cong.json` — see `common/README.md`.
""",
    )
    write(
        ROOT / "docs" / "TWO_TRACKS.md",
        f"""# {COURSE_ID} — two tracks

| Track | Practice | Evidence |
|-------|----------|----------|
| **A — Implement** | `common/` solvers + per-module `examples/tiny_cong.json` | Overflow / demand printouts, checklist |
| **B — Browser lab** | `platform/tools/<lab-id>/` interactive challenges | Cleared challenges on learner state |

Recommended: B for intuition, A for fidelity. Either alone is valid.
""",
    )
    labs = [m for m in MODULES if m["kind"] == "lab"]
    rows = "\n".join(
        f"| `{m['lab']}` | `{m['id']}` | 5 | pending capture |" for m in labs
    )
    write(
        ROOT / "docs" / "WALKTHROUGHS.md",
        f"""# {COURSE_ID} — algorithm walkthroughs

Step frames live under each lab’s `assets/steps/` after capture.

| Lab id | Module | Steps | Status |
|--------|--------|------:|--------|
{rows}

Preview: `platform/tools/algorithm-walkthrough/?algo=<lab-id>&step=1`

Capture (WSL, server on :8080):

```bash
bash courses/{COURSE_ID}/scripts/capture_all_walkthroughs.sh
```
""",
    )


def write_modules_md() -> None:
    rows = []
    for m in MODULES:
        lab = f"`{m['lab']}`" if m["lab"] else ("offline harness" if m["kind"] == "offline" else "—")
        rows.append(
            f"| `{m['id']}` | `{m['kind']}` | [{m['title']}](../{m['id']}/README.md) | {lab} | {m['status']} |"
        )
    write(
        ROOT / "docs" / "MODULES.md",
        f"""# {COURSE_ID} — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
{chr(10).join(rows)}

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (GCell grid, capacity vs demand) |
| `02` | Estimation (RUDY, probabilistic, map, overflow) |
| `03` | Feedback knobs (inflator, net weighting) |
| `04` | Placement feedback loop |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs

Map: [WALKTHROUGHS.md](WALKTHROUGHS.md).

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/{COURSE_ID}/scripts/build_all_media.sh
```
""",
    )


def write_course_readme() -> None:
    landings = "\n".join(
        f"| `{ss_aa(m)}` | [{m['title']}]({m['id']}/README.md) | `{m['kind']}` |" for m in MODULES
    )
    lab_links = ", ".join(f"`{m['lab']}`" for m in MODULES if m["lab"])
    write(
        ROOT / "README.md",
        f"""# {COURSE_ID}

[![GitHub](https://img.shields.io/badge/github-learning-monorepo-blank)](https://github.com/universal-verification-methodology)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-blue)](../../eda.md)
[![Parent](https://img.shields.io/badge/parent-eda__learning-informational)](../../README.md)
[![Labs](https://img.shields.io/badge/labs-platform%20tools-success)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-congestion-orange)](docs/MODULES.md)

**{COURSE_ID}** is the open learning path for *routing congestion estimation and placement feedback* on tiny GCell grids.

Readers follow module READMEs. Authors rebuild clips with module-slides. This tree may be consumed from the parent monorepo or as a submodule later.

## Table of contents

- [Contents](#contents)
- [Browse or clone](#browse-or-clone)
- [Consume from the parent](#consume-from-the-parent)
- [Author: publish or update](#author-publish-or-update)
- [Two learning tracks](#two-learning-tracks)
- [Module landings](#module-landings)
- [Browser labs](#browser-labs)
- [License](#license)

## Contents

```
{COURSE_ID}/
├── README.md
├── LICENSE
├── common/         # Track A: tiny_cong.json, solvers, tests
├── docs/           # MODULES, SCOPE, TWO_TRACKS, WALKTHROUGHS
├── scripts/        # scaffold_course.py, build_all_media.sh, …
└── moduleSS-AA-slug/
    ├── README.md · CHECKLIST.md · EXAMPLES.md
    ├── transcript.md · outline.yaml · quiz.json
    └── (optional) examples/ · assets/ · slides · audio · video
```

Optional per-module media (pptx/pdf/audio/video) is produced by [module-slides](../../.cursor/skills/module-slides/SKILL.md).

## Browse or clone

From the monorepo root:

```bash
cd courses/{COURSE_ID}
```

## Consume from the parent

Prereq: [learn_placement](../learn_placement/README.md) / [learn_legalization](../learn_legalization/README.md).  
Next: [learn_global_routing](../learn_global_routing/README.md) or [learn_clock_tree](../learn_clock_tree/README.md).  
Lane map: [`eda.md`](../../eda.md). Scope: [docs/SCOPE.md](docs/SCOPE.md).

## Author: publish or update

```bash
# WSL / Linux — from monorepo root
python3 courses/{COURSE_ID}/scripts/scaffold_course.py   # regenerate stubs carefully
bash courses/{COURSE_ID}/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py {COURSE_ID}
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \\
  courses/{COURSE_ID} --modules
```

## Two learning tracks

| Track | Where | Doc |
|-------|-------|-----|
| **A — Implement** | `common/` + `examples/` | [TWO_TRACKS.md](docs/TWO_TRACKS.md) |
| **B — Browser lab** | platform tools | [TWO_TRACKS.md](docs/TWO_TRACKS.md) |

## Module landings

Full table: [docs/MODULES.md](docs/MODULES.md).

| Key | Module | Kind |
|-----|--------|------|
{landings}

## Browser labs

By workflow (Track B): {lab_links}. See [all tools]({LIVE_TOOLS}/) and each module README. Walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see [`LICENSE`](LICENSE).
""",
    )


def write_license() -> None:
    write(
        ROOT / "LICENSE",
        """Creative Commons Attribution 4.0 International (CC BY 4.0)

Copyright (c) contributors to learn_congestion / the learning monorepo.

You are free to share and adapt this material for any purpose, even commercially,
provided you give appropriate credit, provide a link to the license, and indicate
if changes were made. See https://creativecommons.org/licenses/by/4.0/ for the
full legal code.

SPDX-License-Identifier: CC-BY-4.0
""",
    )


def write_scripts() -> None:
    write(
        ROOT / "scripts" / "module.sh",
        r"""#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
KEY="${1:-}"
shift || true
if [[ -z "$KEY" || "$KEY" == "--help" ]]; then
  echo "Usage: $0 SS-AA [--check|--demo|--help]"
  exit 0
fi
MOD_DIR="$(find "$ROOT" -maxdepth 1 -type d -name "module${KEY}-*" | head -1)"
if [[ -z "$MOD_DIR" ]]; then
  echo "No module directory for module${KEY}-*"
  exit 1
fi
ACTION="${1:---check}"
case "$ACTION" in
  --check)
    echo "Module $KEY self-check (Track A)"
    [[ -f "$MOD_DIR/EXAMPLES.md" ]] && echo "[OK] EXAMPLES.md"
    [[ -f "$ROOT/common/tiny_cong.json" ]] && echo "[OK] common/tiny_cong.json"
    python3 -c "import sys; sys.path.insert(0,'$ROOT'); from common.solvers import rudy_demand; from common.congestionutil import load; print('[OK] solvers', rudy_demand(load('$ROOT/common/tiny_cong.json')['placement'], load('$ROOT/common/tiny_cong.json')) is not None)"
    ;;
  --demo)
    echo "Demo: open $MOD_DIR/EXAMPLES.md"
    ;;
  *)
    echo "Unknown option: $ACTION"; exit 1
    ;;
esac
""",
    )
    all_mods = "\n  ".join(m["id"] for m in MODULES)
    write(
        ROOT / "scripts" / "build_all_media.sh",
        f"""#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
COURSE_DIR="$(cd "${{SCRIPT_DIR}}/.." && pwd)"
ROOT="$(cd "${{COURSE_DIR}}/../.." && pwd)"
SKILL="${{ROOT}}/.cursor/skills/module-slides/scripts"
source "${{SKILL}}/_require_unix.sh"
cd "$ROOT"
bash "${{SKILL}}/narrate_clips.sh" --course-dir "$COURSE_DIR"
python3 "${{ROOT}}/platform/scripts/publish_course_platform.py" {COURSE_ID}
echo Done: "$COURSE_DIR"
""",
    )
    lab_mods = " \\\n  ".join(m["id"] for m in MODULES if m["kind"] == "lab")
    write(
        ROOT / "scripts" / "capture_all_walkthroughs.sh",
        f"""#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning
for m in \\
  {lab_mods}
do
  echo "=== $m ==="
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \\
    "courses/{COURSE_ID}/$m" --inject-transcript
done
echo CAPTURE_OK
""",
    )


def write_common() -> None:
    write(ROOT / "common" / "tiny_cong.json", tiny_cong_json())
    write(
        ROOT / "common" / "README.md",
        f"""# common — {COURSE_ID}

## Starter instance

[`tiny_cong.json`](tiny_cong.json) — chip 12×8, GCells 4×2 (cell 3×4), capacity 2.0.
Cells A–F; nets match placement. `placement` is spread; `congested_seed` clusters in the center.

## Modules

- `congestionutil.py` — load, GCell index, bbox, HPWL
- `solvers.py` — RUDY, probabilistic, congestion map, overflow, inflate, weights, feedback
- `test_solvers.py` — smoke goldens

Browser algorithms: `platform/tools/<lab-id>/` + `platform/assets/congestion-core.js`.
""",
    )
    write(
        ROOT / "common" / "congestionutil.py",
        '''"""Helpers for learn_congestion Track A."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

Pos = Dict[str, Dict[str, float]]


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def gcell_geom(data: Mapping[str, Any]) -> Tuple[int, int, float, float, float]:
    g = data["gcell"]
    return int(g["nx"]), int(g["ny"]), float(g["cellW"]), float(g["cellH"]), float(data["capacity"])


def cell_gcell(x: float, y: float, nx: int, ny: int, cell_w: float, cell_h: float) -> Tuple[int, int]:
    i = int(x // cell_w)
    j = int(y // cell_h)
    return max(0, min(nx - 1, i)), max(0, min(ny - 1, j))


def net_bbox(net: Sequence[str], positions: Mapping[str, Mapping[str, float]]) -> Tuple[float, float, float, float]:
    xs = [float(positions[c]["x"]) for c in net if c in positions]
    ys = [float(positions[c]["y"]) for c in net if c in positions]
    return min(xs), min(ys), max(xs), max(ys)


def hpwl(net: Sequence[str], positions: Mapping[str, Mapping[str, float]]) -> float:
    x0, y0, x1, y1 = net_bbox(net, positions)
    return (x1 - x0) + (y1 - y0)


def zeros(nx: int, ny: int) -> List[List[float]]:
    return [[0.0 for _ in range(ny)] for _ in range(nx)]


def clone_positions(pos: Mapping[str, Mapping[str, float]]) -> Pos:
    return {k: {"x": float(v["x"]), "y": float(v["y"])} for k, v in pos.items()}
''',
    )
    write(
        ROOT / "common" / "solvers.py",
        '''"""Congestion solvers (Track A) — mirror platform/assets/congestion-core.js."""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence, Tuple

from congestionutil import (
    cell_gcell,
    clone_positions,
    gcell_geom,
    hpwl,
    net_bbox,
    zeros,
)

Pos = Dict[str, Dict[str, float]]


def _tiles_for_bbox(
    x0: float, y0: float, x1: float, y1: float, nx: int, ny: int, cw: float, ch: float
) -> List[Tuple[int, int]]:
    i0, j0 = cell_gcell(x0, y0, nx, ny, cw, ch)
    i1, j1 = cell_gcell(x1, y1, nx, ny, cw, ch)
    if i0 > i1:
        i0, i1 = i1, i0
    if j0 > j1:
        j0, j1 = j1, j0
    return [(i, j) for i in range(i0, i1 + 1) for j in range(j0, j1 + 1)]


def rudy_demand(positions: Mapping[str, Mapping[str, float]], data: Mapping[str, Any]) -> List[List[float]]:
    nx, ny, cw, ch, _ = gcell_geom(data)
    demand = zeros(nx, ny)
    for net in data["nets"]:
        x0, y0, x1, y1 = net_bbox(net, positions)
        wl = hpwl(net, positions)
        tiles = _tiles_for_bbox(x0, y0, x1, y1, nx, ny, cw, ch)
        dens = wl / max(1, len(tiles))
        for i, j in tiles:
            demand[i][j] += dens
    return demand


def _deposit_line(
    demand: List[List[float]],
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    amt: float,
    nx: int,
    ny: int,
    cw: float,
    ch: float,
) -> None:
    tiles = _tiles_for_bbox(x0, y0, x1, y1, nx, ny, cw, ch)
    share = amt / max(1, len(tiles))
    for i, j in tiles:
        demand[i][j] += share


def probabilistic_demand(
    positions: Mapping[str, Mapping[str, float]], data: Mapping[str, Any]
) -> List[List[float]]:
    nx, ny, cw, ch, _ = gcell_geom(data)
    demand = zeros(nx, ny)

    def two_pin(a: str, b: str, scale: float = 1.0) -> None:
        ax, ay = float(positions[a]["x"]), float(positions[a]["y"])
        bx, by = float(positions[b]["x"]), float(positions[b]["y"])
        # H then V
        _deposit_line(demand, ax, ay, bx, ay, 0.5 * scale, nx, ny, cw, ch)
        _deposit_line(demand, bx, ay, bx, by, 0.5 * scale, nx, ny, cw, ch)
        # V then H
        _deposit_line(demand, ax, ay, ax, by, 0.5 * scale, nx, ny, cw, ch)
        _deposit_line(demand, ax, by, bx, by, 0.5 * scale, nx, ny, cw, ch)

    for net in data["nets"]:
        if len(net) == 2:
            two_pin(net[0], net[1])
        else:
            x0, y0, x1, y1 = net_bbox(net, positions)
            cx, cy = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
            # synthetic center pin
            positions_ext = dict(positions)
            positions_ext["__c"] = {"x": cx, "y": cy}
            for p in net:
                two_pin("__c", p, scale=1.0 / max(1, len(net)))
    return demand


def congestion_map(demand: Sequence[Sequence[float]], capacity: float) -> List[List[float]]:
    return [[float(d) / capacity for d in col] for col in demand]


def overflow_metrics(demand: Sequence[Sequence[float]], capacity: float) -> dict:
    ov = [[max(0.0, float(d) - capacity) for d in col] for col in demand]
    flat = [v for col in ov for v in col]
    return {
        "total": sum(flat),
        "max": max(flat) if flat else 0.0,
        "count": sum(1 for v in flat if v > 0),
        "perCell": ov,
    }


def hottest(cong: Sequence[Sequence[float]]) -> Tuple[int, int, float]:
    best = (0, 0, -1.0)
    for i, col in enumerate(cong):
        for j, v in enumerate(col):
            if v > best[2]:
                best = (i, j, float(v))
    return best


def inflate_widths(
    positions: Mapping[str, Mapping[str, float]],
    widths: Mapping[str, float],
    cong: Sequence[Sequence[float]],
    data: Mapping[str, Any],
    alpha: float = 0.5,
) -> Dict[str, float]:
    nx, ny, cw, ch, _ = gcell_geom(data)
    out = {k: float(v) for k, v in widths.items()}
    for cid, p in positions.items():
        i, j = cell_gcell(float(p["x"]), float(p["y"]), nx, ny, cw, ch)
        c = float(cong[i][j])
        if c > 1.0:
            out[cid] = float(widths.get(cid, 1.0)) * (1.0 + alpha * (c - 1.0))
    return out


def net_weights_from_congestion(
    positions: Mapping[str, Mapping[str, float]],
    cong: Sequence[Sequence[float]],
    data: Mapping[str, Any],
    beta: float = 1.0,
) -> List[float]:
    nx, ny, cw, ch, _ = gcell_geom(data)
    weights: List[float] = []
    for net in data["nets"]:
        x0, y0, x1, y1 = net_bbox(net, positions)
        tiles = _tiles_for_bbox(x0, y0, x1, y1, nx, ny, cw, ch)
        mean = sum(float(cong[i][j]) for i, j in tiles) / max(1, len(tiles))
        weights.append(1.0 + beta * mean)
    return weights


def placement_feedback_lite(
    positions: Mapping[str, Mapping[str, float]], data: Mapping[str, Any], alpha: float = 0.5
) -> Pos:
    nx, ny, cw, ch, cap = gcell_geom(data)
    demand = rudy_demand(positions, data)
    cong = congestion_map(demand, cap)
    ov = overflow_metrics(demand, cap)["perCell"]
    out = clone_positions(positions)
    chip_w = float(data["chip"]["W"])
    chip_h = float(data["chip"]["H"])
    for cid, p in list(out.items()):
        i, j = cell_gcell(p["x"], p["y"], nx, ny, cw, ch)
        if ov[i][j] <= 0:
            continue
        best = (i, j, ov[i][j])
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < nx and 0 <= nj < ny and ov[ni][nj] < best[2]:
                best = (ni, nj, ov[ni][nj])
        ti, tj = best[0], best[1]
        tx = (ti + 0.5) * cw
        ty = (tj + 0.5) * ch
        out[cid] = {
            "x": max(0.0, min(chip_w - 1.0, 0.5 * (p["x"] + tx))),
            "y": max(0.0, min(chip_h - 1.0, 0.5 * (p["y"] + ty))),
        }
    return out
''',
    )
    write(
        ROOT / "common" / "__init__.py",
        '"""learn_congestion Track A package."""\n',
    )
    write(
        ROOT / "common" / "test_solvers.py",
        '''#!/usr/bin/env python3
"""Smoke tests for congestion solvers."""
from __future__ import annotations

import unittest
from pathlib import Path

from congestionutil import cell_gcell, gcell_geom, load
from solvers import (
    congestion_map,
    overflow_metrics,
    placement_feedback_lite,
    probabilistic_demand,
    rudy_demand,
)

ROOT = Path(__file__).resolve().parent
DATA = load(ROOT / "tiny_cong.json")


class TestCongestion(unittest.TestCase):
    def test_gcell_index(self):
        nx, ny, cw, ch, _ = gcell_geom(DATA)
        self.assertEqual(cell_gcell(1, 1, nx, ny, cw, ch), (0, 0))
        self.assertEqual(cell_gcell(8, 5, nx, ny, cw, ch), (2, 1))

    def test_congested_overflow_higher(self):
        _, _, _, _, cap = gcell_geom(DATA)
        a = overflow_metrics(rudy_demand(DATA["placement"], DATA), cap)["total"]
        b = overflow_metrics(rudy_demand(DATA["congested_seed"], DATA), cap)["total"]
        self.assertGreater(b, a)

    def test_feedback_reduces(self):
        _, _, _, _, cap = gcell_geom(DATA)
        seed = DATA["congested_seed"]
        before = overflow_metrics(rudy_demand(seed, DATA), cap)["total"]
        after_pos = placement_feedback_lite(seed, DATA)
        after = overflow_metrics(rudy_demand(after_pos, DATA), cap)["total"]
        self.assertLess(after, before)

    def test_prob_runs(self):
        d = probabilistic_demand(DATA["placement"], DATA)
        self.assertEqual(len(d), 4)
        self.assertEqual(len(d[0]), 2)
        self.assertGreater(sum(sum(col) for col in d), 0)

    def test_cong_ratio(self):
        demand = rudy_demand(DATA["placement"], DATA)
        cong = congestion_map(demand, 2.0)
        self.assertAlmostEqual(cong[0][0], demand[0][0] / 2.0)


if __name__ == "__main__":
    unittest.main()
''',
    )


def main() -> None:
    write_license()
    write_docs()
    write_modules_md()
    write_course_readme()
    write_common()
    write_scripts()
    tiny = tiny_cong_json()
    for i, m in enumerate(MODULES):
        mid = m["id"]
        base = ROOT / mid
        write(base / "README.md", readme(m, i))
        write(base / "CHECKLIST.md", checklist(m))
        write(base / "EXAMPLES.md", examples(m))
        write(base / "outline.yaml", outline_stub(m))
        if m["kind"] == "intro":
            write(base / "transcript.md", transcript_intro())
        elif m["kind"] == "wrap":
            write(base / "transcript.md", transcript_wrap())
        elif m["kind"] == "offline":
            write(base / "transcript.md", transcript_offline())
        else:
            write(base / "transcript.md", transcript_lab(m))
        write(base / "quiz.json", json.dumps(quiz(m), indent=2) + "\n")
        if m["kind"] == "lab":
            write(base / "examples" / "tiny_cong.json", tiny)
    print(f"Scaffolded {COURSE_ID}: {len(MODULES)} modules → {ROOT}")


if __name__ == "__main__":
    main()
