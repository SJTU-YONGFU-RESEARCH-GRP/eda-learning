#!/usr/bin/env python3
"""Scaffold learn_routing (hierarchical SS-AA ids) with module-slides stubs."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "learn_routing"
LIVE_TOOLS = "https://universal-verification-methodology.github.io/learning/tools"

MODULES = [
    {
        "id": "module00-00-intro",
        "kind": "intro",
        "title": "Welcome to detailed routing for EDA",
        "short": "Welcome",
        "lab": None,
        "status": "—",
        "section": "00",
        "outcomes": "Explain why detailed routing follows global routing and assigns tracks, vias, and DRC-clean paths.",
        "algorithm": None,
    },
    {
        "id": "module01-01-routing-grid",
        "kind": "lab",
        "title": "Routing grid graph",
        "short": "Routing grid",
        "lab": "routing-grid",
        "status": "**ref**",
        "section": "01",
        "outcomes": "Build the M1/M2 track graph on a 12×8 grid and list horizontal and vertical edges.",
        "algorithm": "routing grid graph (M1 horizontal + M2 vertical tracks)",
    },
    {
        "id": "module01-03-pin-access",
        "kind": "lab",
        "title": "Pin access points",
        "short": "Pin access",
        "lab": "pin-access",
        "status": "**ref**",
        "section": "01",
        "outcomes": "Map each pin placement to grid access points usable by detailed routers.",
        "algorithm": "pin access point assignment on the routing grid",
    },
    {
        "id": "module02-01-lee-maze",
        "kind": "lab",
        "title": "Lee maze routing",
        "short": "Lee maze",
        "lab": "lee-maze",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Find a shortest grid path with BFS while avoiding blockages and occupied cells.",
        "algorithm": "Lee maze routing (BFS on grid cells)",
    },
    {
        "id": "module02-03-astar-route",
        "kind": "lab",
        "title": "A* detailed routing",
        "short": "A* route",
        "lab": "astar-route",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Route two-pin nets with A* that penalizes tracks at capacity.",
        "algorithm": "A* detailed routing (congestion-aware grid search)",
    },
    {
        "id": "module02-05-track-usage",
        "kind": "lab",
        "title": "Track usage and capacity",
        "short": "Track usage",
        "lab": "track-usage",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Deposit route segments on directed M1/M2 tracks and report track overflow.",
        "algorithm": "track usage and overflow metrics (total, max, count)",
    },
    {
        "id": "module02-07-via-assignment",
        "kind": "lab",
        "title": "Via assignment (2-layer)",
        "short": "Via assign",
        "lab": "via-assignment",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Assign layer changes at L-route bends with explicit via markers on M1/M2.",
        "algorithm": "two-layer via assignment on L-shaped paths",
    },
    {
        "id": "module03-01-drc-spacing",
        "kind": "lab",
        "title": "DRC spacing lite",
        "short": "DRC spacing",
        "lab": "drc-spacing",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Detect same-layer parallel segments that violate minimum spacing on the toy grid.",
        "algorithm": "DRC spacing lite (parallel same-layer distance check)",
    },
    {
        "id": "module03-03-ripup-detailed",
        "kind": "lab",
        "title": "Rip-up and reroute (detailed)",
        "short": "Rip-up DR",
        "lab": "ripup-detailed",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Rip the hottest congested net and A*-reroute it to reduce track overflow.",
        "algorithm": "rip-up and A* reroute on track usage",
    },
    {
        "id": "module04-01-sequential-detailed",
        "kind": "lab",
        "title": "Sequential detailed route",
        "short": "Sequential DR",
        "lab": "sequential-detailed",
        "status": "**ref**",
        "section": "04",
        "outcomes": "Route all nets in order with layer-aware paths and measure resulting track congestion.",
        "algorithm": "sequential detailed routing (ordered net deposit on tracks)",
    },
    {
        "id": "module05-01-offline-benchmark-compare",
        "kind": "offline",
        "title": "Offline benchmark compare",
        "short": "Offline compare",
        "lab": None,
        "status": "P",
        "section": "05",
        "outcomes": "Compare Lee, A*, L-layer, and rip-up engines on shared instances (overflow, runtime, notes).",
        "algorithm": "benchmark harness vs reference detailed routes",
    },
    {
        "id": "module99-00-wrap",
        "kind": "wrap",
        "title": "Detailed routing path complete",
        "short": "Wrap",
        "lab": None,
        "status": "—",
        "section": "99",
        "outcomes": "Recap grid, maze, A*, track usage, vias, DRC, rip-up; choose compaction or pattern matching next.",
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


def tiny_dr() -> dict:
    return {
        "chip": {"W": 12, "H": 8},
        "grid": {"nx": 12, "ny": 8},
        "track_capacity": 1,
        "layers": ["M1", "M2"],
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
        "placement": {
            "A": {"x": 1, "y": 1},
            "B": {"x": 8, "y": 1},
            "C": {"x": 1, "y": 5},
            "D": {"x": 8, "y": 5},
            "E": {"x": 5, "y": 3},
            "F": {"x": 6, "y": 3},
        },
        "blockages": [{"x": 5, "y": 2, "w": 2, "h": 2}],
        "notes": "12×8 grid. M1=horizontal edges, M2=vertical. Via at (x,y) connects layers. track_capacity=1 per directed edge.",
    }


def tiny_dr_json() -> str:
    return json.dumps(tiny_dr(), indent=2) + "\n"


PSEUDO: dict[str, str] = {
    "routing-grid": """## Pseudocode

```text
Input: nx, ny grid, layers M1 (horizontal), M2 (vertical)
h_edges ← empty;  v_edges ← empty
for each grid point (x,y):
  if x+1 < nx: add directed M1 edge ((x,y)→(x+1,y))
  if y+1 < ny: add directed M2 edge ((x,y)→(x,y+1))
Output: track graph with canonical directed keys
Golden: 12×8 yields 11×8 M1 edges and 12×7 M2 edges
```
""",
    "pin-access": """## Pseudocode

```text
Input: pin (x,y), grid nx×ny, blockages[]
(gx,gy) ← pin_grid(round x, round y) clamped to grid
if cell_blocked(gx,gy): nudge to nearest free neighbor4
access[cell_id] ← (gx, gy)
Output: map cell → grid access point for routing start/end
Golden: A at (1,1) → (1,1); E at (5,3) near blockage nudges off (5,2)
```
""",
    "lee-maze": """## Pseudocode

```text
Input: start, goal, blocked cells, nx, ny
BFS queue ← (start, [start]);  visited ← {start}
while queue not empty:
  pop (cur, path)
  for each neighbor nb in neighbors4(cur) minus blocked:
    if nb == goal: return path + [nb]
    if nb not visited: enqueue (nb, path + [nb])
Output: shortest cell path or None
Golden: (4,1)→(7,1) detours around blockage 5,2,2,2
```
""",
    "astar-route": """## Pseudocode

```text
Input: start, goal, track usage, capacity Cap, blockages
open ← min-heap by f = g + Manhattan(goal)
while open not empty:
  pop (g, cur, path)
  for each 4-neighbor nb on M1 or M2 layer step:
    if cell_blocked(nb): skip
    step_cost ← 1 + 10×overflow_penalty if usage[track] ≥ Cap
    if better g to nb: push (g+step_cost, nb, path+[nb])
Output: congestion-aware shortest path or None
Golden: hot M1 edge ((1,1),(2,1)) at Cap=1 forces detour
```
""",
    "track-usage": """## Pseudocode

```text
Input: route segments [{x,y,layer}, …], capacity Cap
for each consecutive pair (a,b) in path:
  key ← h_edge(a,b) if horizontal else v_edge(a,b)
  usage[key] += 1
for each track t: ov[t] ← max(0, usage[t] − Cap)
Output: {total, max, count, perTrack} overflow summary
Golden: sequential L-HV on six nets overflows at Cap=1
```
""",
    "via-assignment": """## Pseudocode

```text
Input: start, goal, prefer HV or VH
Walk first axis on M1 (H) or M2 (V) per prefer
At bend cell: append segment with via=True on incoming layer
Continue second axis on opposite layer
Output: segment list with explicit via markers
Golden: (1,1)→(5,4) HV includes at least one via=True segment
```
""",
    "drc-spacing": """## Pseudocode

```text
Input: segments, min_dist (default 1)
Group points by layer M1 / M2
for each same-layer pair on parallel tracks:
  if 0 < track_distance ≤ min_dist: return FAIL + violation
Output: {pass: true/false, violation or null}
Golden: parallel M1 rows y=2 and y=3 one track apart → fail
```
""",
    "ripup-detailed": """## Pseudocode

```text
Input: routes per net, track usage, Cap, terminals, blockages
worst ← net with largest track overflow on its segments
subtract worst's track usage from global map
newSegs ← astar_route(worst pins, remaining usage, Cap) or L fallback
add newSegs track usage back
Output: updated usage; total overflow ≤ before (ideal)
Golden: after sequential L-HV seed, one rip-up drops total overflow
```
""",
    "sequential-detailed": """## Pseudocode

```text
Input: ordered nets[], terminals, mode (astar/l_hv/lee), Cap
usage ← empty;  routes ← empty
for each net N in order:
  route N with chosen mode respecting current usage + blockages
  deposit +1 on each directed track key in the route
Output: routes map + final usage; order affects congestion
Golden: all six nets in default order yields positive track overflow
```
""",
}


LAB_QUIZZES: dict[str, list] = {
    "routing-grid": [
        {
            "id": "routing-grid-q1",
            "type": "mcq",
            "prompt": "On our toy grid M1 tracks run…",
            "choices": [
                "Horizontally (left–right)",
                "Vertically only",
                "Diagonally",
                "Only inside vias",
            ],
            "answer": 0,
        },
        {
            "id": "routing-grid-q2",
            "type": "mcq",
            "prompt": "A 12×8 routing grid has how many M1 horizontal directed edges?",
            "choices": ["11×8 = 88", "12×8 = 96", "12×7 = 84", "11×7 = 77"],
            "answer": 0,
        },
        {
            "id": "routing-grid-q3",
            "type": "mcq",
            "prompt": "Detailed routes deposit usage on…",
            "choices": [
                "Directed track edges (M1 or M2)",
                "GCell coarse edges only",
                "Liberty arcs",
                "Scan chain flops",
            ],
            "answer": 0,
        },
    ],
    "pin-access": [
        {
            "id": "pin-access-q1",
            "type": "mcq",
            "prompt": "Pin access maps a pin to…",
            "choices": [
                "A grid cell the router can start from",
                "A GCell four tiles wide",
                "A Liberty timing arc",
                "A power strap only",
            ],
            "answer": 0,
        },
        {
            "id": "pin-access-q2",
            "type": "mcq",
            "prompt": "If a pin lands inside a blockage we…",
            "choices": [
                "Nudge to a free neighbor on the grid",
                "Delete the net",
                "Skip detailed routing forever",
                "Inflate the chip",
            ],
            "answer": 0,
        },
        {
            "id": "pin-access-q3",
            "type": "mcq",
            "prompt": "Access points are needed before…",
            "choices": [
                "Lee, A*, or layer-aware pattern routes",
                "Synthesis only",
                "Floorplanning only",
                "Scan insertion",
            ],
            "answer": 0,
        },
    ],
    "lee-maze": [
        {
            "id": "lee-maze-q1",
            "type": "mcq",
            "prompt": "Lee maze routing uses…",
            "choices": [
                "BFS for shortest cell path",
                "DFS only",
                "Simulated annealing",
                "SPICE transient",
            ],
            "answer": 0,
        },
        {
            "id": "lee-maze-q2",
            "type": "mcq",
            "prompt": "Lee maze skips cells that are…",
            "choices": ["Blocked or in the blockage set", "On M1 only", "Always diagonal", "Outside the netlist"],
            "answer": 0,
        },
        {
            "id": "lee-maze-q3",
            "type": "mcq",
            "prompt": "If no feasible path exists, lee_maze returns…",
            "choices": ["None", "A random walk", "Negative overflow", "A via stack only"],
            "answer": 0,
        },
    ],
    "astar-route": [
        {
            "id": "astar-route-q1",
            "type": "mcq",
            "prompt": "Our A* router penalizes tracks where…",
            "choices": ["usage ≥ capacity", "usage = 0", "pins align", "HPWL = 0"],
            "answer": 0,
        },
        {
            "id": "astar-route-q2",
            "type": "mcq",
            "prompt": "A* uses Manhattan distance as…",
            "choices": ["Heuristic h toward the goal", "DRC spacing rule", "Via count only", "Power IR drop"],
            "answer": 0,
        },
        {
            "id": "astar-route-q3",
            "type": "mcq",
            "prompt": "Horizontal steps in A* use layer…",
            "choices": ["M1", "M2", "M3 always", "No layer"],
            "answer": 0,
        },
    ],
    "track-usage": [
        {
            "id": "track-usage-q1",
            "type": "mcq",
            "prompt": "Track overflow on one directed edge is…",
            "choices": ["max(0, usage − capacity)", "usage × capacity", "HPWL only", "Always zero"],
            "answer": 0,
        },
        {
            "id": "track-usage-q2",
            "type": "mcq",
            "prompt": "path_track_usage converts segments to…",
            "choices": [
                "Directed M1/M2 edge counts",
                "Only via locations",
                "GCell demand",
                "Liberty tables",
            ],
            "answer": 0,
        },
        {
            "id": "track-usage-q3",
            "type": "mcq",
            "prompt": "Sequential L-HV at Cap=1 on tiny_dr should…",
            "choices": [
                "Produce positive total track overflow",
                "Always be zero overflow",
                "Skip track counting",
                "Only count vias",
            ],
            "answer": 0,
        },
    ],
    "via-assignment": [
        {
            "id": "via-assignment-q1",
            "type": "mcq",
            "prompt": "An L-route with prefer=HV walks horizontal on…",
            "choices": ["M1 first, then vertical on M2", "M2 only", "Diagonals", "Random layers"],
            "answer": 0,
        },
        {
            "id": "via-assignment-q2",
            "type": "mcq",
            "prompt": "A layer change at the bend is marked with…",
            "choices": ["via=True on the segment", "A new net name", "DRC waiver", "Scan bit"],
            "answer": 0,
        },
        {
            "id": "via-assignment-q3",
            "type": "mcq",
            "prompt": "Two-layer via assignment teaches…",
            "choices": [
                "How detailed routers connect M1 and M2",
                "Clock-tree buffering",
                "Power-grid synthesis only",
                "Abacus packing",
            ],
            "answer": 0,
        },
    ],
    "drc-spacing": [
        {
            "id": "drc-spacing-q1",
            "type": "mcq",
            "prompt": "DRC spacing lite checks…",
            "choices": [
                "Same-layer parallel segments too close",
                "Only via enclosure",
                "Only power straps",
                "Scan chain order",
            ],
            "answer": 0,
        },
        {
            "id": "drc-spacing-q2",
            "type": "mcq",
            "prompt": "Parallel M1 segments one track apart with min_dist=1…",
            "choices": ["Fail spacing", "Always pass", "Require a via", "Skip DRC"],
            "answer": 0,
        },
        {
            "id": "drc-spacing-q3",
            "type": "mcq",
            "prompt": "Production DRC is heavier; this lab teaches…",
            "choices": [
                "The idea of geometric spacing rules",
                "Foundry tape-out signoff only",
                "Nothing useful",
                "Only global routing",
            ],
            "answer": 0,
        },
    ],
    "ripup-detailed": [
        {
            "id": "ripup-detailed-q1",
            "type": "mcq",
            "prompt": "Rip-up picks the net with…",
            "choices": [
                "Largest track overflow on its route",
                "Shortest HPWL always",
                "Lowest pin count always",
                "Random selection",
            ],
            "answer": 0,
        },
        {
            "id": "ripup-detailed-q2",
            "type": "mcq",
            "prompt": "After rip-up we reroute with…",
            "choices": [
                "A* respecting remaining track usage",
                "Same L blindly",
                "Delete the net",
                "Inflate cells",
            ],
            "answer": 0,
        },
        {
            "id": "ripup-detailed-q3",
            "type": "mcq",
            "prompt": "Rip-up should ideally…",
            "choices": [
                "Not increase total track overflow vs before",
                "Always zero all overflow",
                "Skip usage accounting",
                "Only run in global route",
            ],
            "answer": 0,
        },
    ],
    "sequential-detailed": [
        {
            "id": "sequential-detailed-q1",
            "type": "mcq",
            "prompt": "Sequential detailed routing processes nets…",
            "choices": [
                "In a fixed order, depositing on shared tracks",
                "All in parallel with no sharing",
                "Only before placement",
                "Only after compaction",
            ],
            "answer": 0,
        },
        {
            "id": "sequential-detailed-q2",
            "type": "mcq",
            "prompt": "route mode astar means…",
            "choices": [
                "Congestion-aware A* for two-pin nets",
                "GCell maze only",
                "Skip multi-pin nets",
                "Ignore blockages",
            ],
            "answer": 0,
        },
        {
            "id": "sequential-detailed-q3",
            "type": "mcq",
            "prompt": "Order sensitivity means…",
            "choices": [
                "Later nets see congested tracks from earlier nets",
                "Order never matters",
                "Only one net routes",
                "Capacity is ignored",
            ],
            "answer": 0,
        },
    ],
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

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **{m['algorithm']}** on `examples/tiny_dr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with track usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh {key} --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/{lab}/](http://127.0.0.1:8080/tools/{lab}/)
2. Live: [{LIVE_TOOLS}/{lab}/]({LIVE_TOOLS}/{lab}/)
3. Tools shelf: open `{lab}` from the platform tools index
4. Load the **starter detailed routing** instance, run the router, inspect track overflow and vias.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach detailed routing literacy on a tiny M1/M2 grid — not production signoff routers.
"""
    elif m["kind"] == "offline":
        body = f"""
## Outcomes

After this module you can: **{m['outcomes']}**

## Offline track

1. Follow [EXAMPLES.md](EXAMPLES.md) to run the local compare harness.
2. Record track overflow totals and runtime against at least one reference when available.
3. Complete [CHECKLIST.md](CHECKLIST.md).
"""
    elif m["kind"] == "intro":
        body = """
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
"""
    else:
        body = """
## You can now

- Build a routing grid with M1/M2 tracks and assign pin access points
- Route with Lee maze, A*, layer-aware L paths, and via assignment
- Measure track overflow, check DRC spacing lite, and rip-up congested nets
- Run sequential detailed routing on the tiny instance

## Dual-track recap

If you mainly used **browser labs**, spend a short session on Track A for A* and track overflow metrics.
If you mainly used **Track A**, skim any skipped shipped browser labs for visual track heat maps.

## Next course

Prereqs done: **learn_global_routing**.

→ **learn_compaction** or **learn_pattern_matching** (see parent [`eda.md`](../../../eda.md))

## Checklist

- [ ] I completed Track A and/or Track B for the lab modules I care about
- [ ] I can explain Lee vs A* vs rip-up in my own words
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
- [ ] Implemented **{m['algorithm']}** end-to-end on `examples/tiny_dr.json`
- [ ] Reported track usage / overflow when relevant
- [ ] Can explain the algorithm without the UI

## Track B — Browser lab (`{m['lab']}`)

- [ ] Opened the lab (local or live)
- [ ] Loaded the starter detailed routing instance
- [ ] Ran the router and inspected track overflow / vias

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

- [ ] I can explain how to judge detailed routing quality across engines
"""
    if m["kind"] == "intro":
        return f"""# Checklist — {m['title']}

- [ ] I understand the course map (sections 01–05 + wrap)
- [ ] I know Track A (implement) vs Track B (browser lab)
- [ ] I opened [docs/MODULES.md](../docs/MODULES.md) once
- [ ] I finished learn_global_routing or know why detailed route follows it
- [ ] Ready for the routing grid graph
"""
    return f"""# Checklist — {m['title']}

- [ ] I can name the main detailed routing ideas from sections 01–04
- [ ] I know when Lee vs A* vs rip-up fits
- [ ] I picked a next course (`learn_compaction` or `learn_pattern_matching`)
"""


def examples(m: dict) -> str:
    if m["kind"] == "lab":
        lab = m["lab"]
        pseudo = PSEUDO.get(lab, "## Pseudocode\n\n```text\n(see common/solvers.py)\n```\n")
        return f"""# Examples — {m['title']}

Track A (implement). Use the tiny detailed routing instance first (`examples/tiny_dr.json`).

## Algorithm

**{m['algorithm']}**

{pseudo}

## Track A API

```bash
# from courses/learn_routing/
python3 -c "from common.solvers import route_from_data; from common.drutil import load; d=load('common/tiny_dr.json'); print(route_from_data(d))"
```

Prefer helpers in `common/drutil.py` and `common/solvers.py` over ad-hoc scripts.

## Starter prompts

1. Load `placement`, `blockages`, and `nets` from `tiny_dr.json`; print the 12×8 grid and track count.
2. Run the algorithm for this lab; print track usage or overflow with two decimals.
3. Compare sequential L-HV vs A* on total track overflow.
4. Change track_capacity from 1 to 2 and report which tracks flip congested.
5. Write one sentence: why this idea belongs after global routing.

## Expected artifacts

- Track usage map or segment listing for the lab algorithm
- Overflow summary (total, max, count) when relevant
- Short note tying the metric to rip-up or sequential order
"""
    if m["kind"] == "offline":
        return """# Examples — Offline benchmark compare

1. Export the same tiny_dr instance used in sequential / overflow labs.
2. Run Lee, L-HV, A*, and one rip-up pass; record total track overflow and wall time.
3. If available, compare against a reference detailed route.
4. Fill a comparison table: quality, overflow, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
"""
    if m["kind"] == "intro":
        return """# Examples — Welcome

No coding yet.

1. Sketch the PD path: place → legalize → global route → **detailed route** → compaction / signoff.
2. Write one sentence: “Detailed routing exists because …”
3. Name one difference between GCell edge usage (global route) and directed track usage (detailed route).
"""
    return """# Examples — Wrap

1. List three detailed routing algorithms from this course and one strength each.
2. For a congested sequential L pass, which module’s idea do you reach for first?
3. Write the bridge sentence you’ll need for compaction or pattern matching next.
"""


LAB_TRANSCRIPTS: dict[str, str] = {
    "routing-grid": """# Routing grid graph

**Module id:** module01-01-routing-grid
**Lab:** routing-grid
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Why a track graph

Detailed routers do not hop GCell to GCell. They walk a fine grid whose edges are directed tracks: M1 horizontal and M2 vertical. Before any maze or A* route, you must enumerate those tracks on our twelve-by-eight toy grid.

## Slide 2 — The idea

For each grid point at column x and row y, add a directed M1 edge to the right neighbor when x plus one is less than nx, and a directed M2 edge upward when y plus one is less than ny. Canonical keys sort endpoints so left-to-right and bottom-to-top always win. On twelve by eight you get eighty-eight M1 edges and eighty-four M2 edges.

## Slide 3 — Browser lab track

Open the **routing-grid** lab. Toggle layer M1 and M2 overlays. Highlight one horizontal track between columns one and two on row one. Read the track list in the metrics panel and match the counts.

## Slide 4 — Implement track

Inspect `h_edge`, `v_edge`, and `track_key` in `common/drutil.py`. Print sample M1 and M2 keys for tiny_dr. Verify diagonals are absent and layers match movement axis.

## Slide 5 — Pitfalls

Counting grid points instead of directed tracks. Treating M1 and M2 as interchangeable. Forgetting blockages still occupy cells even if tracks exist between free neighbors.

## Slide 6 — Your turn

Finish the checklist. Sketch M1 on one row from memory. Next: map pin placements to access points on the grid.
""",
    "pin-access": """# Pin access points

**Module id:** module01-03-pin-access
**Lab:** pin-access
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Pins need grid access

A detailed route starts and ends at grid access points—integer cells the router can reach. Legal placement gives you x y coordinates; this module converts them with round-and-clamp and nudges off blockages when needed.

## Slide 2 — The idea

pin_grid of x y returns column gx equals round of x clamped zero to nx minus one, and row gy likewise. Cell A at one comma one maps to one comma one. Cell E at five comma three sits near the blockage at five comma two; nudge to a free neighbor if the pin lands inside the blocked rectangle.

## Slide 3 — Browser lab track

Open **pin-access**. Hover each cell and read its access grid point. Move a pin across the blockage boundary and watch the access index shift. Confirm all six cells on tiny_dr match your Track A printout.

## Slide 4 — Implement track

Implement or call `terminals(positions, data)` in `common/drutil.py`. Assert A through F on spread placement. Print access points before any routing lab.

## Slide 5 — Pitfalls

Using GCell floor divide from global routing instead of per-grid rounding. Off-by-one at the chip edge without clamp. Ignoring blockages when assigning access.

## Slide 6 — Your turn

Complete access points for all six cells. Next: Lee maze routing around the central blockage.
""",
    "lee-maze": """# Lee maze routing

**Module id:** module02-01-lee-maze
**Lab:** lee-maze
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Cell paths before layers

Lee maze finds a shortest path on grid cells ignoring track congestion—ideal for teaching detours around blockages before A* adds capacity penalties.

## Slide 2 — The idea

Seed a BFS queue with start and path list. Pop, expand neighbors4 skipping blocked cells, return the first path that reaches the goal. If the queue empties, return None. Shortest cell hop count wins.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **lee-maze**. Route from four comma one to seven comma one with the blockage at five comma two visible. Watch maze pick a longer detour above or below the blocked rectangle.

## Slide 4 — Implement track

Implement `lee_maze(start, goal, blocked, nx, ny)`. Block cells inside five comma two two by two and show the path avoids them. Match the browser overlay.

## Slide 5 — Pitfalls

Treating blockages as track usage instead of forbidden cells. Forgetting BFS needs visited on cells not edges. Returning a path through a blocked cell because neighbor checks were skipped.

## Slide 6 — Your turn

Pass Lee maze goldens. Next: A* routing that respects track capacity.
""",
    "astar-route": """# A* detailed routing

**Module id:** module02-03-astar-route
**Lab:** astar-route
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Congestion-aware search

Lee ignores other nets. Production detailed routers penalize hot tracks. Our A* adds a heavy step cost when usage is already at capacity so routes detour around congested M1 or M2 edges.

## Slide 2 — The idea

Maintain open heap ordered by f equals g plus Manhattan distance to goal. Expand four neighbors on M1 for horizontal steps and M2 for vertical. Step cost is one plus ten times overflow penalty when usage meets capacity. First time you pop the goal, return the path.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **astar-route**. Pre-fill M1 edge one comma one to two comma one at capacity one and watch A* pick a longer detour. Clear the block and confirm the shortest path returns.

## Slide 4 — Implement track

Implement or call `astar_route(start, goal, usage, cap, nx, ny, blocks)`. Block the hot edge and show A* cannot go direct; unblock a vertical detour path exists.

## Slide 5 — Pitfalls

Using undirected track keys inconsistently. Checking capacity on the wrong layer for a move. Forgetting blockages still forbid cells even when tracks are free.

## Slide 6 — Your turn

Clear A* challenges. Next: deposit segments on tracks and measure overflow.
""",
    "track-usage": """# Track usage and capacity

**Module id:** module02-05-track-usage
**Lab:** track-usage
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — When usage exceeds capacity

Each directed M1 or M2 track has capacity one on tiny_dr. Every routed net deposits plus one on each track its segments traverse. Overflow is how far usage exceeds capacity—summed, maxed, and counted per track.

## Slide 2 — The idea

path_track_usage walks consecutive segment pairs, maps horizontal moves to h_edge and vertical to v_edge, increments usage. track_overflow computes max of zero and usage minus capacity per track. Sequential L-HV on all six nets should yield positive total overflow at cap one.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **track-usage**. Run sequential L routes and read the triple total max count. Heat-map the worst track.

## Slide 4 — Implement track

Implement `path_track_usage` and `track_overflow`. Call sequential_detailed with mode l_hv on tiny_dr and assert total overflow is greater than zero.

## Slide 5 — Pitfalls

Computing overflow before summing all nets. Using GCell edge usage from global routing instead of directed tracks. Reporting negative overflow values.

## Slide 6 — Your turn

Hit overflow targets. Next: assign vias on two-layer L paths.
""",
    "via-assignment": """# Via assignment (2-layer)

**Module id:** module02-07-via-assignment
**Lab:** via-assignment
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Layer changes at bends

Real detailed routes switch between M1 and M2 at vias. Our L-route with layers walks horizontal on M1 and vertical on M2—or the VH variant—and marks via equals true at the bend cell.

## Slide 2 — The idea

Given start and goal, prefer HV walks horizontal on M1 to align columns, inserts a via segment at the bend, then walks vertical on M2. l_route_layers returns segment dicts with x y layer and optional via flag. A path from one comma one to five comma four in HV includes at least one via.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **via-assignment**. Route A to B with HV and read via markers in the segment list. Toggle VH on the same pair and compare the bend cell and layers.

## Slide 4 — Implement track

Implement `l_route_layers(a, b, prefer)`. Route net A–B on tiny_dr and print segments with via flags. Match the browser overlay.

## Slide 5 — Pitfalls

Skipping the via marker at the bend. Putting horizontal motion on M2 or vertical on M1. Forgetting the final segment must land on the goal coordinates.

## Slide 6 — Your turn

Ship Track A layer routes with vias. Next: DRC spacing lite on parallel tracks.
""",
    "drc-spacing": """# DRC spacing lite

**Module id:** module03-01-drc-spacing
**Lab:** drc-spacing
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Geometry rules matter

Signoff DRC is vast; spacing lite teaches the idea: same-layer parallel segments too close fail even when tracks are logically free.

## Slide 2 — The idea

Group segment points by layer. For M1 pairs on the same row y, if horizontal distance is greater than zero but less than or equal to min_dist, return fail with violation coordinates. Likewise for M2 pairs on the same column x. Otherwise pass.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **drc-spacing**. Place parallel M1 segments one track apart on adjacent rows and read the violation panel. Widen spacing and confirm pass.

## Slide 4 — Implement track

Implement `drc_spacing_lite(segments, min_dist)`. Feed the golden failing segment set from test_solvers and assert pass is false.

## Slide 5 — Pitfalls

Checking cross-layer pairs—this lite rule is same-layer only. Using Manhattan grid distance across rows for M1 horizontal segments. Treating DRC pass as proof of tape-out readiness.

## Slide 6 — Your turn

Clear DRC spacing challenges. Next: rip-up the hottest net and A* reroute.
""",
    "ripup-detailed": """# Rip-up and reroute (detailed)

**Module id:** module03-03-ripup-detailed
**Lab:** ripup-detailed
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Relieve track hotspots

When track overflow appears, detailed routers rip up contributing nets and reroute around congested tracks. Our toy pass picks the net whose route contributes the most overflow, removes its usage, then A*-reroutes.

## Slide 2 — The idea

Score each net by track overflow on its segments. Subtract its route from usage. Run astar_route between its pins with the remaining usage map. Add the new segment track usage back. Total overflow should not rise; ideally it drops versus the pre-rip state.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **ripup-detailed**. Run sequential L to create overflow, then one rip-up pass. Watch total overflow fall on the metrics panel.

## Slide 4 — Implement track

Implement `ripup_detailed(routes, usage, cap, terminals_map, nets, nx, ny, blocks)`. Assert total overflow after is less than or equal to before on tiny_dr sequential L seed.

## Slide 5 — Pitfalls

Ripping a net but leaving ghost usage on its old tracks. Rerouting with pattern L through the same hot track. Picking the wrong net to rip—use overflow contribution not HPWL.

## Slide 6 — Your turn

Clear rip-up challenges. Next: tie it together with full sequential detailed routing.
""",
    "sequential-detailed": """# Sequential detailed route

**Module id:** module04-01-sequential-detailed
**Lab:** sequential-detailed
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Order matters on tracks

Production detailed routers process nets in an order. Each net deposits usage on directed tracks; later nets see a more congested grid. Sequential L-HV on tiny_dr is our baseline stress test; A* mode shows congestion-aware ordering effects.

## Slide 2 — The idea

Initialize empty usage. For each net in list order, compute terminals, route with the chosen mode—l_hv for layer L, lee for cell maze, astar for congestion-aware—and increment usage on every track key in the route. Report final usage and track_overflow summary.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **sequential-detailed**. Route all nets in default order. Reorder mentally: would routing the four-pin net last change the hottest track?

## Slide 4 — Implement track

Implement `sequential_detailed` and `route_from_data`. Print usage and overflow after routing all six nets. Compare astar mode with l_hv on total overflow.

## Slide 5 — Pitfalls

Parallel deposit without order— hides rip-up motivation. Ignoring multi-pin net in order list. Resetting usage between nets accidentally.

## Slide 6 — Your turn

Complete sequential detailed routing. Offline compare and wrap come next.
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

Work through EXAMPLES.md on tiny_dr.json.

## Slide 5 — Pitfalls

Watch track keys, capacity, vias, and deterministic goldens.

## Slide 6 — Your turn

Complete the checklist for at least one track.
""",
    )


def transcript_intro() -> str:
    return """# Welcome to detailed routing for EDA

**Module id:** module00-00-intro
**Lab:** none
**Tracks:** intro (dual-track welcome)

## Slide 1 — Detailed routing in the stack

You committed coarse paths in global routing. Detailed routing assigns tracks on M1 and M2, places vias, and chases DRC-clean geometry before compaction or signoff. This course teaches that grid, maze, A*, track usage, vias, spacing, and rip-up on a tiny chip.

## Slide 2 — Two tracks

Track B is the browser lab: route nets, watch track heat, inspect vias, clear challenges. Track A is implement: Python solvers on tiny_dr.json. Use either or both. Browser first for intuition is fine.

## Slide 3 — Course map

Foundations cover the routing grid and pin access. Algorithms cover Lee maze, A*, track usage, and via assignment. DRC and rip-up cover spacing lite and detailed rip-up. Sequential detailed ties the flow together. Offline compare and wrap close the path.

## Slide 4 — Prerequisites

Finish learn_global_routing so GCell graphs and edge usage deposits already make sense. Directed track usage is finer-grained—not the same keys as GCell edges.

## Slide 5 — How to move

Read each module README, pick a track, check the checklist, then skim the clip when media is available. Odd module slots leave room to insert algorithms later without renumbering.

## Slide 6 — Next

Open the routing grid graph and enumerate M1 and M2 tracks on the twelve-by-eight grid.
"""


def transcript_wrap() -> str:
    return """# Detailed routing path complete

**Module id:** module99-00-wrap
**Lab:** none
**Tracks:** recap · next course

## Slide 1 — You can now

You can build a track graph, assign pin access, route with Lee and A*, deposit track usage, assign vias on L paths, check spacing lite, rip up congested nets, and run sequential detailed routing on tiny_dr.

## Slide 2 — Dual-track recap

If you stayed in the browser, implement astar_route and track_overflow once in Python. If you stayed in Track A, skim the track heat-map lab so colors match your usage dict.

## Slide 3 — Pitfalls to remember

Directed track keys, layer-aware moves, sequential order effects, and never treating reveal golden as the solve path.

## Slide 4 — Next course

Natural next steps are learn_compaction for post-route cleanup—or learn_pattern_matching if you continue the PD spine toward lithography-friendly patterns.

## Slide 5 — Checklist

Name three algorithms and one strength each. Say which idea you reach for when sequential L overflows. Pick your next course README.

## Slide 6 — Close

When you are ready, take the short quiz, then open the next course.
"""


def transcript_offline() -> str:
    return """# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none
**Tracks:** offline harness

## Slide 1 — Why compare

Toy detailed routers need a harness: same JSON in, track overflow and runtime out. Comparing Lee, L-layer, A*, and rip-up teaches what better means beyond a pretty heat map.

## Slide 2 — The idea

Fix tiny_dr. Run sequential L-HV, Lee mode, A* mode, and one rip-up pass. Record total overflow, max overflow, wall time. Optionally compare to a reference router. Write one discrepancy hypothesis.

## Slide 3 — Harness shape

A small Python driver loading tiny_dr.json is enough. Print a markdown table. Missing external tools are OK—document blockers and still validate I/O.

## Slide 4 — Pitfalls

Changing track_capacity between rows. Comparing incompatible route modes without labeling. Optimizing runtime before correctness.

## Slide 5 — Your turn

Fill one comparison table for Lee versus A* versus rip-up. Then open the wrap.
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
    if m["kind"] == "lab" and m["lab"] in LAB_QUIZZES:
        return LAB_QUIZZES[m["lab"]]
    if m["kind"] == "intro":
        return [
            {
                "id": "intro-q1",
                "type": "mcq",
                "prompt": "Detailed routing typically sits…",
                "choices": [
                    "After global routing, before compaction or signoff polish",
                    "Before synthesis",
                    "Only inside SPICE",
                    "Instead of placement",
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
                "prompt": "Detailed routes deposit usage on…",
                "choices": [
                    "Directed M1/M2 track edges",
                    "Only cell widths",
                    "Scan flops",
                    "Liberty arcs",
                ],
                "answer": 0,
            },
        ]
    if m["kind"] == "wrap":
        return [
            {
                "id": "wrap-q1",
                "type": "mcq",
                "prompt": "A* routing penalizes tracks where…",
                "choices": [
                    "usage ≥ capacity",
                    "usage = 0",
                    "pins align",
                    "HPWL is minimal",
                ],
                "answer": 0,
            },
            {
                "id": "wrap-q2",
                "type": "mcq",
                "prompt": "A natural next course after detailed routing is…",
                "choices": [
                    "learn_compaction or learn_pattern_matching",
                    "learn_unix only",
                    "learn_spice first always",
                    "Skip to ML-EDA",
                ],
                "answer": 0,
            },
            {
                "id": "wrap-q3",
                "type": "mcq",
                "prompt": "Rip-up reroute picks the net with…",
                "choices": [
                    "Largest track overflow on its route",
                    "Shortest name",
                    "Fewest pins always",
                    "Random choice",
                ],
                "answer": 0,
            },
        ]
    return [
        {
            "id": "offline-q1",
            "type": "mcq",
            "prompt": "A fair router compare keeps constant…",
            "choices": ["Instance and track capacity", "Random Cap per row", "Different netlists silently", "Wall-clock only"],
            "answer": 0,
        },
        {
            "id": "offline-q2",
            "type": "mcq",
            "prompt": "Useful regression metrics include…",
            "choices": [
                "Total track overflow, max overflow, runtime",
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

- M1/M2 routing grid and pin access on a tiny chip (12×8)
- Lee maze routing around blockages (BFS on cells)
- A* detailed routing with track capacity penalties
- Track usage and overflow metrics (total, max, count)
- Two-layer via assignment on L-shaped paths
- DRC spacing lite (parallel same-layer distance)
- Rip-up and A* reroute on track usage
- Sequential detailed routing with ordered net deposit
- Offline compare harness on shared JSON

## Out of scope (v1)

- Production detailed routers / OpenROAD as the syllabus spine
- Full foundry DRC decks and antenna rules
- Vendor GUI certification
- Multi-cut via rules and advanced layer stacks

## Shared instance

`common/tiny_dr.json` — see `common/README.md`.
""",
    )
    write(
        ROOT / "docs" / "TWO_TRACKS.md",
        f"""# {COURSE_ID} — two tracks

| Track | Practice | Evidence |
|-------|----------|----------|
| **A — Implement** | `common/` solvers + per-module `examples/tiny_dr.json` | Track usage / overflow printouts, checklist |
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
| `01` | Foundations (routing grid, pin access) |
| `02` | Algorithms (Lee, A*, track usage, vias) |
| `03` | DRC spacing and rip-up |
| `04` | Sequential detailed route |
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
[![Domain](https://img.shields.io/badge/domain-detailed--routing-orange)](docs/MODULES.md)

**{COURSE_ID}** is the open learning path for *detailed routing on M1/M2 track grids* with Lee, A*, via assignment, DRC lite, and rip-up algorithms.

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
├── common/         # Track A: tiny_dr.json, solvers, tests
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

Prereq: [learn_global_routing](../learn_global_routing/README.md).  
Next: [learn_compaction](../learn_compaction/README.md) or [learn_pattern_matching](../learn_pattern_matching/README.md).  
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

Copyright (c) contributors to learn_routing / the learning monorepo.

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
    [[ -f "$ROOT/common/tiny_dr.json" ]] && echo "[OK] common/tiny_dr.json"
    python3 -c "import sys; sys.path.insert(0,'$ROOT/common'); from solvers import route_from_data; from drutil import load; d=load('$ROOT/common/tiny_dr.json'); u=route_from_data(d); print('[OK] solvers', len(u), 'tracks used')"
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
    src_merge = ROOT.parent / "learn_congestion" / "scripts" / "merge_browser_slides.py"
    if src_merge.is_file():
        shutil.copy2(src_merge, ROOT / "scripts" / "merge_browser_slides.py")


def write_common() -> None:
    write(
        ROOT / "common" / "README.md",
        f"""# common — {COURSE_ID}

## Starter instance

[`tiny_dr.json`](tiny_dr.json) — chip 12×8, grid 12×8, track capacity 1, layers M1/M2.
Cells A–F; six nets on spread placement; blockage at (5,2) size 2×2. Detailed routes deposit +1 usage per traversed directed track.

## Modules

- `drutil.py` — load, grid index, pin access, track keys, blockages
- `solvers.py` — Lee/A*, L-layer routes, track overflow, DRC lite, rip-up, sequential
- `test_solvers.py` — smoke goldens

Browser algorithms: `platform/tools/<lab-id>/` (when published).
""",
    )


def main() -> None:
    write_license()
    write_docs()
    write_modules_md()
    write_course_readme()
    write_common()
    write_scripts()
    tiny = tiny_dr_json()
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
            write(base / "examples" / "tiny_dr.json", tiny)
    print(f"Scaffolded {COURSE_ID}: {len(MODULES)} modules → {ROOT}")


if __name__ == "__main__":
    main()
