#!/usr/bin/env python3
"""Scaffold learn_global_routing (hierarchical SS-AA ids) with module-slides stubs."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "learn_global_routing"
LIVE_TOOLS = "https://universal-verification-methodology.github.io/learning/tools"

MODULES = [
    {
        "id": "module00-00-intro",
        "kind": "intro",
        "title": "Welcome to global routing for EDA",
        "short": "Welcome",
        "lab": None,
        "status": "—",
        "section": "00",
        "outcomes": "Explain why global routing sits after congestion estimation and before detailed routing.",
        "algorithm": None,
    },
    {
        "id": "module01-01-routing-graph",
        "kind": "lab",
        "title": "GCell routing graph",
        "short": "Routing graph",
        "lab": "routing-graph",
        "status": "**ref**",
        "section": "01",
        "outcomes": "Build the undirected GCell adjacency graph and list edges on a 4×2 grid.",
        "algorithm": "GCell routing graph (adjacent tile edges)",
    },
    {
        "id": "module01-03-terminal-gcells",
        "kind": "lab",
        "title": "Pin terminals on GCells",
        "short": "Terminals",
        "lab": "terminal-gcells",
        "status": "**ref**",
        "section": "01",
        "outcomes": "Map each pin placement to its owning GCell terminal for routing.",
        "algorithm": "pin terminal GCell assignment",
    },
    {
        "id": "module02-01-pattern-l-route",
        "kind": "lab",
        "title": "L-shape pattern routes",
        "short": "L-route",
        "lab": "pattern-l-route",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Route two-pin nets with horizontal-then-vertical or vertical-then-horizontal L paths.",
        "algorithm": "L-shape pattern routing (HV / VH)",
    },
    {
        "id": "module02-03-pattern-z-route",
        "kind": "lab",
        "title": "Z-shape pattern routes",
        "short": "Z-route",
        "lab": "pattern-z-route",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Route two-pin nets with a three-segment Z when possible; fall back to L otherwise.",
        "algorithm": "Z-shape pattern routing (HZ / VH bends)",
    },
    {
        "id": "module02-05-maze-gcell-route",
        "kind": "lab",
        "title": "Maze routing on GCells",
        "short": "Maze route",
        "lab": "maze-gcell-route",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Find a shortest GCell path with BFS while skipping edges at capacity.",
        "algorithm": "maze routing (BFS with edge capacity)",
    },
    {
        "id": "module02-07-multipin-tree",
        "kind": "lab",
        "title": "Multi-pin tree (Steiner-lite)",
        "short": "Multipin tree",
        "lab": "multipin-tree",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Connect multi-pin nets with a star from the bbox-center GCell via L legs.",
        "algorithm": "multipin star tree (bbox-center Steiner-lite)",
    },
    {
        "id": "module03-01-edge-overflow",
        "kind": "lab",
        "title": "Edge overflow metrics",
        "short": "Edge overflow",
        "lab": "edge-overflow",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Report total, max, and count of edge overflows from accumulated route usage.",
        "algorithm": "edge overflow metrics (total, max, count)",
    },
    {
        "id": "module03-03-ripup-reroute",
        "kind": "lab",
        "title": "Rip-up and reroute",
        "short": "Rip-up",
        "lab": "ripup-reroute",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Rip the hottest congested net and maze-reroute it to reduce edge overflow.",
        "algorithm": "rip-up and maze reroute",
    },
    {
        "id": "module04-01-sequential-global",
        "kind": "lab",
        "title": "Sequential global route",
        "short": "Sequential GR",
        "lab": "sequential-global",
        "status": "**ref**",
        "section": "04",
        "outcomes": "Route all nets in order with L patterns and measure resulting edge congestion.",
        "algorithm": "sequential global routing (ordered net deposit)",
    },
    {
        "id": "module05-01-offline-benchmark-compare",
        "kind": "offline",
        "title": "Offline benchmark compare",
        "short": "Offline compare",
        "lab": None,
        "status": "P",
        "section": "05",
        "outcomes": "Compare L, maze, and rip-up engines on shared instances (overflow, runtime, notes).",
        "algorithm": "benchmark harness vs reference global routes",
    },
    {
        "id": "module99-00-wrap",
        "kind": "wrap",
        "title": "Global routing path complete",
        "short": "Wrap",
        "lab": None,
        "status": "—",
        "section": "99",
        "outcomes": "Recap graph, patterns, overflow, rip-up; choose detailed routing or CTS next.",
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


def tiny_gr() -> dict:
    return {
        "chip": {"W": 12, "H": 8},
        "gcell": {"nx": 4, "ny": 2, "cellW": 3, "cellH": 4},
        "edge_capacity": 2,
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
        "notes": "4×2 GCells. Edges between adjacent GCells have capacity 2. Global route deposits usage on edges.",
    }


def tiny_gr_json() -> str:
    return json.dumps(tiny_gr(), indent=2) + "\n"


PSEUDO: dict[str, str] = {
    "routing-graph": """## Pseudocode

```text
Input: nx, ny GCell grid
edges ← empty list
for each GCell (i,j):
  if i+1 < nx: add undirected edge ((i,j),(i+1,j))
  if j+1 < ny: add undirected edge ((i,j),(i,j+1))
Output: edge list (11 edges on 4×2)
Golden: horizontal edges along row 0 include ((0,0),(1,0))
```
""",
    "terminal-gcells": """## Pseudocode

```text
Input: placement pin (x,y), gcell nx×ny, cellW, cellH
(i,j) ← cell_gcell(x,y)   # clamp floor divide
terminals[cell_id] ← (i,j)
Output: map cell → GCell terminal
Golden: A at (1,1) → (0,0); D at (8,5) → (2,1)
```
""",
    "pattern-l-route": """## Pseudocode

```text
Input: terminals a=(i0,j0), b=(i1,j1), prefer HV or VH
path ← [a]
if HV: walk horizontal to (i1,j0), then vertical to b
if VH: walk vertical to (i0,j1), then horizontal to b
Output: GCell path; edges = consecutive pairs
Golden: (0,0)→(2,1) HV uses 3 edges
```
""",
    "pattern-z-route": """## Pseudocode

```text
Input: a, b, prefer HZ or VH (vertical-first Z)
if a and b share row or column: fall back to L-route
HZ: horizontal to mid column, vertical, horizontal to b
Output: 3-segment Z path when off-axis
Golden: (0,0)→(3,1) Z uses ≥3 edges, ≠ L path
```
""",
    "maze-gcell-route": """## Pseudocode

```text
Input: start, goal, edge usage, capacity Cap
BFS queue ← (start, [start])
while queue not empty:
  pop (cur, path)
  for each neighbor nb of cur:
    edge ← (cur, nb)
    if usage[edge] ≥ Cap: skip   # congested edge
    if nb == goal: return path + [nb]
    enqueue (nb, path + [nb])
Output: shortest feasible path or None
```
""",
    "multipin-tree": """## Pseudocode

```text
Input: pin GCells pins[]
center ← bbox-center GCell of pins
for each pin p in pins:
  add L-route(center, p, HV) edges to tree
Output: union of L legs (Steiner-lite star)
Golden: 4-corner pins share hub near (1,0)
```
""",
    "edge-overflow": """## Pseudocode

```text
Input: edge usage map, capacity Cap
for each edge e:
  ov[e] ← max(0, usage[e] − Cap)
total ← sum(ov);  max ← max(ov);  count ← #{ov>0}
Output: {total, max, count, perEdge}
```
""",
    "ripup-reroute": """## Pseudocode

```text
Input: routes per net, usage, Cap
worst ← net with largest overflow on its edges
subtract worst's edges from usage
newPath ← maze_route(worst pins, usage, Cap) or alternate L
add newPath edges to usage
Output: updated usage with lower total overflow
```
""",
    "sequential-global": """## Pseudocode

```text
Input: ordered nets[], terminals, mode (l_hv), Cap
usage ← empty
for each net N in order:
  route N with pattern/maze respecting current usage
  deposit +1 on each edge of the route
Output: final usage; sequential L-HV should overflow at Cap=2
```
""",
}


LAB_QUIZZES: dict[str, list] = {
    "routing-graph": [
        {
            "id": "routing-graph-q1",
            "type": "mcq",
            "prompt": "A GCell routing graph connects…",
            "choices": [
                "Horizontally and vertically adjacent GCells",
                "Only diagonal GCell corners",
                "Liberty timing arcs",
                "Scan chain flops",
            ],
            "answer": 0,
        },
        {
            "id": "routing-graph-q2",
            "type": "mcq",
            "prompt": "On a 4×2 GCell grid the undirected edge count is…",
            "choices": ["11", "8", "16", "24"],
            "answer": 0,
        },
        {
            "id": "routing-graph-q3",
            "type": "mcq",
            "prompt": "Global routes deposit demand on…",
            "choices": ["GCell edges", "Standard cells only", "Clock pins", "Power straps only"],
            "answer": 0,
        },
    ],
    "terminal-gcells": [
        {
            "id": "terminal-gcells-q1",
            "type": "mcq",
            "prompt": "Pin terminal assignment maps a pin to…",
            "choices": [
                "The GCell containing the pin center",
                "The farthest GCell on the chip",
                "A Liberty arc",
                "A detailed-route via",
            ],
            "answer": 0,
        },
        {
            "id": "terminal-gcells-q2",
            "type": "mcq",
            "prompt": "Cell A at (1,1) on our 4×2 grid lands in GCell…",
            "choices": ["(0,0)", "(2,1)", "(3,1)", "(1,1)"],
            "answer": 0,
        },
        {
            "id": "terminal-gcells-q3",
            "type": "mcq",
            "prompt": "Terminals are needed before…",
            "choices": [
                "Any pattern or maze route between pins",
                "Synthesis only",
                "DRC at foundry signoff only",
                "Scan insertion",
            ],
            "answer": 0,
        },
    ],
    "pattern-l-route": [
        {
            "id": "pattern-l-route-q1",
            "type": "mcq",
            "prompt": "An L-route with prefer=HV goes…",
            "choices": [
                "Horizontal first, then vertical",
                "Vertical first, then horizontal",
                "Diagonal only",
                "Random zigzag",
            ],
            "answer": 0,
        },
        {
            "id": "pattern-l-route-q2",
            "type": "mcq",
            "prompt": "Two-pin L routing is a…",
            "choices": [
                "Fast pattern router baseline",
                "Detailed DRC engine",
                "CTS solver",
                "Power-grid placer",
            ],
            "answer": 0,
        },
        {
            "id": "pattern-l-route-q3",
            "type": "mcq",
            "prompt": "path_to_edges on an L path returns…",
            "choices": [
                "One edge per consecutive GCell step",
                "Only the first GCell",
                "All nets in the design",
                "Layer assignments",
            ],
            "answer": 0,
        },
    ],
    "pattern-z-route": [
        {
            "id": "pattern-z-route-q1",
            "type": "mcq",
            "prompt": "A Z-route uses…",
            "choices": [
                "Three segments when pins are off the same row and column",
                "Exactly one edge always",
                "Only vias",
                "No bends",
            ],
            "answer": 0,
        },
        {
            "id": "pattern-z-route-q2",
            "type": "mcq",
            "prompt": "When a and b share a row, Z-route…",
            "choices": ["Falls back to L-route", "Returns empty", "Uses maze only", "Fails DRC"],
            "answer": 0,
        },
        {
            "id": "pattern-z-route-q3",
            "type": "mcq",
            "prompt": "HZ prefer means the first segment is…",
            "choices": ["Horizontal", "Vertical", "Diagonal", "Via-only"],
            "answer": 0,
        },
    ],
    "maze-gcell-route": [
        {
            "id": "maze-gcell-route-q1",
            "type": "mcq",
            "prompt": "Maze routing skips edges where…",
            "choices": ["usage ≥ capacity", "usage = 0", "pins coincide", "HPWL = 0"],
            "answer": 0,
        },
        {
            "id": "maze-gcell-route-q2",
            "type": "mcq",
            "prompt": "Our maze router uses…",
            "choices": ["BFS for shortest feasible path", "DFS only", "Simulated annealing", "SPICE"],
            "answer": 0,
        },
        {
            "id": "maze-gcell-route-q3",
            "type": "mcq",
            "prompt": "If all paths are blocked, maze_route returns…",
            "choices": ["None", "A random path", "Negative overflow", "A via stack"],
            "answer": 0,
        },
    ],
    "multipin-tree": [
        {
            "id": "multipin-tree-q1",
            "type": "mcq",
            "prompt": "Our Steiner-lite star hubs at…",
            "choices": [
                "Bbox-center GCell of the pins",
                "Chip lower-left corner always",
                "Random tile",
                "Power pad",
            ],
            "answer": 0,
        },
        {
            "id": "multipin-tree-q2",
            "type": "mcq",
            "prompt": "Each pin connects to the hub with…",
            "choices": ["An L-route leg", "A separate chip exit", "Only a via", "No edges"],
            "answer": 0,
        },
        {
            "id": "multipin-tree-q3",
            "type": "mcq",
            "prompt": "The four-pin net A–B–C–D uses…",
            "choices": [
                "Multipin star, not pairwise maze",
                "Only one two-pin L",
                "Clock-tree buffering",
                "Abacus packing",
            ],
            "answer": 0,
        },
    ],
    "edge-overflow": [
        {
            "id": "edge-overflow-q1",
            "type": "mcq",
            "prompt": "Edge overflow on one edge is…",
            "choices": ["max(0, usage − capacity)", "usage × capacity", "HPWL only", "Always zero"],
            "answer": 0,
        },
        {
            "id": "edge-overflow-q2",
            "type": "mcq",
            "prompt": "Sequential L-routes at Cap=2 on tiny_gr should…",
            "choices": [
                "Produce positive total overflow",
                "Always be zero overflow",
                "Skip edge counting",
                "Only count vias",
            ],
            "answer": 0,
        },
        {
            "id": "edge-overflow-q3",
            "type": "mcq",
            "prompt": "Overflow count reports…",
            "choices": [
                "How many edges exceed capacity",
                "Number of cells",
                "Git commits",
                "Clock skew",
            ],
            "answer": 0,
        },
    ],
    "ripup-reroute": [
        {
            "id": "ripup-reroute-q1",
            "type": "mcq",
            "prompt": "Rip-up picks the net with…",
            "choices": [
                "Largest overflow contribution on its edges",
                "Shortest HPWL always",
                "Lowest pin count always",
                "Random selection",
            ],
            "answer": 0,
        },
        {
            "id": "ripup-reroute-q2",
            "type": "mcq",
            "prompt": "After rip-up we reroute with…",
            "choices": ["Maze respecting remaining usage", "Same L blindly", "Delete the net", "Inflate cells"],
            "answer": 0,
        },
        {
            "id": "ripup-reroute-q3",
            "type": "mcq",
            "prompt": "Rip-up should…",
            "choices": [
                "Not increase total overflow vs before (ideal)",
                "Always zero all overflow",
                "Skip usage accounting",
                "Only run in detailed route",
            ],
            "answer": 0,
        },
    ],
    "sequential-global": [
        {
            "id": "sequential-global-q1",
            "type": "mcq",
            "prompt": "Sequential global routing processes nets…",
            "choices": [
                "In a fixed order, depositing on shared edges",
                "All in parallel with no sharing",
                "Only after CTS",
                "Before placement",
            ],
            "answer": 0,
        },
        {
            "id": "sequential-global-q2",
            "type": "mcq",
            "prompt": "route_nets mode l_hv means…",
            "choices": [
                "L-route each two-pin net horizontal-then-vertical",
                "Z-route only",
                "Skip multi-pin nets",
                "Maze every net first",
            ],
            "answer": 0,
        },
        {
            "id": "sequential-global-q3",
            "type": "mcq",
            "prompt": "Order sensitivity means…",
            "choices": [
                "Later nets see congested edges from earlier nets",
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

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **{m['algorithm']}** on `examples/tiny_gr.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with edge usage and overflow when relevant.
3. Optional self-check: `./scripts/module.sh {key} --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/{lab}/](http://127.0.0.1:8080/tools/{lab}/)
2. Live: [{LIVE_TOOLS}/{lab}/]({LIVE_TOOLS}/{lab}/)
3. Tools shelf: open `{lab}` from the platform tools index
4. Load the **starter global routing** instance, run the router, inspect edge overflow.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach global routing literacy on a tiny GCell graph — not production detailed routers.
"""
    elif m["kind"] == "offline":
        body = f"""
## Outcomes

After this module you can: **{m['outcomes']}**

## Offline track

1. Follow [EXAMPLES.md](EXAMPLES.md) to run the local compare harness.
2. Record edge overflow totals and runtime against at least one reference when available.
3. Complete [CHECKLIST.md](CHECKLIST.md).
"""
    elif m["kind"] == "intro":
        body = """
## What this course is

**learn_global_routing** teaches *coarse global routing on GCell graphs* using **two learning modes** on every lab module:

| Track | Where you practice | Best for |
|-------|--------------------|----------|
| **A — Implement** | Tiny GCell instance + `EXAMPLES.md` / `examples/` | Fidelity: patterns, maze, overflow |
| **B — Browser lab** | Interactive lab on the learning platform | Concept literacy, quick visual feedback |

You can do **A only**, **B only**, or **both** (recommended: B for intuition when shipped, then A for fidelity).

**Prerequisite:** [learn_congestion](../learn_congestion/README.md) / [learn_legalization](../learn_legalization/README.md) — you need GCell literacy and a placed netlist.

## Setup (Track A)

1. Open this course under `courses/learn_global_routing/`.
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

- Build a GCell routing graph and assign pin terminals
- Route with L, Z, maze, and multipin star patterns
- Measure edge overflow and rip-up congested nets
- Run sequential global routing on the tiny instance

## Dual-track recap

If you mainly used **browser labs**, spend a short session on Track A for maze and overflow metrics.
If you mainly used **Track A**, skim any skipped shipped browser labs for visual edge heat maps.

## Next course

Prereqs done: **learn_congestion** / **learn_legalization**.

→ **learn_routing** or **learn_clock_tree** (see parent [`eda.md`](../../../eda.md))

## Checklist

- [ ] I completed Track A and/or Track B for the lab modules I care about
- [ ] I can explain L vs maze vs rip-up in my own words
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
- [ ] Implemented **{m['algorithm']}** end-to-end on `examples/tiny_gr.json`
- [ ] Reported edge usage / overflow when relevant
- [ ] Can explain the algorithm without the UI

## Track B — Browser lab (`{m['lab']}`)

- [ ] Opened the lab (local or live)
- [ ] Loaded the starter global routing instance
- [ ] Ran the router and inspected edge overflow metrics

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

- [ ] I can explain how to judge global routing quality across engines
"""
    if m["kind"] == "intro":
        return f"""# Checklist — {m['title']}

- [ ] I understand the course map (sections 01–05 + wrap)
- [ ] I know Track A (implement) vs Track B (browser lab)
- [ ] I opened [docs/MODULES.md](../docs/MODULES.md) once
- [ ] I finished learn_congestion / learn_legalization or know why global route follows them
- [ ] Ready for the GCell routing graph
"""
    return f"""# Checklist — {m['title']}

- [ ] I can name the main global routing ideas from sections 01–04
- [ ] I know when L vs maze vs rip-up fits
- [ ] I picked a next course (`learn_routing` or `learn_clock_tree`)
"""


def examples(m: dict) -> str:
    if m["kind"] == "lab":
        lab = m["lab"]
        pseudo = PSEUDO.get(lab, "## Pseudocode\n\n```text\n(see common/solvers.py)\n```\n")
        return f"""# Examples — {m['title']}

Track A (implement). Use the tiny global routing instance first (`examples/tiny_gr.json`).

## Algorithm

**{m['algorithm']}**

{pseudo}

## Track A API

```bash
# from courses/learn_global_routing/
python3 -c "from common.solvers import route_from_data; from common.grutil import load; d=load('common/tiny_gr.json'); print(route_from_data(d))"
```

Prefer helpers in `common/grutil.py` and `common/solvers.py` over ad-hoc scripts.

## Starter prompts

1. Load `placement` and `nets` from `tiny_gr.json`; print the 4×2 GCell layout and edge count.
2. Run the algorithm for this lab; print edge usage or overflow with two decimals.
3. Compare sequential L-HV vs maze on total edge overflow.
4. Change edge_capacity from 2 to 1 and report which edges flip congested.
5. Write one sentence: why this idea belongs before detailed routing.

## Expected artifacts

- Edge usage map or path listing for the lab algorithm
- Overflow summary (total, max, count) when relevant
- Short note tying the metric to rip-up or sequential order
"""
    if m["kind"] == "offline":
        return """# Examples — Offline benchmark compare

1. Export the same tiny_gr instance used in sequential / overflow labs.
2. Run L-HV, maze, and one rip-up pass; record total edge overflow and wall time.
3. If available, compare against a reference global route.
4. Fill a comparison table: quality, overflow, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
"""
    if m["kind"] == "intro":
        return """# Examples — Welcome

No coding yet.

1. Sketch the PD path: place → legalize → congestion → **global route** → detailed route / CTS.
2. Write one sentence: “Global routing exists because …”
3. Name one difference between GCell demand maps (congestion) and edge usage (global route).
"""
    return """# Examples — Wrap

1. List three global routing algorithms from this course and one strength each.
2. For a congested sequential L pass, which module’s idea do you reach for first?
3. Write the bridge sentence you’ll need for detailed routing next.
"""


LAB_TRANSCRIPTS: dict[str, str] = {
    "routing-graph": """# GCell routing graph

**Module id:** module01-01-routing-graph
**Lab:** routing-graph
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Why a routing graph

Global routers do not hop pixel by pixel. They walk a coarse graph whose nodes are GCells and whose edges are the channels between neighbors. Before any pattern route, you must enumerate those edges on our four-by-two toy grid.

## Slide 2 — The idea

For each GCell at column i and row j, add an undirected edge to the right neighbor when i plus one is less than nx, and to the upper neighbor when j plus one is less than ny. On four by two you get eleven edges. Store each edge as a sorted pair of GCell indices so direction does not matter.

## Slide 3 — Browser lab track

Open the **routing-graph** lab. Toggle grid lines and highlight one horizontal edge between columns zero and one. Read the edge list in the metrics panel. Match the count to eleven.

## Slide 4 — Implement track

Implement `edge_list(nx, ny)` in `common/grutil.py`. Print all edges for the tiny instance. Verify ((0,0),(1,0)) is present and diagonals are absent.

## Slide 5 — Pitfalls

Counting tile interiors instead of adjacency channels. Double-counting undirected edges as two directed arcs without collapsing. Forgetting top and right boundary checks.

## Slide 6 — Your turn

Finish the checklist. Sketch the eleven edges from memory. Next: map pin placements to terminal GCells.
""",
    "terminal-gcells": """# Pin terminals on GCells

**Module id:** module01-03-terminal-gcells
**Lab:** terminal-gcells
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Pins become terminals

A global route starts and ends at GCell terminals—one tile per pin. Legal placement gives you x y coordinates; this module converts them to grid indices using the same floor-and-clamp rule as congestion GCells.

## Slide 2 — The idea

cell_gcell of x y returns column i equals floor of x over cell width clamped, and row j likewise. Cell A at one comma one maps to zero comma zero. Cell D at eight comma five maps to two comma one. Build a dictionary from cell id to GCell for every pin in the netlist.

## Slide 3 — Browser lab track

Open **terminal-gcells**. Hover each cell and read its terminal GCell. Move a pin across a boundary and watch the terminal index flip. Confirm the six cells on tiny_gr match your Track A printout.

## Slide 4 — Implement track

Implement `terminals(positions, data)` returning the map. Assert A through F on spread placement. Print terminals before any routing lab.

## Slide 5 — Pitfalls

Using cell origin instead of pin center. Off-by-one at the right or top chip edge without clamp. Mixing site columns from legalization with GCell columns.

## Slide 6 — Your turn

Complete terminals for all six cells. Next: L-shape pattern routes between two terminals.
""",
    "pattern-l-route": """# L-shape pattern routes

**Module id:** module02-01-pattern-l-route
**Lab:** pattern-l-route
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — The simplest global path

Two-pin global routing often starts with an L: travel along one axis, then the other. It is fast, deterministic, and good enough to teach edge usage before maze search or rip-up.

## Slide 2 — The idea

Given terminals a and b, prefer HV walks horizontal to align columns then vertical to the row; prefer VH swaps the order. Emit the list of GCells visited and convert consecutive pairs to edges with path_to_edges. A path from zero comma zero to two comma one in HV uses three edges.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **pattern-l-route**. Route A to B with HV and read the highlighted edges. Toggle VH on the same pair and compare the bend GCell.

## Slide 4 — Implement track

Implement `l_route(a, b, prefer)` and `path_to_edges`. Route net A–B on tiny_gr and print the edge list. Match the browser overlay.

## Slide 5 — Pitfalls

Skipping duplicate GCells at the bend. Returning directed edges inconsistently—always normalize undirected keys. Forgetting that L routes ignore existing congestion until sequential routing.

## Slide 6 — Your turn

Ship Track A L-routes and clear browser challenges. Next: Z-shape patterns when you want a third segment.
""",
    "pattern-z-route": """# Z-shape pattern routes

**Module id:** module02-03-pattern-z-route
**Lab:** pattern-z-route
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Three segments

When pins are not on the same row or column, an L is not your only pattern. A Z bends twice: horizontal to a midpoint column, vertical, then horizontal to the destination—or the vertical-first variant.

## Slide 2 — The idea

If a and b share a row or column, fall back to L-route. Otherwise with prefer HZ pick mid column as the average of the two columns, walk H–V–H. path_to_edges should show at least three edges for off-axis pairs like zero comma zero to three comma one.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **pattern-z-route**. Compare Z versus L on B to D. Note the extra bend GCell and how edge usage shifts.

## Slide 4 — Implement track

Implement `z_route(a, b, prefer)`. Print Z and L paths for the same terminal pair; explain one edge difference.

## Slide 5 — Pitfalls

Using a midpoint that leaves zero-length segments. Not falling back to L on aligned pins. Confusing Z prefer HZ with L prefer HV naming.

## Slide 6 — Your turn

Finish Z routing on two-pin nets. Next: maze routing that respects congested edges.
""",
    "maze-gcell-route": """# Maze routing on GCells

**Module id:** module02-05-maze-gcell-route
**Lab:** maze-gcell-route
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Routes that detour

Pattern routers ignore blocked channels. Maze routing runs BFS on the GCell graph, skipping any edge whose usage is already at capacity. That is how global routers find alternate corridors.

## Slide 2 — The idea

Seed a queue with start and path list. Pop, expand neighbors, skip edges with usage greater than or equal to capacity. First time you dequeue the goal, return the path. If the queue empties, return None. Shortest feasible path wins.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **maze-gcell-route**. Pre-fill an edge to capacity two and watch maze pick a longer detour. Clear the block and confirm the shortest path returns.

## Slide 4 — Implement track

Implement `maze_route(a, b, usage, capacity, nx, ny)`. Block edge ((0,0),(1,0)) at cap two and show maze cannot go direct; unblock a vertical detour path exists.

## Slide 5 — Pitfalls

Treating usage as per-tile instead of per-edge. Forgetting BFS needs visited set on GCells not edges. Returning a path through a full edge because you checked the wrong direction key.

## Slide 6 — Your turn

Pass maze goldens. Next: connect more than two pins with a star tree.
""",
    "multipin-tree": """# Multi-pin tree (Steiner-lite)

**Module id:** module02-07-multipin-tree
**Lab:** multipin-tree
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — More than two pins

Real nets have many pins. A full Steiner tree is heavy; our Steiner-lite star picks the bbox-center GCell as a hub and L-routes each pin to that hub. Good enough to teach shared edge usage on the four-pin net A B C D.

## Slide 2 — The idea

Collect terminal GCells for the net. Center is the integer average of min and max column and row. For each pin, add the edges along l_route center to pin with HV unless you choose VH. Union all legs—edges shared by two legs count once in usage when you deposit.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **multipin-tree**. Route the four-pin net and highlight the hub near column one row zero. Compare total edges to four separate two-pin L routes.

## Slide 4 — Implement track

Implement `multipin_star` and `multipin_star_edges`. Route net index four on tiny_gr and print hub GCell plus edge count.

## Slide 5 — Pitfalls

Routing pairwise between every pin pair— that explodes edges. Picking chip center instead of bbox center GCell. Double-depositing the same edge when summing legs—usage should increment per net once per edge traversed.

## Slide 6 — Your turn

Complete multipin routing. Next: quantify overflow on those shared edges.
""",
    "edge-overflow": """# Edge overflow metrics

**Module id:** module03-01-edge-overflow
**Lab:** edge-overflow
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — When usage exceeds capacity

Each GCell edge has capacity two on tiny_gr. Every routed net deposits plus one on each edge it uses. Overflow is how far usage exceeds capacity—summed, maxed, and counted per edge.

## Slide 2 — The idea

For each edge e, overflow e equals max of zero and usage e minus capacity. Total is the sum across edges. Max is the worst edge. Count is how many edges have positive overflow. Sequential L-HV on all six nets should yield positive total overflow at cap two.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **edge-overflow**. Run sequential L routes and read the triple total max count. Heat-map the worst edge.

## Slide 4 — Implement track

Implement `edge_overflow(usage, capacity)`. Call route_nets with mode l_hv on tiny_gr and assert total overflow is greater than zero.

## Slide 5 — Pitfalls

Computing overflow before summing all nets. Using tile demand from congestion instead of edge usage. Reporting negative overflow values.

## Slide 6 — Your turn

Hit overflow targets. Next: rip-up the hottest net and maze reroute.
""",
    "ripup-reroute": """# Rip-up and reroute

**Module id:** module03-03-ripup-reroute
**Lab:** ripup-reroute
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Relieve hotspots

When overflow appears, global routers rip up contributing nets and reroute around congested edges. Our toy pass picks the net whose edges contribute the most overflow, removes its usage, then maze-reroutes.

## Slide 2 — The idea

Score each net by overflow on its edges. Subtract its route from usage. Run maze_route between its pins with the remaining usage map. Add the new edges back. Total overflow should not rise; ideally it drops versus the pre-rip state.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **ripup-reroute**. Run sequential L to create overflow, then one rip-up pass. Watch total overflow fall on the metrics panel.

## Slide 4 — Implement track

Implement `ripup_reroute(routes, usage, capacity, nets, term, nx, ny)`. Assert total overflow after is less than or equal to before on tiny_gr sequential L seed.

## Slide 5 — Pitfalls

Ripping a net but leaving ghost usage on its old edges. Rerouting with pattern L through the same hot edge. Picking the wrong net to rip—use overflow contribution not HPWL.

## Slide 6 — Your turn

Clear rip-up challenges. Next: tie it together with full sequential global routing.
""",
    "sequential-global": """# Sequential global route

**Module id:** module04-01-sequential-global
**Lab:** sequential-global
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Order matters

Production global routers process nets in an order. Each net deposits usage on edges; later nets see a more congested graph. Sequential L-HV on tiny_gr is our baseline stress test.

## Slide 2 — The idea

Initialize empty usage. For each net in list order, compute terminals, route with the chosen mode—l_hv for two-pin L, star for multi-pin—and increment usage on every edge in the route. Report final usage and edge_overflow summary.

## Slide 3 — Browser lab track

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

Open **sequential-global**. Route all nets in default order. Reorder mentally: would routing the four-pin net last change the hottest edge?

## Slide 4 — Implement track

Implement `route_nets` and `route_nets_with_routes`. Print usage and overflow after routing all six nets. Compare with maze mode on total overflow.

## Slide 5 — Pitfalls

Parallel deposit without order— hides rip-up motivation. Ignoring multi-pin net in order list. Resetting usage between nets accidentally.

## Slide 6 — Your turn

Complete sequential global routing. Offline compare and wrap come next.
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

Work through EXAMPLES.md on tiny_gr.json.

## Slide 5 — Pitfalls

Watch edge keys, capacity, and deterministic goldens.

## Slide 6 — Your turn

Complete the checklist for at least one track.
""",
    )


def transcript_intro() -> str:
    return """# Welcome to global routing for EDA

**Module id:** module00-00-intro
**Lab:** none
**Tracks:** intro (dual-track welcome)

## Slide 1 — Global routing in the stack

You estimated congestion on GCells. Global routing commits coarse paths on the GCell graph, depositing usage on edges before detailed routing or CTS. This course teaches that graph, pattern routers, overflow, and rip-up on a tiny chip.

## Slide 2 — Two tracks

Track B is the browser lab: route nets, watch edge heat, clear challenges. Track A is implement: Python solvers on tiny_gr.json. Use either or both. Browser first for intuition is fine.

## Slide 3 — Course map

Foundations cover the routing graph and terminals. Patterns cover L, Z, maze, and multipin star. Congestion response covers edge overflow and rip-up. Sequential global ties the flow together. Offline compare and wrap close the path.

## Slide 4 — Prerequisites

Finish learn_congestion or learn_legalization so GCell indexing and placed netlists already make sense. Congestion demand maps are cousins—not the same as edge usage deposits.

## Slide 5 — How to move

Read each module README, pick a track, check the checklist, then skim the clip when media is available. Odd module slots leave room to insert algorithms later without renumbering.

## Slide 6 — Next

Open the GCell routing graph and enumerate eleven edges on the four-by-two grid.
"""


def transcript_wrap() -> str:
    return """# Global routing path complete

**Module id:** module99-00-wrap
**Lab:** none
**Tracks:** recap · next course

## Slide 1 — You can now

You can build a routing graph, assign terminals, route with L Z maze and star patterns, measure edge overflow, rip up congested nets, and run sequential global routing on tiny_gr.

## Slide 2 — Dual-track recap

If you stayed in the browser, implement maze_route and edge_overflow once in Python. If you stayed in Track A, skim the edge heat-map lab so colors match your usage dict.

## Slide 3 — Pitfalls to remember

Undirected edge keys, sequential order effects, and never treating reveal golden as the solve path.

## Slide 4 — Next course

Natural next steps are learn_routing for detailed routes—or learn_clock_tree if you continue the PD spine toward CTS.

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

Toy global routers need a harness: same JSON in, edge overflow and runtime out. Comparing L, maze, and rip-up teaches what better means beyond a pretty heat map.

## Slide 2 — The idea

Fix tiny_gr. Run sequential L-HV, maze mode, and one rip-up pass. Record total overflow, max overflow, wall time. Optionally compare to a reference router. Write one discrepancy hypothesis.

## Slide 3 — Harness shape

A small Python driver loading tiny_gr.json is enough. Print a markdown table. Missing external tools are OK—document blockers and still validate I/O.

## Slide 4 — Pitfalls

Changing edge_capacity between rows. Comparing incompatible route modes without labeling. Optimizing runtime before correctness.

## Slide 5 — Your turn

Fill one comparison table for L versus maze versus rip-up. Then open the wrap.
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
                "prompt": "Global routing typically sits…",
                "choices": [
                    "After congestion estimate, before detailed routing",
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
                "prompt": "Global routes deposit usage on…",
                "choices": [
                    "GCell graph edges",
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
                "prompt": "Maze routing avoids edges where…",
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
                "prompt": "A natural next course after global routing is…",
                "choices": [
                    "learn_routing or learn_clock_tree",
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
                    "Largest overflow on its edges",
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
            "choices": ["Instance and edge capacity", "Random Cap per row", "Different netlists silently", "Wall-clock only"],
            "answer": 0,
        },
        {
            "id": "offline-q2",
            "type": "mcq",
            "prompt": "Useful regression metrics include…",
            "choices": [
                "Total edge overflow, max overflow, runtime",
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

- GCell routing graph and pin terminals on a tiny chip (4×2 over 12×8)
- L-shape and Z-shape pattern routing
- Maze routing with edge capacity (BFS)
- Multipin star tree (Steiner-lite)
- Edge overflow metrics (total, max, count)
- Rip-up and maze reroute
- Sequential global routing with ordered net deposit
- Offline compare harness on shared JSON

## Out of scope (v1)

- Production global routers / OpenROAD as the syllabus spine
- Layer assignment, via rules, and detailed DRC (see `learn_routing`)
- Vendor GUI certification
- Foundry PDK edge capacity tables

## Shared instance

`common/tiny_gr.json` — see `common/README.md`.
""",
    )
    write(
        ROOT / "docs" / "TWO_TRACKS.md",
        f"""# {COURSE_ID} — two tracks

| Track | Practice | Evidence |
|-------|----------|----------|
| **A — Implement** | `common/` solvers + per-module `examples/tiny_gr.json` | Edge usage / overflow printouts, checklist |
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
| `01` | Foundations (routing graph, terminals) |
| `02` | Pattern routing (L, Z, maze, multipin) |
| `03` | Overflow and rip-up |
| `04` | Sequential global route |
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
[![Domain](https://img.shields.io/badge/domain-global--routing-orange)](docs/MODULES.md)

**{COURSE_ID}** is the open learning path for *global routing on GCell graphs* with pattern, maze, and rip-up algorithms.

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
├── common/         # Track A: tiny_gr.json, solvers, tests
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

Prereq: [learn_congestion](../learn_congestion/README.md) / [learn_legalization](../learn_legalization/README.md).  
Next: [learn_routing](../learn_routing/README.md) or [learn_clock_tree](../learn_clock_tree/README.md).  
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

Copyright (c) contributors to learn_global_routing / the learning monorepo.

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
    [[ -f "$ROOT/common/tiny_gr.json" ]] && echo "[OK] common/tiny_gr.json"
    python3 -c "import sys; sys.path.insert(0,'$ROOT/common'); from solvers import route_from_data; from grutil import load; d=load('$ROOT/common/tiny_gr.json'); u=route_from_data(d); print('[OK] solvers', len(u), 'edges used')"
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
    write(ROOT / "common" / "tiny_gr.json", tiny_gr_json())
    write(
        ROOT / "common" / "README.md",
        f"""# common — {COURSE_ID}

## Starter instance

[`tiny_gr.json`](tiny_gr.json) — chip 12×8, GCells 4×2 (cell 3×4), edge capacity 2.
Cells A–F; six nets on spread placement. Global routes deposit +1 usage per traversed edge.

## Modules

- `grutil.py` — load, GCell index, edge list, terminals
- `solvers.py` — L/Z/maze/star, route_nets, overflow, rip-up
- `test_solvers.py` — smoke goldens

Browser algorithms: `platform/tools/<lab-id>/` (when published).
""",
    )
    # grutil.py, solvers.py, test_solvers.py written by scaffold from templates below
    write(ROOT / "common" / "__init__.py", f'"""{COURSE_ID} Track A package."""\n')
    common_dir = ROOT / "common"
    for name in ("grutil.py", "solvers.py", "test_solvers.py"):
        src = common_dir / name
        if not src.is_file():
            raise FileNotFoundError(f"Expected {src} — create before running scaffold or embed in write_common")


def main() -> None:
    write_license()
    write_docs()
    write_modules_md()
    write_course_readme()
    write_common()
    write_scripts()
    tiny = tiny_gr_json()
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
            write(base / "examples" / "tiny_gr.json", tiny)
    print(f"Scaffolded {COURSE_ID}: {len(MODULES)} modules → {ROOT}")


if __name__ == "__main__":
    main()
