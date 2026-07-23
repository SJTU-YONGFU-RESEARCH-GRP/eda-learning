#!/usr/bin/env python3
"""Scaffold learn_legalization modules (hierarchical SS-AA ids) with module-slides stubs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "learn_legalization"
LIVE_TOOLS = "https://universal-verification-methodology.github.io/learning/tools"

MODULES = [
    {
        "id": "module00-00-intro",
        "kind": "intro",
        "title": "Welcome to legalization for EDA",
        "short": "Welcome",
        "lab": None,
        "status": "—",
        "section": "00",
        "outcomes": "Explain why legalization follows global placement, and how site/row snapping fits the PD stack.",
        "algorithm": None,
    },
    {
        "id": "module01-01-site-row-model",
        "kind": "lab",
        "title": "Site and row model",
        "short": "Site / row",
        "lab": "site-row-model",
        "status": "**ref**",
        "section": "01",
        "outcomes": "State chip sites, row height, row bottoms, and map cell widths to site columns.",
        "algorithm": "site and row geometry model (sites, rowH, cell width in sites)",
    },
    {
        "id": "module01-03-legality-metrics",
        "kind": "lab",
        "title": "Legality metrics",
        "short": "Legality",
        "lab": "legality-metrics",
        "status": "**ref**",
        "section": "01",
        "outcomes": "Check row alignment, site snapping, pairwise non-overlap, and report a legality verdict.",
        "algorithm": "legality checker (row, site, overlap)",
    },
    {
        "id": "module02-01-greedy-snap",
        "kind": "lab",
        "title": "Greedy site/row snap",
        "short": "Greedy snap",
        "lab": "greedy-snap",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Snap floating global-place coordinates to the nearest legal site and row bottom.",
        "algorithm": "greedy site/row snap from float coordinates",
    },
    {
        "id": "module02-03-overlap-removal",
        "kind": "lab",
        "title": "Overlap removal in rows",
        "short": "Overlap removal",
        "lab": "overlap-removal",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Resolve same-row overlaps by shifting cells along the row until no interior overlap.",
        "algorithm": "in-row overlap removal by shifting",
    },
    {
        "id": "module02-05-abacus-row-pack",
        "kind": "lab",
        "title": "Abacus row packing",
        "short": "Abacus",
        "lab": "abacus-row-pack",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Pack cells in a row with Abacus-style cluster compaction toward the row origin.",
        "algorithm": "Abacus row packing (cluster collapse)",
    },
    {
        "id": "module02-07-tetris-row-pack",
        "kind": "lab",
        "title": "Tetris-style row packing",
        "short": "Tetris pack",
        "lab": "tetris-row-pack",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Fill row slots with Tetris-style placement order while respecting widths and legality.",
        "algorithm": "Tetris-style row slot packing",
    },
    {
        "id": "module03-01-fixed-macros",
        "kind": "lab",
        "title": "Fixed macros during legalization",
        "short": "Fixed macros",
        "lab": "fixed-macros",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Legalize movable standard cells around fixed macro obstacles locked at (x, y).",
        "algorithm": "legalization with fixed macro obstacles",
    },
    {
        "id": "module03-03-displacement-hpwl",
        "kind": "lab",
        "title": "Displacement vs HPWL tradeoff",
        "short": "Displacement / HPWL",
        "lab": "displacement-hpwl",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Report total displacement from global place and compare HPWL before vs after legalize.",
        "algorithm": "displacement sum vs HPWL tradeoff metrics",
    },
    {
        "id": "module04-01-detailed-vs-global",
        "kind": "lab",
        "title": "Detailed vs global legalize",
        "short": "Detailed vs global",
        "lab": "detailed-vs-global",
        "status": "**ref**",
        "section": "04",
        "outcomes": "Contrast a fast global snap/pack pass with a detailed multi-row legalization flow.",
        "algorithm": "global vs detailed legalization pipeline contrast",
    },
    {
        "id": "module05-01-offline-benchmark-compare",
        "kind": "offline",
        "title": "Offline benchmark compare",
        "short": "Offline compare",
        "lab": None,
        "status": "P",
        "section": "05",
        "outcomes": "Compare toy legalizers on shared instances (legality, displacement, HPWL, runtime).",
        "algorithm": "benchmark harness vs reference legalizations",
    },
    {
        "id": "module99-00-wrap",
        "kind": "wrap",
        "title": "Legalization path complete",
        "short": "Wrap",
        "lab": None,
        "status": "—",
        "section": "99",
        "outcomes": "Recap site/row snap, row packing, macros, and displacement; choose routing or congestion next.",
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


def tiny_legal_json() -> str:
    data = {
        "chip": {"W": 12, "H": 6, "siteW": 1, "rowH": 2, "rows": [0, 2, 4]},
        "cells": [
            {"id": "A", "width": 2},
            {"id": "B", "width": 2},
            {"id": "C", "width": 2},
            {"id": "D", "width": 2},
            {"id": "E", "width": 1},
            {"id": "F", "width": 1},
        ],
        "nets": [
            ["A", "B"],
            ["C", "D"],
            ["A", "C"],
            ["B", "D"],
            ["A", "B", "C", "D"],
            ["E", "F"],
        ],
        "fixed_macros": [{"id": "D", "x": 8, "y": 4, "width": 2, "fixed": True}],
        "starter_illegal": {
            "A": {"x": 4, "y": 2},
            "B": {"x": 4, "y": 2},
            "C": {"x": 4, "y": 2},
            "D": {"x": 8, "y": 4},
            "E": {"x": 0, "y": 4},
            "F": {"x": 10, "y": 0},
        },
        "starter_float": {
            "A": {"x": 3.7, "y": 1.2},
            "B": {"x": 4.1, "y": 1.4},
            "C": {"x": 5.2, "y": 2.3},
            "D": {"x": 8.4, "y": 3.8},
            "E": {"x": 0.3, "y": 4.6},
            "F": {"x": 10.2, "y": 0.4},
        },
        "notes": "W=12 sites, H=6 (3 rows), siteW=1, rowH=2, row bottoms y=0,2,4. "
        "starter_illegal: A,B,C overlap on middle row; D fixed macro at (8,4). "
        "starter_float: global-place floats for greedy snap.",
    }
    return json.dumps(data, indent=2) + "\n"


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

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **{m['algorithm']}** on `examples/tiny_legal.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, displacement, and HPWL when relevant.
3. Optional self-check: `./scripts/module.sh {key} --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/{lab}/](http://127.0.0.1:8080/tools/{lab}/)
2. Live: [{LIVE_TOOLS}/{lab}/]({LIVE_TOOLS}/{lab}/)
3. Tools shelf: open `{lab}` from the platform tools index
4. Load the **starter legalization**, run the algorithm, inspect legality and metrics.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach legalization literacy on tiny site/row grids — not production OpenROAD legalizers.
"""
    elif m["kind"] == "offline":
        body = f"""
## Outcomes

After this module you can: **{m['outcomes']}**

## Offline track

1. Follow [EXAMPLES.md](EXAMPLES.md) to run the local compare harness.
2. Record legality, displacement, HPWL, and runtime against at least one reference when available.
3. Complete [CHECKLIST.md](CHECKLIST.md).
"""
    elif m["kind"] == "intro":
        body = """
## What this course is

**learn_legalization** teaches *site/row snapping and overlap removal after global placement* using **two learning modes** on every lab module:

| Track | Where you practice | Best for |
|-------|--------------------|----------|
| **A — Implement** | Tiny legal instance + `EXAMPLES.md` / `examples/` | Fidelity: sites, rows, legality, packing |
| **B — Browser lab** | Interactive lab on the learning platform | Concept literacy, quick visual feedback |

You can do **A only**, **B only**, or **both** (recommended: B for intuition when shipped, then A for fidelity).

**Prerequisite:** [learn_placement](../learn_placement/README.md) — global placement produces the float coordinates you snap here.

## Setup (Track A)

1. Open this course under `courses/learn_legalization/`.
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

- Model sites and rows on a tiny chip grid
- Check legalization legality (row, site, non-overlap)
- Snap floats, remove overlaps, and pack rows with Abacus and Tetris-style flows
- Legalize around fixed macros and report displacement vs HPWL
- Contrast global vs detailed legalization passes

## Dual-track recap

If you mainly used **browser labs**, spend a short session on Track A for site/row model and one row-packing algorithm.
If you mainly used **Track A**, skim any skipped shipped browser labs for visual row packing.

## Next course

Prereqs done: **learn_placement** (global place → legalization).

→ **learn_routing** or congestion-aware flows (see parent [`eda.md`](../../../eda.md))

## Checklist

- [ ] I completed Track A and/or Track B for the lab modules I care about
- [ ] I can explain snap vs pack vs macro obstacles in my own words
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
- [ ] Implemented **{m['algorithm']}** end-to-end on `examples/tiny_legal.json`
- [ ] Reported legality (row, site, non-overlap) and displacement / HPWL when relevant
- [ ] Can explain the algorithm without the UI

## Track B — Browser lab (`{m['lab']}`)

- [ ] Opened the lab (local or live)
- [ ] Loaded the starter legalization instance
- [ ] Ran the algorithm and inspected legality metrics

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

- [ ] I can explain how to judge legalization quality across engines
"""
    if m["kind"] == "intro":
        return f"""# Checklist — {m['title']}

- [ ] I understand the course map (sections 01–05 + wrap)
- [ ] I know Track A (implement) vs Track B (browser lab)
- [ ] I opened [docs/MODULES.md](../docs/MODULES.md) once
- [ ] I finished learn_placement or know why legalization follows global place
- [ ] Ready for site and row model
"""
    return f"""# Checklist — {m['title']}

- [ ] I can name the main legalization ideas from sections 01–04
- [ ] I know when greedy snap vs Abacus vs Tetris fits
- [ ] I picked a next course (routing / congestion)
"""


def examples(m: dict) -> str:
    if m["kind"] == "lab":
        return f"""# Examples — {m['title']}

Track A (implement). Use the tiny legalization instance first (`examples/tiny_legal.json`).

## Algorithm

**{m['algorithm']}**

## Starter prompts

1. Restate the idea in five bullets (inputs → row/site model → algorithm loop → legality → metrics).
2. Load cells A–F on the 12-site × 6-height grid (3 rows, rowH=2, bottoms y=0,2,4).
3. Pick `starter_float` or `starter_illegal` depending on the lab; confirm cell widths in sites.
4. Produce legal site-aligned coordinates; report legality boolean and total displacement from float start.
5. Change one knob (macro lock, pack order, snap rounding) and report HPWL or displacement delta.

## Expected artifacts

- Legal (x, y) per cell on site grid
- Legality boolean + displacement / HPWL summary
- Short note: why this idea belongs on the legalization shelf

## Stretch

Lock macro D at (8,4) or add a second fixed block; keep the same metrics API.
"""
    if m["kind"] == "offline":
        return """# Examples — Offline benchmark compare

1. Export the same tiny_legal instance used in snap / pack labs.
2. Run your toy legalizer; record legality, displacement, HPWL, wall time.
3. If available, compare against a reference legalization (golden coordinates or another engine).
4. Fill a comparison table: quality, legality, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
"""
    if m["kind"] == "intro":
        return """# Examples — Welcome

No coding yet.

1. Sketch the PD path: partition → floorplan → global place → **legalize** → route.
2. Write one sentence: “Legalization snaps cells to sites/rows because …”
3. Name one difference between global placement coordinates and legal coordinates.
"""
    return """# Examples — Wrap

1. List three legalization algorithms from this course and one strength each.
2. For overlapping cells on one row, which module’s idea do you reach for first?
3. Write the bridge sentence you’ll need for detailed routing next.
"""


LAB_TRANSCRIPTS: dict[str, str] = {
    "site-row-model": """# Site and row model

**Module id:** module01-01-site-row-model
**Lab:** site-row-model
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Sites and rows

Global placement gives you smooth floating coordinates. Legalization lives on a discrete grid: sites along each row, fixed row height, and row bottoms at known y values. On our toy chip that is twelve sites wide, six units tall, three rows with height two, and row bottoms at zero, two, and four.

## Slide 2 — The idea

Each standard cell has a width measured in site columns—A through D are two sites wide; E and F are one. A legal x coordinate aligns to site boundaries: zero, one, two, and so on. Row y is the bottom of the cell and must match a row bottom. Site width and row height are constants in the JSON—treat them as the floorplan contract from the library.

## Slide 3 — Browser lab track

Open the **site-row-model** lab from the tools shelf. Highlight the grid: sites as vertical ticks, rows as horizontal bands. Place a cell and read which row bottom and left site it claims. Drag across a row boundary and watch the model reject or snap the position. Then encode the same grid in Track A.

## Slide 4 — Implement track

Parse `tiny_legal.json`. Print row bottoms, site count, and each cell width in sites. Given a candidate (x, y), classify whether x is site-aligned and y matches a row bottom. Keep integers on the toy grid so goldens stay stable. This module is geometry literacy—no packing yet.

## Slide 5 — Pitfalls

Mixing cell height with row height when only width varies on the toy instance. Forgetting that x is left edge in sites, not center. Using float y from global place without mapping to the nearest row bottom—that is the next module’s job, not this one.

## Slide 6 — Your turn

Complete the checklist for at least one track. Be able to draw the three rows and site columns from memory. Next: legality metrics—the checker every snap and pack pass must call.
""",
    "legality-metrics": """# Legality metrics

**Module id:** module01-03-legality-metrics
**Lab:** legality-metrics
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — What “legal” means

Legalization is not “looks fine in the GUI.” A placement is legal when cells sit on valid sites and rows, stay inside the chip, and do not overlap in area. This lab builds the checker you will reuse after greedy snap, overlap removal, Abacus, and Tetris packing.

## Slide 2 — The idea

Check three things. Row: every cell bottom y equals a row bottom and height fits rowH. Site: every left x is an integer site index and width in sites fits within W. Overlap: for cells on the same row, intervals [x, x+width) do not intersect unless sharing a boundary is allowed—pick a rule and document it. Return the first violation for debugging.

## Slide 3 — Browser lab track

Open **legality-metrics**. Load the starter with A, B, and C stacked at the same middle-row coordinate—classic illegal overlap. Read the legality flag and violation message. Fix one cell and watch the checker pass. Mirror the same rules in Python.

## Slide 4 — Implement track

Load `starter_illegal` from `tiny_legal.json`. Implement `is_legal(positions)` returning pass/fail plus reason. Test the known overlap on row y=2. Add a helper for in-chip containment: x+width ≤ W and y+rowH ≤ H. Print a one-line summary your later solvers will call after every move.

## Slide 5 — Pitfalls

Checking overlap only among neighbors instead of all pairs on a row. Treating touching edges as overlap when your spec allows abutment. Reporting legal=True because rows look aligned while x floats remain fractional—snap first or reject floats explicitly.

## Slide 6 — Your turn

Finish the checklist. Your checker should fail the starter_illegal layout and pass any manually separated legal packing. Next: greedy snap turns global-place floats into row/site candidates.
""",
    "greedy-snap": """# Greedy site/row snap

**Module id:** module02-01-greedy-snap
**Lab:** greedy-snap
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — From float to grid

Global placement optimizes wirelength on continuous coordinates. Legalization’s first move is often the simplest: snap each cell to the nearest site column and row bottom. Greedy snap is fast, local, and a baseline every fancier legalizer compares against.

## Slide 2 — The idea

For each cell, round or floor x to the nearest legal site index respecting width so x+width ≤ W. Map y to the nearest row bottom—usually minimize |y − rowBottom|. Process cells in a fixed order on the toy instance. Overlap may remain; snap does not pack. Measure displacement as Manhattan or Euclidean sum from float start.

## Slide 3 — Browser lab track

Open **greedy-snap**. Load `starter_float` coordinates. Run snap and watch cells jump to row bands. Note overlaps that appear after snap—that is expected. Compare displacement totals before calling overlap removal. Then implement the same rounding policy in Track A.

## Slide 4 — Implement track

Implement `greedy_snap(starter_float)` returning integer site-aligned positions. Use chip rows [0,2,4] and siteW=1. Log per-cell displacement. Call your legality checker—expect overlap failures until a later lab. Keep deterministic tie-breaking for goldens.

## Slide 5 — Pitfalls

Snapping x without ensuring x+width fits in W. Snapping macros that should stay fixed—skip fixed cells. Using round() inconsistently on negative or boundary floats. Declaring success because coordinates are integer—legality still requires non-overlap.

## Slide 6 — Your turn

Snap all six cells from starter_float. Report total displacement and legality. Next: overlap removal clears same-row collisions without leaving the grid.
""",
    "overlap-removal": """# Overlap removal in rows

**Module id:** module02-03-overlap-removal
**Lab:** overlap-removal
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Overlaps after snap

Greedy snap lands multiple cells on the same row with colliding site intervals—our starter_illegal has A, B, and C all starting at x=4 on the middle row. Overlap removal walks each row left-to-right and pushes cells until intervals are disjoint. It is the duct tape between snap and true row packing.

## Slide 2 — The idea

Sort cells on a row by left x. Scan in order; if the next cell starts before the previous ends, shift it right to abut the predecessor. Repeat until no overlap or you hit the chip right edge—then flag failure. Preserve row y and widths. Optional: left-compact afterward to reduce displacement.

## Slide 3 — Browser lab track

Open **overlap-removal**. Start from the illegal triple overlap. Step the shift rule and watch intervals separate. Try a row that overflows W—read the failure mode. Implement the same sweep in Track A and compare displacement to Abacus later.

## Slide 4 — Implement track

Implement `overlap_remove(positions)` on starter_illegal or post-snap layouts. Return legal positions or explicit overflow error. Pair with legality checker asserts. Document order dependence—fixed cell order vs sorted by x.

## Slide 5 — Pitfalls

Only fixing pairwise first overlap while a later cell still collides. Ignoring fixed macros when shifting movables. Shifting y instead of x and breaking row alignment. Silent wrap to the next row—reject that unless your spec allows row changes.

## Slide 6 — Your turn

Clear overlaps on the middle row for A, B, C. Report legality and displacement from starter_illegal. Next: Abacus row packing—a structured pack instead of ad hoc shifts.
""",
    "abacus-row-pack": """# Abacus row packing

**Module id:** module02-05-abacus-row-pack
**Lab:** abacus-row-pack
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Abacus packing

Abacus is a classic row legalization approach: cells in a row form clusters that collapse toward the origin like beads on a wire. It respects cell widths, compacts left, and handles obstacles. On our toy grid you will pack one row at a time with a simplified Abacus-lite loop.

## Slide 2 — The idea

Process cells in order (often by global x). Maintain clusters as contiguous blocks. When placing the next cell, merge with the previous cluster if they would overlap, then collapse the cluster left to x=0 or the nearest obstacle. Fixed macros act as immovable pillars—pack movables around them.

## Slide 3 — Browser lab track

Open **abacus-row-pack**. Load a row with mixed widths and a fixed D at x=8. Step clusters merging and collapsing. Watch movables slide left until they hit D or the row origin. Compare final displacement to overlap removal alone.

## Slide 4 — Implement track

Implement `abacus_lite(positions, row_y)` matching the JS API name you will see in platform tools. Run on middle and bottom rows separately. Assert legality after each row. Export coordinates for golden tests when platform goldens land.

## Slide 5 — Pitfalls

Forgetting macro D at (8,4) when packing the top row. Merging clusters without updating rightmost extent. Packing rows in random order and breaking cross-row assumptions on the toy instance. Calling it Abacus but only doing greedy snap—clusters must collapse.

## Slide 6 — Your turn

Pack all movable cells row-by-row with Abacus-lite. Report legality and displacement. Next: Tetris-style packing fills slots in a different order—compare trade-offs.
""",
    "tetris-row-pack": """# Tetris-style row packing

**Module id:** module02-07-tetris-row-pack
**Lab:** tetris-row-pack
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Tetris rows

Another row legalization mental model is Tetris: walk cells in some order and drop each into the leftmost slot that fits on its row, like falling blocks locking into gaps. It is greedy, order-dependent, and surprisingly instructive for why industrial legalizers optimize order and displacement together.

## Slide 2 — The idea

For each cell, find the minimum x on its assigned row such that [x, x+width) is free of occupied sites. Occupancy is a boolean array over sites. Fixed macros pre-occupy sites. Order matters: sort by global x, by width descending, or by net criticality on advanced instances—start with global x on the toy grid.

## Slide 3 — Browser lab track

Open **tetris-row-pack**. Try two cell orders on the same starter—watch different legal packings and displacement. Visualize site occupancy per row. Then code the occupancy bitmap in Track A.

## Slide 4 — Implement track

Implement `tetris_lite(positions)` with a clear order policy documented in comments. Use starter_float row assignment (map y to nearest row first). Compare HPWL after pack vs Abacus-lite on the same order seed.

## Slide 5 — Pitfalls

Allowing cells to float between rows mid-pack. Not marking multi-site widths as occupied through x+width−1. Skipping fixed macro sites. Assuming Tetris always beats Abacus—report metrics, not folklore.

## Slide 6 — Your turn

Produce a legal Tetris packing for all rows. Note order sensitivity in your checklist notes. Next: fixed macros as first-class obstacles across the whole chip.
""",
    "fixed-macros": """# Fixed macros during legalization

**Module id:** module03-01-fixed-macros
**Lab:** fixed-macros
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Macros do not move

Memories and analog IP arrive as fixed rectangles—size locked, sometimes position locked too. On tiny_legal, macro D is fixed at x=8, y=4 with width two. Movable standard cells must legalize around D without shifting it. Treat fixed blocks as pre-placed obstacles in every row pass.

## Slide 2 — The idea

Tag cells with `fixed: true` and optional locked (x, y). Skip them in snap shifts and mark their site intervals occupied before packing movables. Legality checks still apply—movables must not overlap D. Displacement for fixed cells is zero by definition.

## Slide 3 — Browser lab track

Open **fixed-macros**. Lock D and run snap plus pack on A, B, C, E, F. Attempt to drag D—UI should refuse. Overflow near the right edge shows why macro placement upstream matters.

## Slide 4 — Implement track

Extend your legalizer to read `fixed_macros` from JSON. Ensure overlap removal and Abacus/Tetris respect occupied sites from D. Add a test that movables never change D’s coordinates.

## Slide 5 — Pitfalls

Including D in displacement sums. Collapsing clusters through a macro. Letting Tetris place a movable into D’s sites because occupancy was not seeded. Unfixing D during detailed pass without updating the JSON contract.

## Slide 6 — Your turn

Legalize all movables with D fixed. Verify legality and zero displacement on D. Next: quantify how much the legalizer moved cells versus wirelength cost.
""",
    "displacement-hpwl": """# Displacement vs HPWL tradeoff

**Module id:** module03-03-displacement-hpwl
**Lab:** displacement-hpwl
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Two costs after legalize

Legalization fixes geometry but moves cells from global-place targets. Displacement measures that movement—usually sum of Manhattan distances from float or pre-legal positions. HPWL measures connectivity stretch on the legalized sites. Good legalizers minimize both under legality constraints.

## Slide 2 — The idea

Compute total displacement vs starter_float and HPWL on nets from tiny_legal (same netlist as learn_placement). Compare before and after legalize. A aggressive pack may crush HPWL but spike displacement; a conservative snap may do the opposite. Report both numbers side by side.

## Slide 3 — Browser lab track

Open **displacement-hpwl**. Run two legalization presets if the UI offers them—note displacement and HPWL deltas. Tie-break mentally: which trade-off would you accept for routing?

## Slide 4 — Implement track

Add helpers `total_displacement(before, after)` and reuse HPWL from placementutil patterns. Run metrics on greedy+overlap vs Abacus vs Tetris packings you built. Tabulate results in EXAMPLES.md notes.

## Slide 5 — Pitfalls

Measuring displacement from already-integer illegal starts. Ignoring fixed cells in displacement sum. Comparing HPWL on illegal layouts. Using Euclidean distance on a site grid without documenting it.

## Slide 6 — Your turn

Fill a small table: method, legal?, displacement, HPWL. Next: contrast global one-pass legalize vs detailed multi-stage flows.
""",
    "detailed-vs-global": """# Detailed vs global legalize

**Module id:** module04-01-detailed-vs-global
**Lab:** detailed-vs-global
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — One pass vs pipeline

Industrial flows sometimes legalize in one global pass; detailed placement runs multiple row-aware stages afterward. This lab names the difference on our toy grid: global snap+pack everywhere at once versus row-by-row detailed refinement with macro awareness.

## Slide 2 — The idea

Global lite: snap all cells, then pack each row independently. Detailed lite: iterate rows bottom-up, re-run overlap removal and Abacus on each row while freezing prior rows, optionally swap adjacent cells to reduce HPWL. Same legality checker gates both. Compare displacement, HPWL, and runtime.

## Slide 3 — Browser lab track

Open **detailed-vs-global**. Toggle between modes on the same starter. Watch whether middle-row ordering changes when bottom row is frozen first. Capture notes for Track A pipeline design.

## Slide 4 — Implement track

Wire a `global_legalize()` and `detailed_legalize()` using your existing solvers. Same I/O as platform tools will expect. Log stage timings—even milliseconds teach pipeline thinking.

## Slide 5 — Pitfalls

Calling it detailed but only running one Abacus pass. Breaking legality in row two while fixing row three. Mixing float coordinates mid-pipeline. Expecting detailed to always win on HPWL—report honestly on tiny_legal.

## Slide 6 — Your turn

Run both pipelines; document trade-offs in CHECKLIST notes. Next: offline benchmark compare, then course wrap.
""",
}


def transcript_lab(m: dict) -> str:
    lab = m["lab"]
    if lab in LAB_TRANSCRIPTS:
        return LAB_TRANSCRIPTS[lab]
    return f"# {m['title']}\n\n## Slide 1 — {m['title']}\n\nImplement **{m['algorithm']}**.\n"


def transcript_intro() -> str:
    return """# Welcome to legalization for EDA

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to legalization

Global placement spreads cells for wirelength and density—but coordinates float freely. Legalization snaps them to rows and sites, removes overlaps, and respects fixed macros before routing. This course teaches that transition on a tiny twelve-site grid so detailed routing has a legal canvas.

## Slide 2 — What you’ll build

You’ll model sites and rows, check legality, greedy-snap floats, remove overlaps, and pack rows with Abacus and Tetris-style algorithms. Then legalize around fixed macros, measure displacement versus HPWL, and contrast global versus detailed passes. One idea per lab—complete on scoped instances, not production OpenROAD.

## Slide 3 — Prerequisite path

Finish **learn_placement** first: you need global-place floats and HPWL intuition. Floorplanning and clustering further upstream set the outline; legalization assumes cells already have rough (x, y) targets.

## Slide 4 — Two tracks

Every lab offers Track A—implement on `tiny_legal.json`—and Track B—browser labs when shipped. Good rhythm: browser for row/site intuition, implement to harden checkers and packers.

## Slide 5 — How to move

Read each README, pick a track, work the checklist. Keep legality, displacement, and HPWL as habits. When intro checklist is done, continue to site and row model—the geometry contract for every later algorithm.
"""


def transcript_wrap() -> str:
    return """# Legalization path complete

**Module id:** module99-00-wrap
**Lab:** none (wrap)
**Tracks:** recap · next course

## Slide 1 — Legalization path complete

You’ve walked from site/row geometry through legality checks, greedy snap, overlap removal, Abacus and Tetris packing, fixed macros, displacement versus HPWL, and global vs detailed pipelines. This wrap names what you can do now and where to go next.

## Slide 2 — What you can do now

You can explain why legalization follows global placement. You can check row/site legality, snap floats, clear overlaps, and pack rows. You can respect fixed macros and report displacement alongside HPWL. You are building algorithm literacy—not shipping a foundry legalizer.

## Slide 3 — Close the gaps

If you mainly used browser labs, implement legality checking plus one row packer in Track A. If you mainly coded, skim browser labs for visual row intuition. Placement prereqs should feel connected: floats in, legal sites out.

## Slide 4 — Next courses

Natural next steps are detailed routing and congestion-aware flows. Keep your tiny_legal harness; routing courses consume legal coordinates. Open **`eda.md`** in the parent monorepo for the full PD spine.

## Slide 5 — Your turn

Review the wrap checklist. Name three packing strategies and when you’d pick each. When ready, take the short quiz, then continue along the PD path.
"""


def transcript_offline() -> str:
    return """# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none (offline)
**Tracks:** offline harness

## Slide 1 — Offline benchmark compare

Toy legalizers teach mechanism. Benchmarks teach honesty. Run the same tiny_legal instance through your code and, when available, a reference tool—then compare legality, displacement, HPWL, and runtime without pretending the numbers are sign-off quality.

## Slide 2 — Fair compare rules

Identical input JSON, same row/site rules, fixed seeds if randomized. Report the same metrics on both sides. Missing reference tools? Still run your harness and document the gap.

## Slide 3 — What good looks like

Educational engines may be slower—that is fine. Look for legal outputs, stable displacement totals, and plausible HPWL. Unexplained huge wins usually mean unequal metrics or skipped legality checks.

## Slide 4 — Your turn

Follow EXAMPLES.md, fill the comparison table, finish the checklist, then continue to the wrap module.
"""


def quiz(m: dict) -> dict:
    if m["kind"] == "intro":
        items = [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "This course focuses primarily on…",
                "choices": [
                    "Vendor P&R GUI click-paths",
                    "Site/row snapping and overlap removal after global placement",
                    "Foundry PDK certification",
                    "Writing UVM agents",
                ],
                "answer": 1,
                "explain": "Algorithm literacy on tiny legalization grids.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "Legalization typically follows global placement in the PD flow.",
                "answer": True,
                "explain": "Global place → legalize → route.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A good study rhythm is…",
                "choices": [
                    "Only memorize folder names",
                    "Browser intuition then implement on tiny_legal.json",
                    "Skip checklists entirely",
                    "Start with routing before legality",
                ],
                "answer": 1,
                "explain": "Track B then Track A hardens the idea.",
            },
        ]
        title = "Intro check"
    elif m["kind"] == "wrap":
        items = [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "Legalization primarily ensures…",
                "choices": [
                    "Only timing closure",
                    "Site/row alignment and non-overlap",
                    "Only power grid synthesis",
                    "Scan chain ordering",
                ],
                "answer": 1,
                "explain": "Geometry on rows/sites before routing.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "Greedy snap alone may leave overlaps; row packing or removal may be needed.",
                "answer": True,
                "explain": "Snap ≠ full legalize.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "Prerequisite for this course is…",
                "choices": [
                    "learn_placement",
                    "Analog layout only",
                    "Git internals",
                    "UART framing",
                ],
                "answer": 0,
                "explain": "Global place feeds legalization.",
            },
        ]
        title = "Wrap check"
    elif m["kind"] == "offline":
        items = [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Fair compares require the same tiny_legal input and comparable metrics.",
                "answer": True,
                "explain": "Otherwise you compare different problems.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "If a reference legalizer is missing you should…",
                "choices": [
                    "Invent golden HPWL",
                    "Still run your harness and document the gap",
                    "Skip legality checks",
                    "Delete displacement metrics",
                ],
                "answer": 1,
                "explain": "Honesty about tooling beats fake goldens.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "An educational legalizer that is slower than a commercial tool is automatically wrong.",
                "answer": False,
                "explain": "Speed differs; look for legal, consistent metrics.",
            },
        ]
        title = "Offline check"
    else:
        lab_quizzes = {
            "site-row-model": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": "On tiny_legal, row bottoms are at y = …",
                    "choices": ["0, 2, 4", "0, 1, 2", "Only 0", "8, 9, 10"],
                    "answer": 0,
                    "explain": "Three rows, rowH=2.",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "Cell width is measured in site columns on this grid.",
                    "answer": True,
                    "explain": "siteW=1; widths are integer sites.",
                },
                {
                    "id": "q3",
                    "type": "multiple_choice",
                    "prompt": "Chip width W in sites is…",
                    "choices": ["6", "12", "3", "24"],
                    "answer": 1,
                    "explain": "W=12 in tiny_legal.json.",
                },
                {
                    "id": "q4",
                    "type": "true_false",
                    "prompt": "Track A uses examples/tiny_legal.json.",
                    "answer": True,
                    "explain": "Shared Track A instance.",
                },
            ],
            "legality-metrics": [
                {
                    "id": "q1",
                    "type": "true_false",
                    "prompt": "starter_illegal has A, B, C overlapping on the middle row.",
                    "answer": True,
                    "explain": "All at x=4, y=2.",
                },
                {
                    "id": "q2",
                    "type": "multiple_choice",
                    "prompt": "Legality checking includes…",
                    "choices": [
                        "Only HPWL",
                        "Row/site alignment and non-overlap",
                        "Only Git status",
                        "Liberty arcs",
                    ],
                    "answer": 1,
                    "explain": "Geometry gates.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Touching cell edges may be allowed if interiors do not overlap—depends on spec.",
                    "answer": True,
                    "explain": "Document abutment policy.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "A legal x coordinate aligns to…",
                    "choices": [
                        "Fractional sites",
                        "Integer site indices (left edge)",
                        "Only row centers",
                        "Random floats",
                    ],
                    "answer": 1,
                    "explain": "Site grid alignment.",
                },
            ],
            "greedy-snap": [
                {
                    "id": "q1",
                    "type": "true_false",
                    "prompt": "Greedy snap maps global-place floats to nearest row/site coordinates.",
                    "answer": True,
                    "explain": "First legalization step.",
                },
                {
                    "id": "q2",
                    "type": "multiple_choice",
                    "prompt": "starter_float is intended for…",
                    "choices": [
                        "Snap labs",
                        "Only routing",
                        "PDK release",
                        "Scan chains",
                    ],
                    "answer": 0,
                    "explain": "Float coordinates from global place.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "After snap alone, overlaps may still exist.",
                    "answer": True,
                    "explain": "Snap does not pack.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "Displacement measures…",
                    "choices": [
                        "Movement from pre-legal to legal positions",
                        "Only temperature",
                        "Only row count",
                        "Pin count",
                    ],
                    "answer": 0,
                    "explain": "How far cells moved.",
                },
            ],
            "overlap-removal": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": "Overlap removal primarily shifts cells along…",
                    "choices": ["The same row (x)", "Random y jumps", "Only diagonals", "Netlist edges"],
                    "answer": 0,
                    "explain": "In-row interval fix.",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "Sorting cells by left x before shifting is a common policy.",
                    "answer": True,
                    "explain": "Deterministic sweep.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Overlap removal always minimizes HPWL.",
                    "answer": False,
                    "explain": "Goal is legality first.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "If shift exceeds chip width W, you should…",
                    "choices": [
                        "Flag failure/overflow",
                        "Ignore legality",
                        "Delete cells",
                        "Skip row checks",
                    ],
                    "answer": 0,
                    "explain": "Cannot pack in row.",
                },
            ],
            "abacus-row-pack": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": "Abacus-style packing collapses clusters toward…",
                    "choices": [
                        "Row origin / obstacles",
                        "Random coordinates",
                        "Only north edge",
                        "Negative x",
                    ],
                    "answer": 0,
                    "explain": "Cluster collapse left.",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "Fixed macros act as obstacles during Abacus pack.",
                    "answer": True,
                    "explain": "Do not move D.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Abacus and greedy snap are identical algorithms.",
                    "answer": False,
                    "explain": "Packing vs rounding.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "Track A solver stub name is…",
                    "choices": ["abacus_lite", "only hpwl", "uart_tx", "kl_refine"],
                    "answer": 0,
                    "explain": "Matches common/solvers.py.",
                },
            ],
            "tetris-row-pack": [
                {
                    "id": "q1",
                    "type": "true_false",
                    "prompt": "Tetris packing is sensitive to cell processing order.",
                    "answer": True,
                    "explain": "Order-dependent greedy fill.",
                },
                {
                    "id": "q2",
                    "type": "multiple_choice",
                    "prompt": "Tetris lite finds the leftmost…",
                    "choices": [
                        "Free slot fitting cell width",
                        "Random site",
                        "Only macro center",
                        "Pin location",
                    ],
                    "answer": 0,
                    "explain": "Slot filling on row.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Occupancy is tracked per site column in a row.",
                    "answer": True,
                    "explain": "Bitmap / interval model.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "Compare Tetris vs Abacus primarily on…",
                    "choices": [
                        "Legality, displacement, HPWL",
                        "Only font size",
                        "Git branch name",
                        "TTS voice",
                    ],
                    "answer": 0,
                    "explain": "Metrics-driven compare.",
                },
            ],
            "fixed-macros": [
                {
                    "id": "q1",
                    "type": "true_false",
                    "prompt": "Macro D is fixed at x=8, y=4 in tiny_legal.json.",
                    "answer": True,
                    "explain": "fixed_macros entry.",
                },
                {
                    "id": "q2",
                    "type": "multiple_choice",
                    "prompt": "Fixed macros during legalize should…",
                    "choices": [
                        "Move freely",
                        "Stay locked; movables pack around them",
                        "Shrink to one site",
                        "Ignore overlap rules",
                    ],
                    "answer": 1,
                    "explain": "Obstacle model.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Displacement for fixed cells is zero by definition.",
                    "answer": True,
                    "explain": "They did not move.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "Movable cells must not occupy sites already covered by…",
                    "choices": ["Fixed macros", "Only nets", "README files", "Audio clips"],
                    "answer": 0,
                    "explain": "Pre-occupied intervals.",
                },
            ],
            "displacement-hpwl": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": "HPWL after legalize uses…",
                    "choices": [
                        "Legal cell positions on the grid",
                        "Only pre-legal floats",
                        "Only macro names",
                        "Slide titles",
                    ],
                    "answer": 0,
                    "explain": "Wirelength on legal coords.",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "Lower displacement always means lower HPWL.",
                    "answer": False,
                    "explain": "Trade-off, not identity.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Nets in tiny_legal match the learn_placement toy netlist.",
                    "answer": True,
                    "explain": "Same connectivity pattern.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "Report displacement relative to…",
                    "choices": [
                        "starter_float (or documented baseline)",
                        "Random origin",
                        "Only rowH",
                        "License text",
                    ],
                    "answer": 0,
                    "explain": "Global place baseline.",
                },
            ],
            "detailed-vs-global": [
                {
                    "id": "q1",
                    "type": "true_false",
                    "prompt": "Global legalize may process all rows in one pass; detailed may iterate row-by-row.",
                    "answer": True,
                    "explain": "Pipeline contrast.",
                },
                {
                    "id": "q2",
                    "type": "multiple_choice",
                    "prompt": "Both pipelines must pass the same…",
                    "choices": [
                        "Legality checker",
                        "UART baud test",
                        "Git hook",
                        "SPICE only",
                    ],
                    "answer": 0,
                    "explain": "Shared legality gate.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Detailed always beats global on every metric.",
                    "answer": False,
                    "explain": "Measure on tiny_legal.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "This lab contrasts…",
                    "choices": [
                        "Fast global snap/pack vs multi-stage detailed flow",
                        "Floorplanning vs clustering",
                        "Analog vs digital only",
                        "Git vs SVN",
                    ],
                    "answer": 0,
                    "explain": "Legalization pipeline literacy.",
                },
            ],
        }
        items = lab_quizzes.get(
            m["lab"],
            [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": "This lab’s primary focus is…",
                    "choices": [
                        m["algorithm"],
                        "Vendor GUI only",
                        "SPICE transient",
                        "Scan stitching",
                    ],
                    "answer": 0,
                    "explain": f"Focus: {m['algorithm']}.",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "You should report legality and displacement for legalizations.",
                    "answer": True,
                    "explain": "Core legalization metrics.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": f"Track A asks you to implement {m['algorithm']} on tiny_legal.json.",
                    "answer": True,
                    "explain": "Implement track hardens the idea.",
                },
            ],
        )
        title = f"{m['short']} check"
    return {
        "module": m["id"],
        "title": title,
        "passing_score": 0.67,
        "items": items,
    }


def outline_stub(m: dict) -> str:
    return f"""title: "{m['title']}"
footer: "{COURSE_ID} — {m['short']}"
slides:
  - type: title
    title: "{m['title']}"
    subtitle: "{m['id']} · {COURSE_ID}"
    notes: |
      Stub — replace via transcript_to_outline.py after revising transcript.md.
"""


def write_modules_md() -> None:
    rows = []
    for m in MODULES:
        lab = (
            f"`{m['lab']}`"
            if m["lab"]
            else ("offline harness" if m["kind"] == "offline" else "—")
        )
        status = "**ref**" if m["kind"] == "lab" else m["status"]
        rows.append(
            f"| `{m['id']}` | `{m['kind']}` | [{m['title']}](../{m['id']}/README.md) | {lab} | {status} |"
        )
    text = f"""# {COURSE_ID} — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.
Published ids are **stable keys**; order below is the teaching path.

Status: **ref** = reference / lab id reserved for `platform/tools/` (algorithm modules).

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
{chr(10).join(rows)}

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (site/row model, legality metrics) |
| `02` | Snap & row pack (greedy snap, overlap, Abacus, Tetris) |
| `03` | Macros & objectives (fixed macros, displacement vs HPWL) |
| `04` | Global vs detailed legalize |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs (PPT / transcript)

When walkthrough frames exist: each lab module may have `assets/STEPS.md` and `assets/steps/*.png`. Map: [WALKTHROUGHS.md](WALKTHROUGHS.md).

**Build media in WSL** (LibreOffice + edge-tts + ffmpeg):

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/{COURSE_ID}/scripts/build_all_media.sh
```
"""
    write(ROOT / "docs" / "MODULES.md", text)


def write_docs() -> None:
    write(
        ROOT / "docs" / "SCOPE.md",
        f"""# Scope — {COURSE_ID}

## In scope

- Site and row geometry model (sites, rowH, cell width in sites)
- Legality checking: row alignment, site snapping, non-overlap
- Greedy site/row snap from global-place floats
- In-row overlap removal
- Abacus and Tetris-style row packing (educational lite versions)
- Fixed macro obstacles during legalization
- Displacement vs HPWL tradeoff metrics
- Global vs detailed legalization pipeline contrast
- Offline compare habits on shared tiny instances

## Out of scope (v1)

- Production OpenROAD or commercial legalizer sign-off
- Vendor GUI workflows (Innovus / ICC2 click-paths)
- Full detailed placement optimization beyond scoped lite flows
- Foundry PDK certification

## Reference instance

[`common/tiny_legal.json`](../common/tiny_legal.json): W=12 sites, H=6 (3 rows), siteW=1, rowH=2, row bottoms y=0,2,4. Cells A–D width 2 sites; E,F width 1. Nets match learn_placement. Fixed macro D at (8,4). Starters: `starter_illegal` (overlap on middle row) and `starter_float` (global-place floats).

## “Full implementation” means

Complete and correct for the **scoped problem size** (six cells on a tiny site grid): parse input, legalize, emit coordinates + legality/displacement/HPWL—not a production-scale engine.
""",
    )
    write(
        ROOT / "docs" / "TWO_TRACKS.md",
        f"""# Two learning tracks

## Track A — Implement

Practice by coding legalization checkers and row packers on the tiny instance.

- Prompts live under each `moduleSS-AA-*/EXAMPLES.md`
- Shared instance: [`common/tiny_legal.json`](../common/tiny_legal.json)
- Per-lab copy: `module*/examples/tiny_legal.json`
- Self-check: `./scripts/module.sh SS-AA --check` (e.g. `02-05`)

Use this track when you need **fidelity**: site/row geometry, legality, reproducible goldens.

## Track B — Browser lab

Practice in the learning platform concept labs (when shipped).

- Local tools: http://127.0.0.1:8080/tools/
- Live: {LIVE_TOOLS}/
- Each lab module README names its primary lab id
- Lab status **ref** in [MODULES.md](MODULES.md) marks reserved / reference lab ids

Use this track for **intuition** and quick visual feedback.

## Recommended path

1. **Track B** starter (if shipped) — 5–10 min
2. **Track A** implement + metrics — 20–45 min
3. Optional quiz / transcript review

**Prerequisite:** [learn_placement](../learn_placement/README.md) (global placement).

Doing only Track A is OK for self-study while browser labs are planned.
""",
    )
    labs = [m for m in MODULES if m["kind"] == "lab"]
    walk_rows = "\n".join(
        f"| `{m['lab']}` | [`{ss_aa(m)}`](../{m['id']}/README.md) | pending |"
        for m in labs
    )
    write(
        ROOT / "docs" / "WALKTHROUGHS.md",
        f"""# Algorithm walkthroughs (for PPT / transcript)

Step frames will live under each lab module’s `assets/steps/` with captions in `assets/STEPS.md`.
Transcripts embed them between `<!-- algorithm-walkthrough -->` markers when captured.

## Interactive viewer

`platform/tools/algorithm-walkthrough/?algo=<lab-id>&step=N`

Serve: `python3 -m http.server 8080 --directory platform`

## Capture + rebuild (WSL)

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/{COURSE_ID}/scripts/build_all_media.sh
bash courses/{COURSE_ID}/scripts/capture_all_walkthroughs.sh
```

| Algorithm | Module | Steps |
|-----------|--------|-------|
{walk_rows}

Intro / offline / wrap modules have PPTX from transcript only (no algorithm step frames).

Walkthrough PNGs are **pending** until labs ship under `platform/tools/`.
""",
    )


def write_course_readme() -> None:
    landings = "\n".join(
        f"| {ss_aa(m)} — {m['title']} | [{m['id']}]({m['id']}/README.md) |"
        for m in MODULES
    )
    lab_links = " · ".join(
        f"[{m['lab']}]({LIVE_TOOLS}/{m['lab']}/)" for m in MODULES if m["kind"] == "lab"
    )
    first_lab = next(m for m in MODULES if m["kind"] == "lab")
    write(
        ROOT / "README.md",
        f"""# {COURSE_ID}

[![GitHub](https://img.shields.io/badge/GitHub-learn__legalization-181717?logo=github)](https://github.com/universal-verification-methodology/learn_legalization)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-orange)](../../eda.md)
[![Parent](https://img.shields.io/badge/parent-learning%20monorepo-0A9EDC)](https://github.com/universal-verification-methodology/learning)
[![Labs](https://img.shields.io/badge/labs-GitHub%20Pages-222?logo=githubpages)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-legalization%20%7C%20sites%20%7C%20rows%20%7C%20Abacus-purple)](docs/MODULES.md)

**{COURSE_ID}** is the open learning path for *site/row snapping and overlap removal after global placement*—one full idea per lab, on a tiny site grid.

Readers and students usually **open a module README** (or the live tools) or work from the parent monorepo checkout. Authors edit content here, rebuild slides/audio with **module-slides** in the parent, and publish platform shells when tools + media are ready.

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

```text
{COURSE_ID}/
├── README.md
├── LICENSE              # CC BY 4.0
├── common/              # tiny_legal.json, legalization helpers
├── docs/
│   ├── MODULES.md       # full module index
│   ├── TWO_TRACKS.md    # Track A (implement) vs Track B (browser)
│   ├── SCOPE.md
│   └── WALKTHROUGHS.md  # algorithm walkthrough map
├── scripts/
│   ├── module.sh
│   ├── scaffold_course.py
│   ├── build_all_media.sh
│   └── capture_all_walkthroughs.sh
├── module00-00-intro/
├── module01-01-site-row-model/
│   ├── README.md
│   ├── CHECKLIST.md
│   ├── EXAMPLES.md
│   ├── outline.yaml
│   ├── transcript.md
│   ├── examples/        # Track A
│   └── (optional) slides.pptx / slides.pdf / video.mp4 / assets/
├── …
└── module99-00-wrap/
```

Module folders use **hierarchical ids** `moduleSS-AA-slug` so algorithms can be added later without renumbering.

Videos and decks are optional per module. Generate with the **module-slides** skill (`.cursor/skills/module-slides/`) in the parent monorepo when ready.

## Browse or clone

- **Browser labs:** [https://universal-verification-methodology.github.io/learning/tools/](https://universal-verification-methodology.github.io/learning/tools/)
- **Syllabus (parent):** [`eda.md` § {COURSE_ID}](../../eda.md)
- **Scope:** [docs/SCOPE.md](docs/SCOPE.md)
- **Prerequisite:** [learn_placement](../learn_placement/README.md)
- **From the monorepo:** open `courses/{COURSE_ID}/` (this tree).

Then open [module00-00-intro/README.md](module00-00-intro/README.md).

## Consume from the parent

From a clone of the **learning** monorepo:

```bash
git clone --recurse-submodules \\
  git@github.com:universal-verification-methodology/learning.git
# or, if already cloned without submodules:
git submodule update --init --recursive

ls courses/{COURSE_ID}
```

Working tree path in the parent: `courses/{COURSE_ID}/`.

## Author: publish or update

Edit inside the parent monorepo (recommended).

```bash
# from the learning monorepo checkout
cd courses/{COURSE_ID}
# … edit module README / CHECKLIST / EXAMPLES / transcript …

# rebuild media from the parent (one module at a time; Unix/WSL):
cd ../..
# revise transcript.md, then:
python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \\
  courses/{COURSE_ID}/{first_lab['id']}
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \\
  courses/{COURSE_ID}/{first_lab['id']}

# bulk (when asked):
# bash courses/{COURSE_ID}/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py {COURSE_ID}
```

Verify README consistency:

```bash
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \\
  courses/{COURSE_ID} --modules
```

See the skill `SKILL.md` for dual-track narration, algorithm walkthrough frames, and the full PPTX → PDF → TTS → MP4 pipeline.

## Two learning tracks

Every **lab** module documents both tracks. Intro/wrap modules have no lab. Details: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md).

| Track | Practice surface | Start here |
|-------|------------------|------------|
| **A — Implement** | Tiny legal instance + `EXAMPLES.md` / `examples/` | [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md) · `./scripts/module.sh SS-AA --check` |
| **B — Browser lab** | Platform tools | [local tools](http://127.0.0.1:8080/tools/) · [live](https://universal-verification-methodology.github.io/learning/tools/) |

Recommended path: short Track B starter (if shipped) → Track A implement + checklist → optional quiz / transcript review.

## Module landings

Full status table: **[docs/MODULES.md](docs/MODULES.md)**. Clusters: 00 intro · 01 foundations · 02 snap/pack · 03 macros/objectives · 04 global vs detailed · 05 offline · 99 wrap.

| Module | Landing |
|--------|---------|
{landings}

## Browser labs

By workflow (Track B): {lab_links}. Lab tools may still be shipping—use Track A until each id is live. See [all tools](https://universal-verification-methodology.github.io/learning/tools/) and each module README for its primary lab id. Algorithm step walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see [`LICENSE`](LICENSE).

Platform tools and the parent monorepo may carry additional notices.
""",
    )


def write_license() -> None:
    write(
        ROOT / "LICENSE",
        """Creative Commons Attribution 4.0 International (CC BY 4.0)

Copyright (c) contributors to learn_legalization / the learning monorepo.

You are free to share and adapt this material for any purpose, even commercially,
provided you give appropriate credit, provide a link to the license, and indicate
if changes were made. See https://creativecommons.org/licenses/by/4.0/ for the
full legal code.

SPDX-License-Identifier: CC-BY-4.0
""",
    )


def write_module_sh() -> None:
    write(
        ROOT / "scripts" / "module.sh",
        r"""#!/usr/bin/env bash
# Hierarchical module helper: ./scripts/module.sh SS-AA [--check|--demo|--help]
# Examples: ./scripts/module.sh 01-03 --check
#           ./scripts/module.sh 02-05 --demo
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
KEY="${1:-}"
shift || true
if [[ -z "$KEY" || "$KEY" == "--help" ]]; then
  echo "Usage: $0 SS-AA [--check|--demo|--help]"
  echo "  SS-AA matches moduleSS-AA-* (e.g. 01-03, 02-05, 99-00)"
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
    echo "Module dir: $MOD_DIR"
    command -v bash >/dev/null && echo "[OK] bash"
    [[ -f "$MOD_DIR/EXAMPLES.md" ]] && echo "[OK] EXAMPLES.md" || echo "[INFO] no EXAMPLES.md"
    [[ -f "$MOD_DIR/CHECKLIST.md" ]] && echo "[OK] CHECKLIST.md"
    [[ -f "$MOD_DIR/transcript.md" ]] && echo "[OK] transcript.md"
    [[ -f "$MOD_DIR/examples/tiny_legal.json" ]] && echo "[OK] examples/tiny_legal.json" || echo "[INFO] no examples/tiny_legal.json"
    echo "[INFO] Track B lab link is in README.md"
    echo "[INFO] --check placeholder: implement goldens when solvers land"
    ;;
  --demo)
    echo "Demo: open $MOD_DIR/EXAMPLES.md and README.md"
    ;;
  *)
    echo "Unknown option: $ACTION"
    exit 1
    ;;
esac
""",
    )


def write_build_script() -> None:
    all_mods = "\n  ".join(m["id"] for m in MODULES)
    write(
        ROOT / "scripts" / "build_all_media.sh",
        f"""#!/usr/bin/env bash
# Build {COURSE_ID} media in WSL/Linux (canonical module-slides path).
#
# From repo root (WSL or Linux — not Windows):
#   bash courses/{COURSE_ID}/scripts/build_all_media.sh
#   bash courses/{COURSE_ID}/scripts/build_all_media.sh --pptx-only
#   bash courses/{COURSE_ID}/scripts/build_all_media.sh --no-video
#
# Requires: python3, soffice (LibreOffice), edge-tts; ffmpeg+pdftoppm for video.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
COURSE_DIR="$(cd "${{SCRIPT_DIR}}/.." && pwd)"
ROOT="$(cd "${{COURSE_DIR}}/../.." && pwd)"
SKILL="${{ROOT}}/.cursor/skills/module-slides/scripts"

# shellcheck source=/dev/null
source "${{SKILL}}/_require_unix.sh"

DO_PPTX=1
DO_NARRATE=1
DO_VIDEO=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pptx-only) DO_NARRATE=0; DO_VIDEO=0 ;;
    --no-video) DO_VIDEO=0 ;;
    --help|-h)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown flag: $1" >&2
      exit 2
      ;;
  esac
  shift
done

cd "$ROOT"

if [[ ! -d "$SKILL" ]]; then
  echo "ERROR: missing skill scripts at $SKILL" >&2
  exit 1
fi

ALL=(
  {all_mods}
)

if [[ "$DO_PPTX" -eq 1 && "$DO_NARRATE" -eq 0 ]]; then
  echo "=== PPTX only ==="
  for m in "${{ALL[@]}}"; do
    d="${{COURSE_DIR}}/${{m}}"
    python3 "${{SKILL}}/transcript_to_outline.py" "$d"
    python3 "${{SKILL}}/build_pptx.py" "$d"
    python3 "${{SKILL}}/verify_transcript_consistency.py" "$d"
  done
fi

if [[ "$DO_NARRATE" -eq 1 ]]; then
  echo "=== Narrate (outline + PPTX + PDF + audio${{DO_VIDEO:+ + video}}) ==="
  if [[ "$DO_VIDEO" -eq 1 ]]; then
    bash "${{SKILL}}/narrate_clips.sh" --course-dir "$COURSE_DIR"
  else
    for m in "${{ALL[@]}}"; do
      d="${{COURSE_DIR}}/${{m}}"
      echo
      echo "======== ${{m}} ========"
      python3 "${{SKILL}}/transcript_to_outline.py" "$d"
      python3 "${{SKILL}}/build_pptx.py" "$d"
      python3 "${{SKILL}}/verify_transcript_consistency.py" "$d"
      pptx="$d/slides.pptx"
      [[ -f "$pptx" ]] || pptx="$d/clip.pptx"
      bash "${{SKILL}}/pptx_to_pdf.sh" "$pptx"
      python3 "${{SKILL}}/synthesize_audio.py" "$d" --voice "${{VOICE:-en-US-JennyNeural}}"
    done
  fi

  echo "=== Platform publish (catalog + course pages + course-media) ==="
  python3 "${{ROOT}}/platform/scripts/publish_course_platform.py" {COURSE_ID}
fi

echo
echo "Done (WSL). Course: $COURSE_DIR"
""",
    )


def write_capture_script() -> None:
    lab_mods = [m for m in MODULES if m["kind"] == "lab"]
    mod_list = " \\\n  ".join(m["id"] for m in lab_mods)
    write(
        ROOT / "scripts" / "capture_all_walkthroughs.sh",
        f"""#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/proj/designs/eda_learning
for m in \\
  {mod_list}
do
  echo "=== $m ==="
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \\
    "courses/{COURSE_ID}/$m" --inject-transcript
done
echo CAPTURE_OK
ls courses/{COURSE_ID}/module*/assets/steps/*.png 2>/dev/null | wc -l
""",
    )


def write_common_files() -> None:
    write(
        ROOT / "common" / "README.md",
        f"""# common — {COURSE_ID}

Shared Track A helpers for tiny legalization instances.

## Starter instance

[`tiny_legal.json`](tiny_legal.json) — W=12 sites, H=6 (3 rows), siteW=1, rowH=2, row bottoms y=0,2,4.
Cells A–D width 2 sites; E,F width 1. Nets match learn_placement. Macro D fixed at (8,4).

Starters:
- `starter_illegal` — A,B,C overlap on middle row (integer coords)
- `starter_float` — global-place floats for greedy snap

Suggested layout as reference solvers mature:

- `legalizationutil.py` — load JSON, legality, displacement, HPWL helpers
- `solvers.py` — greedy_snap, overlap_remove, abacus_lite, tetris_lite
- `test_solvers.py` — smoke tests (goldens pending platform JS alignment)

Browser algorithms will live under `platform/tools/<lab-id>/` when published.
""",
    )
    write(ROOT / "common" / "tiny_legal.json", tiny_legal_json())


def main() -> None:
    write_license()
    write_docs()
    write_modules_md()
    write_course_readme()
    write_common_files()
    write_module_sh()
    write_build_script()
    write_capture_script()

    tiny = tiny_legal_json()
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
            write(base / "examples" / "tiny_legal.json", tiny)
        print(f"ok {mid}")
    print(f"Scaffolded {len(MODULES)} modules under {ROOT}")


if __name__ == "__main__":
    main()
