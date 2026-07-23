#!/usr/bin/env python3
"""Scaffold learn_floorplanning modules (hierarchical SS-AA ids) with module-slides stubs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "learn_floorplanning"
LIVE_TOOLS = "https://universal-verification-methodology.github.io/learning/tools"

MODULES = [
    {
        "id": "module00-00-intro",
        "kind": "intro",
        "title": "Welcome to floorplanning for EDA",
        "short": "Welcome",
        "lab": None,
        "status": "—",
        "section": "00",
        "outcomes": "Explain why fixed-outline floorplanning sits between partitioning and placement, and how this course is organized.",
        "algorithm": None,
    },
    {
        "id": "module01-01-fixed-outline",
        "kind": "lab",
        "title": "Fixed-outline constraints",
        "short": "Fixed outline",
        "lab": "fixed-outline",
        "status": "**ref**",
        "section": "01",
        "outcomes": "State a W×H chip outline, pack modules, and decide whether a packing is legal (inside outline, no overlap).",
        "algorithm": "fixed-outline legality check (containment + non-overlap)",
    },
    {
        "id": "module01-03-area-deadspace",
        "kind": "lab",
        "title": "Area, packing density, whitespace/deadspace",
        "short": "Area & deadspace",
        "lab": "area-deadspace",
        "status": "**ref**",
        "section": "01",
        "outcomes": "Compute outline area, sum of module areas, packing density, and deadspace = outlineArea − Σ module areas.",
        "algorithm": "area / density / deadspace metrics on a packing",
    },
    {
        "id": "module02-01-slicing-floorplan",
        "kind": "lab",
        "title": "Slicing tree / polish expression packing",
        "short": "Slicing",
        "lab": "slicing-floorplan",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Encode a slicing floorplan as an H/V slicing tree or polish expression and pack rectangles from it.",
        "algorithm": "slicing tree / polish expression packing (H and V cuts)",
    },
    {
        "id": "module02-03-bstar-tree",
        "kind": "lab",
        "title": "B*-tree floorplan representation",
        "short": "B*-tree",
        "lab": "bstar-tree",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Represent a packing with a B*-tree (left-child / right-child geometry) and reconstruct module coordinates.",
        "algorithm": "B*-tree packing (left = right-of, right = above)",
    },
    {
        "id": "module02-05-sequence-pair",
        "kind": "lab",
        "title": "Sequence-pair representation",
        "short": "Sequence pair",
        "lab": "sequence-pair",
        "status": "**ref**",
        "section": "02",
        "outcomes": "Use positive and negative sequences to encode relative order and pack a sequence-pair into coordinates.",
        "algorithm": "sequence-pair packing (Γ+ / Γ−)",
    },
    {
        "id": "module03-01-simulated-annealing-fp",
        "kind": "lab",
        "title": "Simulated annealing floorplan search",
        "short": "Simulated annealing",
        "lab": "simulated-annealing-fp",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Run SA moves on a floorplan representation (swap, rotate, perturb) under a fixed outline cost.",
        "algorithm": "simulated annealing over floorplan moves (rep + cost)",
    },
    {
        "id": "module03-03-soft-module-sizing",
        "kind": "lab",
        "title": "Soft module aspect sizing",
        "short": "Soft modules",
        "lab": "soft-module-sizing",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Resize soft modules within aspect-ratio bounds while preserving area and keeping the packing legal.",
        "algorithm": "soft-module aspect-ratio sizing under fixed outline",
    },
    {
        "id": "module03-05-macro-placement",
        "kind": "lab",
        "title": "Hard macro / fixed-block placement",
        "short": "Macros",
        "lab": "macro-placement",
        "status": "**ref**",
        "section": "03",
        "outcomes": "Treat hard macros as fixed-size (and optionally fixed-position) blocks and pack soft/movable modules around them.",
        "algorithm": "hard-macro / fixed-block constrained packing",
    },
    {
        "id": "module04-01-hierarchical-floorplan",
        "kind": "lab",
        "title": "Hierarchical floorplanning",
        "short": "Hierarchical",
        "lab": "hierarchical-floorplan",
        "status": "**ref**",
        "section": "04",
        "outcomes": "Floorplan nested clusters: pack sub-floorplans inside parent regions, then compose the top outline.",
        "algorithm": "hierarchical / recursive sub-floorplan packing",
    },
    {
        "id": "module04-03-pin-assignment",
        "kind": "lab",
        "title": "Boundary pin / I/O assignment",
        "short": "Pin assignment",
        "lab": "pin-assignment",
        "status": "**ref**",
        "section": "04",
        "outcomes": "Assign I/O pins to chip edges (N/E/S/W) and relate pin sides to module abutments and wirelength hints.",
        "algorithm": "boundary pin / I/O edge assignment",
    },
    {
        "id": "module05-01-offline-benchmark-compare",
        "kind": "offline",
        "title": "Offline benchmark compare",
        "short": "Offline compare",
        "lab": None,
        "status": "P",
        "section": "05",
        "outcomes": "Compare toy floorplan engines on shared instances (area, deadspace, wirelength proxy, runtime).",
        "algorithm": "benchmark harness vs reference packings",
    },
    {
        "id": "module99-00-wrap",
        "kind": "wrap",
        "title": "Floorplanning path complete",
        "short": "Wrap",
        "lab": None,
        "status": "—",
        "section": "99",
        "outcomes": "Recap representations and search, then choose learn_placement or learn_legalization next.",
        "algorithm": None,
    },
]


def prev_next(i: int) -> tuple[dict | None, dict | None]:
    prev_m = MODULES[i - 1] if i > 0 else None
    next_m = MODULES[i + 1] if i + 1 < len(MODULES) else None
    return prev_m, next_m


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def ss_aa(m: dict) -> str:
    mid = m["id"]
    parts = mid.replace("module", "", 1).split("-")
    return f"{parts[0]}-{parts[1]}"


def nav_line(prev_m, next_m) -> str:
    left = (
        f"[← {prev_m['short']}](../{prev_m['id']}/README.md)"
        if prev_m
        else "← Start"
    )
    right = (
        f"[{next_m['short']} →](../{next_m['id']}/README.md)"
        if next_m
        else "End →"
    )
    return f"{left} · [Course README](../README.md) · {right}"


def lab_badge(m: dict) -> str:
    if m["kind"] == "lab":
        return f"**Kind:** `lab` · Primary lab: `{m['lab']}` · **Shipped**"
    if m["kind"] == "offline":
        return "**Kind:** `offline` · Primary activity: local benchmark harness · **Planned**"
    if m["kind"] == "intro":
        return "**Kind:** `intro` · Dual-track course welcome"
    return f"**Kind:** `{m['kind']}`"


def tiny_modules_json() -> str:
    data = {
        "outline": {"W": 10, "H": 8},
        "modules": [
            {"id": "A", "w": 3, "h": 2, "soft": True, "aspect_min": 0.5, "aspect_max": 2.0},
            {"id": "B", "w": 2, "h": 3, "soft": False},
            {"id": "C", "w": 2, "h": 2, "soft": False},
            {"id": "D", "w": 3, "h": 1, "soft": False},
            {"id": "E", "w": 2, "h": 2, "soft": False},
        ],
        "notes": "Outline 10×8. Deadspace = 80 − Σ(w·h). Module A is soft (aspect optional).",
    }
    return json.dumps(data, indent=2) + "\n"


# ---------------------------------------------------------------------------
# Per-module README
# ---------------------------------------------------------------------------


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

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **{m['algorithm']}** on `examples/tiny_modules.json`.
2. Complete [CHECKLIST.md](CHECKLIST.md) with legality, area, density, and deadspace (plus lab-specific metrics).
3. Optional self-check: `./scripts/module.sh {key} --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/{lab}/](http://127.0.0.1:8080/tools/{lab}/)
2. Live: [{LIVE_TOOLS}/{lab}/]({LIVE_TOOLS}/{lab}/)
3. Tools shelf: open `{lab}` from the platform tools index
4. Load the **starter modules**, run the packing / search, inspect outline metrics.
5. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach floorplan literacy on tiny outlines — not production place-and-route.
"""
    elif m["kind"] == "offline":
        body = f"""
## Outcomes

After this module you can: **{m['outcomes']}**

## Offline track

1. Follow [EXAMPLES.md](EXAMPLES.md) to run the local compare harness.
2. Record area, deadspace, wirelength proxy, and runtime against at least one reference packing when available.
3. Complete [CHECKLIST.md](CHECKLIST.md).
"""
    elif m["kind"] == "intro":
        body = """
## What this course is

**learn_floorplanning** teaches *fixed-outline floorplanning representations and search used in EDA physical design* using **two learning modes** on every lab module:

| Track | Where you practice | Best for |
|-------|--------------------|----------|
| **A — Implement** | Tiny modules + `EXAMPLES.md` / `examples/` | Fidelity: representations, packing, metrics |
| **B — Browser lab** | Interactive lab on the learning platform | Concept literacy, quick visual feedback |

You can do **A only**, **B only**, or **both** (recommended: B for intuition when shipped, then A for fidelity).

## Setup (Track A)

1. Open this course under `courses/learn_floorplanning/`.
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
    else:  # wrap
        body = """
## You can now

- Pack modules under a fixed W×H outline and report legality, density, and deadspace
- Encode packings with slicing / polish, B*-tree, and sequence-pair representations
- Search with simulated annealing moves and size soft modules / respect hard macros
- Sketch hierarchical sub-floorplans and boundary pin assignment

## Dual-track recap

If you mainly used **browser labs**, spend a short session on Track A for fixed-outline, one representation, and SA.
If you mainly used **Track A**, skim any skipped shipped browser labs for visual packing challenges.

## Next course

Prereqs done: **learn_clustering** / **learn_partitioning** (shapes from groups/cuts).

→ **learn_placement** or **learn_legalization** (see parent [`syllabus.md`](../../../syllabus.md))

## Checklist

- [ ] I completed Track A and/or Track B for the lab modules I care about
- [ ] I can explain representation trade-offs in my own words
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
- [ ] Implemented **{m['algorithm']}** end-to-end on the starter modules
- [ ] Reported legality (in-outline, no overlap), area, density, and deadspace
- [ ] Can explain the representation / move without the UI

## Track B — Browser lab (`{m['lab']}`)

- [ ] Opened the lab (local or live)
- [ ] Loaded the starter modules / outline
- [ ] Ran packing or search and inspected metrics

## Done when

- [ ] I can reproduce the packing on paper/code **or** I finished the browser challenges (preferably both)
"""
    if m["kind"] == "offline":
        return f"""# Checklist — {m['title']}

## Offline harness

- [ ] Ran the compare script on at least one shared instance
- [ ] Recorded toy-engine vs reference metrics (or documented tool missing)
- [ ] Named one discrepancy and a hypothesis

## Done when

- [ ] I can explain how to judge floorplan quality across engines
"""
    if m["kind"] == "intro":
        return f"""# Checklist — {m['title']}

- [ ] I understand the course map (sections 01–05 + wrap)
- [ ] I know Track A (implement) vs Track B (browser lab)
- [ ] I opened [docs/MODULES.md](../docs/MODULES.md) once
- [ ] Ready for fixed-outline constraints
"""
    return f"""# Checklist — {m['title']}

- [ ] I can name the main representations from sections 02–04
- [ ] I know when slicing vs B* vs sequence-pair fits
- [ ] I picked a next course (`learn_placement` or `learn_legalization`)
"""


def examples(m: dict) -> str:
    if m["kind"] == "lab":
        return f"""# Examples — {m['title']}

Track A (implement). Use the tiny outline first (`examples/tiny_modules.json`, W×H = 10×8).

## Algorithm

**{m['algorithm']}**

## Starter prompts

1. Restate the idea in five bullets (inputs → representation or loop → legality → metrics → output).
2. Load modules A–E; confirm outline area = 80 and module areas sum correctly.
3. Produce a packing (or assignment) and check: every module inside the outline, no pairwise overlap.
4. Report deadspace = outlineArea − Σ(module areas) and packing density = Σ areas / outlineArea.
5. Change one knob (aspect of soft A, a tree edge, a sequence swap, a pin side) and report what moved.

## Expected artifacts

- Coordinates (or representation) for each module
- Legality boolean + deadspace / density
- Short note: why this idea belongs on the floorplanning shelf

## Stretch

Add one hard macro at a fixed (x, y) or nest a 2-module sub-floorplan; keep the same metrics API.
"""
    if m["kind"] == "offline":
        return """# Examples — Offline benchmark compare

1. Export the same tiny_modules instance used in representation / SA labs.
2. Run your toy packer; record deadspace, density, wirelength proxy, wall time.
3. If available, compare against a reference packing (golden coordinates or another engine).
4. Fill a comparison table: quality, legality, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
"""
    if m["kind"] == "intro":
        return """# Examples — Welcome

No coding yet.

1. Sketch the PD path: partition/cluster → floorplan outline → place → legalize → route.
2. Write one sentence: “Fixed-outline floorplanning packs blocks into a given W×H because …”
3. Name one difference between a slicing floorplan and a non-slicing packing.
"""
    return """# Examples — Wrap

1. List three representations from this course and one strength each.
2. For a soft block that must keep area but change aspect, which module’s idea do you reach for?
3. Write the bridge sentence you’ll need for placement or legalization next.
"""


# ---------------------------------------------------------------------------
# Floorplanning-specific transcripts
# ---------------------------------------------------------------------------

LAB_TRANSCRIPTS: dict[str, str] = {
    "fixed-outline": """# Fixed-outline constraints

**Module id:** module01-01-fixed-outline
**Lab:** fixed-outline
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Fixed-outline constraints

Floorplanning in modern SoCs is rarely “grow the chip until everything fits.” You are given a fixed outline—width W by height H—and every module must pack inside it. In this lab you will state that outline, place rectangles, and decide whether the packing is legal.

## Slide 2 — The idea

A packing is legal when two rules hold. First, every module’s bounding box lies entirely inside the outline: no overflow past the right or top edge. Second, no two modules overlap in area. Coordinates are usually lower-left based; pick a convention and stick to it. Illegal packings are not “almost fine”—they are rejected before you optimize wirelength.

## Slide 3 — Browser lab track

Open the **fixed-outline** lab from the tools shelf. Load the starter modules on a ten-by-eight outline. Drag or assign positions, then read the legality flag. Try one illegal move—push a block past the edge or overlap two modules—and watch the checker fail. Orient yourself, then implement the same checks yourself.

## Slide 4 — Implement track

Parse `tiny_modules.json`, assign each module an (x, y), and write containment and pairwise non-overlap tests. Print a clear pass/fail plus the first violation you find. Prefer integer coordinates on the toy instance so goldens stay stable. Debugging a false illegal is part of learning the geometry.

## Slide 5 — Pitfalls

Common traps: off-by-one edges when checking “inside”; comparing centers instead of rectangles; allowing zero-area “touching” when your spec forbids shared interiors but allows shared boundaries—or the reverse. Document whether edge-touching counts as overlap. Also don’t optimize density before legality—illegal density is meaningless.

## Slide 6 — Your turn

Complete the checklist for at least one track—preferably both. Get a legal packing of A through E inside ten by eight. When you’re ready, take the short quiz, then continue to area and deadspace—the metrics every later representation will report.
""",
    "area-deadspace": """# Area, packing density, whitespace/deadspace

**Module id:** module01-03-area-deadspace
**Lab:** area-deadspace
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Area, packing density, whitespace

Once a packing is legal, you still need numbers that say how tightly the outline is used. Outline area is W times H. Module area is width times height for each block. Deadspace—also called whitespace—is outline area minus the sum of module areas. Density is that sum divided by the outline area.

## Slide 2 — The idea

Deadspace equals outlineArea minus the sum of module areas. On our toy chip, outline area is eighty. If modules sum to fifty-six, deadspace is twenty-four and density is zero point seven. Soft modules can change width and height while keeping product—area—fixed, which changes packing geometry but not the sum until you resize. Always report both deadspace and density alongside legality.

## Slide 3 — Browser lab track

Open the **area-deadspace** lab. Load the starter outline and modules. Inspect the metrics panel: outline area, sum of areas, deadspace, density. Nudge a soft module’s aspect if the UI allows and confirm the area sum stays stable while coordinates change. Then come back and compute the same formulas in code.

## Slide 4 — Implement track

Load `tiny_modules.json`. Compute outline area, per-module areas, deadspace, and density. Cross-check that deadspace is never negative for a feasible area budget—if sum of module areas exceeds the outline, no legal packing exists regardless of representation. Print a one-line metrics summary your later labs can reuse.

## Slide 5 — Pitfalls

Don’t confuse bounding-box waste of a particular packing with deadspace of the outline budget. Deadspace here is the area budget leftover, not “holes between modules” measured by a separate void analysis—though holes relate. Also don’t use wirelength as a substitute for density. And remember: a packing can be legal with high deadspace; that is whitespace, not an illegal gap.

## Slide 6 — Your turn

Finish the checklist. Memorize the deadspace formula so you can say it without notes. Next you’ll encode packings with slicing trees—same metrics, new representation.
""",
    "slicing-floorplan": """# Slicing tree / polish expression packing

**Module id:** module02-01-slicing-floorplan
**Lab:** slicing-floorplan
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Slicing floorplans

A slicing floorplan is built by recursively cutting a rectangle with through-cuts—horizontal or vertical—until each leaf is a module. The cut tree, or its polish expression with operators H and V, is a compact encoding. In this lab you’ll pack modules from a slicing tree or polish string into concrete coordinates.

## Slide 2 — The idea

An H operator stacks left and right children as bottom and top (or as specified by your convention). A V operator places them side by side. Evaluating the tree bottom-up yields the size of each composite rectangle; placing top-down assigns origins. Polish expressions are postfix: operands then H or V. Not every packing is slicing—wheels need non-slicing representations—but slicing is a strong first model.

## Slide 3 — Browser lab track

Open **slicing-floorplan**. Load a starter polish expression or tree. Step through cuts and watch rectangles subdivide. Read deadspace on the fixed outline. Change one operator from H to V and see the packing reshape. Then implement tree evaluation yourself.

## Slide 4 — Implement track

Define a small tree or polish string over modules A–E. Evaluate composite widths and heights, then assign (x, y) under the ten-by-eight outline. Reject trees whose root size exceeds the outline. Report legality and deadspace. Keep operator conventions documented in comments.

## Slide 5 — Pitfalls

Swapping H and V conventions silently flips the packing. Forgetting that composite size is max-along-cut versus sum-along-cut is the classic bug. Also: a polish string that is not a valid slicing expression will crash a naive evaluator—validate arity as you parse.

## Slide 6 — Your turn

Pack a legal slicing floorplan for the starter modules. Quiz when ready, then meet B*-trees—which can represent non-slicing packings more naturally.
""",
    "bstar-tree": """# B*-tree floorplan representation

**Module id:** module02-03-bstar-tree
**Lab:** bstar-tree
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — B*-tree floorplans

B*-trees are a popular compacted floorplan representation. Each node is a module. The left child sits to the right of its parent; the right child sits above—under the usual contour packing rules. From the tree you reconstruct coordinates without storing every x and y explicitly.

## Slide 2 — The idea

Root at the lower-left. Walking left children grows the packing rightward; right children grow upward along a contour of previously placed blocks. Packing is typically done with a horizontal contour so y coordinates stay compacted. Perturbing the tree—rotate, move, swap—yields neighboring packings for annealing later.

## Slide 3 — Browser lab track

Open **bstar-tree**. Load a starter tree over A–E. Step placement: parent, left child, right child. Watch modules land left/right/above as the contour updates. Inspect outline legality and deadspace. Then code the same left/right packing rules.

## Slide 4 — Implement track

Build a B*-tree for the tiny modules. Implement contour-based packing to emit (x, y, w, h). Verify non-overlap and outline containment. Print the tree in a readable parenthesized form so goldens are reviewable. Prefer deterministic child ordering for tests.

## Slide 5 — Pitfalls

Getting left/right geometry backwards is the number-one bug. Contour updates that forget deleted segments leave modules floating or overlapping. Don’t confuse B*-tree adjacency with netlist adjacency—the tree is a packing code, not connectivity.

## Slide 6 — Your turn

Produce a legal B*-tree packing inside the outline. Next: sequence pairs—another classic encoding with positive and negative sequences.
""",
    "sequence-pair": """# Sequence-pair representation

**Module id:** module02-05-sequence-pair
**Lab:** sequence-pair
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Sequence pairs

A sequence pair is two permutations of the modules—often called the positive and negative sequences, Γ-plus and Γ-minus. Together they encode relative left-right and above-below order. From the pair you can pack coordinates with longest-path style constraints on a constraint graph.

## Slide 2 — The idea

If module A appears before B in both sequences, A is left of B. If A appears before B in Γ-plus but after B in Γ-minus, A is above B—under the standard Murata interpretation. Horizontal and vertical constraint graphs yield x and y via longest paths. Soft sizing and rotation can be layered on later; first get hard rectangles right.

## Slide 3 — Browser lab track

Open **sequence-pair**. Load starter Γ-plus and Γ-minus. Highlight one pair of modules and read the implied relation—left-of or above. Pack and inspect deadspace under the fixed outline. Swap two symbols in one sequence and watch relations flip. Then implement packing from sequences in Track A.

## Slide 4 — Implement track

Represent Γ-plus and Γ-minus as lists of module ids. Build constraint edges, compute coordinates, and check legality on the ten-by-eight outline. Report deadspace. Keep permutations as permutations—no duplicate ids. Deterministic packing helps goldens.

## Slide 5 — Pitfalls

Mixing up which sequence pair condition means “left of” versus “above” yields mirrored nonsense. Forgetting transitive longest-path compaction leaves unnecessary whitespace. And sequence pairs can encode non-slicing packings—don’t force a slicing tree interpretation onto them.

## Slide 6 — Your turn

Pack A–E from a sequence pair and verify legality. Next you’ll search the space of representations with simulated annealing.
""",
    "simulated-annealing-fp": """# Simulated annealing floorplan search

**Module id:** module03-01-simulated-annealing-fp
**Lab:** simulated-annealing-fp
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Simulated annealing search

Representations give you a packing. Search finds a good one under a fixed outline. Simulated annealing perturbs the representation—swap modules, rotate, change a tree edge or sequence—and accepts uphill moves early so you escape local minima. Cost usually mixes outline overflow, deadspace, and a wirelength proxy.

## Slide 2 — The idea

Pick a representation you already trust: slicing, B*, or sequence pair. Define moves that stay in that encoding. At temperature T, accept worse costs with probability related to exp of minus delta over T. Cool on a schedule. Always re-pack and re-score after a move. Illegal overflow should cost heavily so the search prefers legal packings.

## Slide 3 — Browser lab track

Open **simulated-annealing-fp**. Run a short anneal on the starter instance. Watch cost and temperature. Pause, inspect the current packing, then continue. Try a hotter start versus a greedy low temperature. Then implement a tiny SA loop yourself with a fixed seed.

## Slide 4 — Implement track

Wire SA around one representation. Log temperature, cost, and best packing. Use a deterministic RNG seed. Stop after a modest iteration budget on the toy outline—this is literacy, not overnight runs. Export the best coordinates and deadspace.

## Slide 5 — Pitfalls

Moves that don’t change the packing waste iterations. A cost that ignores overflow will “optimize” illegal layouts. Cooling too fast freezes a bad packing; cooling too slow teaches nothing on a five-module toy. Also don’t compare costs across different outline penalties without documenting the weights.

## Slide 6 — Your turn

Get SA to improve deadspace or wirelength proxy from a random start while staying legal. Next: soft modules—resize aspect under area constraints.
""",
    "soft-module-sizing": """# Soft module aspect sizing

**Module id:** module03-03-soft-module-sizing
**Lab:** soft-module-sizing
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Soft module sizing

Hard modules have fixed width and height. Soft modules keep a fixed area but may change aspect ratio within bounds—minimum and maximum width over height. Floorplanning often sizes soft blocks while packing so the outline fills with less deadspace.

## Slide 2 — The idea

For soft module A with area a, choose width w and set height to a over w, subject to aspect_min ≤ w/h ≤ aspect_max. Re-pack after each sizing move. On our starter, A is soft; B through E stay hard. Deadspace uses the same formula: outline area minus sum of areas—areas stay constant if only aspect changes.

## Slide 3 — Browser lab track

Open **soft-module-sizing**. Select module A, drag aspect within bounds, and watch the packing reshape under the fixed outline. Confirm area of A stays constant while density of the packing geometry changes. Then implement aspect moves in Track A.

## Slide 4 — Implement track

Extend your packer so A’s (w, h) can vary under aspect constraints at constant area. Combine with a simple search—even greedy aspect tries help. Report legality and deadspace before and after. Reject sizes outside aspect bounds.

## Slide 5 — Pitfalls

Using aspect limits on w/h but updating only w without fixing h = area/w breaks the area invariant. Allowing zero width is nonsense—enforce positive sizes. Soft sizing cannot fix an area budget that already exceeds the outline.

## Slide 6 — Your turn

Improve a legal packing by resizing A within bounds. Next: hard macros that refuse to move or resize.
""",
    "macro-placement": """# Hard macro / fixed-block placement

**Module id:** module03-05-macro-placement
**Lab:** macro-placement
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Hard macros

Hard macros are fixed-size blocks—memories, analog IP, pre-placed covers. Sometimes their (x, y) is fixed too. Floorplanning must pack softer or movable modules around them without overlap and without leaving the outline. Treating macros as ordinary free rectangles loses the constraint.

## Slide 2 — The idea

Mark macros as hard: width and height immutable. If position is fixed, lock (x, y) and forbid moves that shift them. Other modules pack in the remaining free space. Cost still includes overflow and deadspace; wirelength may prefer soft blocks near related macros. Legality checks apply unchanged—macros are just immovable obstacles.

## Slide 3 — Browser lab track

Open **macro-placement**. Lock one module as a fixed hard block. Try to pack the others around it. Force an overlap and watch the checker. Unlock and compare freedom. Then encode fixed blocks in your Track A data model.

## Slide 4 — Implement track

Extend `tiny_modules.json` with a `fixed: true` and optional `x`, `y` on one module. Pack the rest with your chosen representation, treating the macro as an obstacle. Fail loudly if a move would shift a fixed macro. Report legality and deadspace.

## Slide 5 — Pitfalls

Silently moving a “fixed” macro during SA is a trust-breaking bug. Also don’t shrink hard macros when soft sizing runs. Overlapping two macros at init means the instance is already illegal—detect that before search.

## Slide 6 — Your turn

Produce a legal packing with at least one fixed hard macro. Next: hierarchical floorplans that nest sub-packings inside parent regions.
""",
    "hierarchical-floorplan": """# Hierarchical floorplanning

**Module id:** module04-01-hierarchical-floorplan
**Lab:** hierarchical-floorplan
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Hierarchical floorplans

Large designs floorplan recursively: clusters become soft or hard regions, each with its own sub-floorplan, then compose into the chip outline. Hierarchy reuses the same packing ideas at every level and mirrors how partitioning and clustering fed you the blocks.

## Slide 2 — The idea

Pick a parent region inside the outline. Floorplan a subset of modules inside that region as if it were its own fixed outline. Place sibling regions, then recurse. Top-level deadspace still uses the chip outline area; local deadspace can be reported per region. Keep region outlines legal with respect to their parent.

## Slide 3 — Browser lab track

Open **hierarchical-floorplan**. Load a two-level starter: a parent outline and two child groups. Pack inside each child, then place children in the parent. Inspect metrics at both levels. Then implement nested packing in Track A.

## Slide 4 — Implement track

Partition A–E into two groups. Floorplan each group into a sub-rectangle, then place those rectangles in the ten-by-eight outline. Verify no group overflows its region and regions don’t overlap. Report global deadspace.

## Slide 5 — Pitfalls

Optimizing children while ignoring parent legality leaves you with beautiful sub-floorplans that don’t compose. Don’t double-count module area across levels. Align coordinates to a single global origin when composing.

## Slide 6 — Your turn

Ship one hierarchical packing for the tiny instance. Next: assign I/O pins to the chip boundary.
""",
    "pin-assignment": """# Boundary pin / I/O assignment

**Module id:** module04-03-pin-assignment
**Lab:** pin-assignment
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Boundary pins

Chips talk to the outside world through I/O pins on the outline edges—north, east, south, west. Pin assignment places those pins along edges and influences which modules should abut which sides. Floorplanning without pins ignores a major wirelength and packaging constraint.

## Slide 2 — The idea

Each pin gets an edge and a position along that edge. Modules that connect to a pin prefer shorter Manhattan stubs toward that side. You can score a packing with a simple pin-to-module wirelength proxy. Fixed outline still governs module legality; pins live on the boundary, not inside module interiors.

## Slide 3 — Browser lab track

Open **pin-assignment**. Place a few pins on the four edges. Connect them to modules A–E with a toy netlist. Watch the wirelength proxy as you move pins or modules. Then implement edge assignment and scoring in Track A.

## Slide 4 — Implement track

Add a pin list: id, side, offset. Assign sides for a handful of I/Os. Score sum of distances from module centers (or abutment points) to pin locations. Keep modules legal under the outline while you tweak assignments. Print the assignment table and score.

## Slide 5 — Pitfalls

Putting pins inside the outline instead of on the boundary breaks the model. Crowding every pin onto one edge creates congestion you won’t see if you only watch deadspace. Don’t forget that pin order on an edge can matter for packaging—even on a toy.

## Slide 6 — Your turn

Assign boundary pins and report a wirelength proxy beside deadspace. Then continue to offline compare—and finally the wrap.
""",
}


def transcript_lab(m: dict) -> str:
    lab = m["lab"]
    if lab in LAB_TRANSCRIPTS:
        return LAB_TRANSCRIPTS[lab]
    # Fallback should not happen for this course
    return f"# {m['title']}\n\n## Slide 1 — {m['title']}\n\nImplement **{m['algorithm']}**.\n"


def transcript_intro() -> str:
    return """# Welcome to floorplanning for EDA

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to floorplanning for EDA

After clustering and partitioning, physical design asks a geometric question: how do we pack blocks into a fixed chip outline? That is floorplanning. This course teaches fixed-outline packing, classic representations, and search—as full implementations on tiny modules—so placement and legalization make sense later.

## Slide 2 — What you’ll build

You’ll start with outline legality, area, density, and deadspace. Then slicing trees and polish expressions, B*-trees, and sequence pairs. Simulated annealing searches those encodings. Soft modules change aspect; hard macros stay fixed; hierarchy nests sub-floorplans; pins land on chip edges. One idea per lab. Complete and correct on scoped instances—not a production P&R engine.

## Slide 3 — Stable module ids

Module folders use hierarchical ids: section, then algorithm slot—like module two dash zero three for B*-tree. Odd slots leave room for inserts. Treat published ids as stable keys; display order lives in the module index.

## Slide 4 — Two tracks

Every lab offers Track A—implement packing and metrics on tiny modules—and Track B—browser labs for visual intuition when shipped. A good rhythm is browser first for the geometry, then implement to harden it. Intro and wrap have no lab.

## Slide 5 — How to move

Read each README for outcomes, pick a track—or both—then work the checklist. Keep legality, deadspace, and density as your habit. When this intro checklist is done, continue to fixed-outline constraints—the gate every later packing must pass.
"""


def transcript_wrap() -> str:
    return """# Floorplanning path complete

**Module id:** module99-00-wrap
**Lab:** none (wrap)
**Tracks:** recap · next course

## Slide 1 — Floorplanning path complete

You’ve walked the floorplanning path—from fixed outlines and deadspace, through slicing, B*-tree, and sequence-pair encodings, into simulated annealing, soft sizing, macros, hierarchy, and pin assignment, plus an offline compare habit. This wrap names what you can do now and where to go next.

## Slide 2 — What you can do now

You can pack modules under a W by H outline and prove legality. You can compute deadspace as outline area minus the sum of module areas. You can encode packings three classic ways, search with annealing moves, size soft blocks, respect hard macros, nest sub-floorplans, and assign boundary pins. You are building algorithm literacy—not shipping a foundry floorplanner.

## Slide 3 — Close the gaps

If you mainly watched browser labs, finish at least one full implementation in foundations and one representation plus SA. If you mainly coded, re-open visual labs for packing intuition. Clustering and partitioning as prereqs should already feel connected: groups and cuts became shapes and whitespace.

## Slide 4 — Next courses

Natural next steps are learn_placement—spreading standard cells under the floorplan—and learn_legalization—snapping to rows and sites without overlap. Keep your tiny_modules harness; placement courses reuse outline thinking. Mentally bookmark clustering and partitioning as the path you already finished into this course.

## Slide 5 — Your turn

Review the wrap checklist. Name three representations and one strength each. Say how deadspace is computed. When you’re ready, take the short quiz, then open learn_placement or learn_legalization.
"""


def transcript_offline() -> str:
    return """# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none (offline)
**Tracks:** offline harness

## Slide 1 — Offline benchmark compare

Toy packers teach mechanism. Benchmarks teach honesty. In this offline module you’ll run the same tiny_modules instances through your floorplan code and, when available, a reference packing—then compare deadspace, density, wirelength proxy, and runtime without pretending the numbers are tape-out sign-off.

## Slide 2 — Fair compare rules

Use identical input and the same outline. Fix seeds when search is randomized. Report the same metrics on both sides. If a reference engine is missing, still run your harness and document the gap—don’t invent golden deadspace. A clean I/O contract matters more than a flashy chart.

## Slide 3 — What good looks like

Expect your educational engine to be slower and sometimes lower quality. That’s fine. You’re looking for legal packings, non-negative deadspace consistent with areas, and improving cost under SA. Huge unexplained wins usually mean a metric mismatch—or an illegal packing you failed to reject.

## Slide 4 — Your turn

Follow the examples file, fill the comparison table, and finish the checklist. Bring one discrepancy and a short hypothesis into your notes. Then continue to the wrap module to close the course.
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
                    "Fixed-outline floorplanning representations and search on tiny modules",
                    "Foundry PDK certification",
                    "Writing UVM agents",
                ],
                "answer": 1,
                "explain": "Algorithm / toy-engine literacy on scoped floorplans.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "A fixed-outline floorplan may legally place modules outside the W×H chip.",
                "answer": False,
                "explain": "Containment inside the outline is required for legality.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A good study rhythm is…",
                "choices": [
                    "Only memorize folder names",
                    "Browser intuition then implement packing metrics on tiny modules",
                    "Skip checklists entirely",
                    "Start with pin assignment before legality",
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
                "prompt": "Deadspace under a fixed outline is…",
                "choices": [
                    "Always zero",
                    "outlineArea − sum(module areas)",
                    "Only the wirelength",
                    "The number of pins on the north edge",
                ],
                "answer": 1,
                "explain": "Whitespace budget left after module areas.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "B*-tree and sequence-pair are packing representations; SA searches over moves on a representation.",
                "answer": True,
                "explain": "Encode then search is the floorplan pattern.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "Natural next courses after floorplanning are…",
                "choices": [
                    "Only analog layout",
                    "learn_placement and learn_legalization",
                    "SPICE device models first",
                    "Ignore the PD stack",
                ],
                "answer": 1,
                "explain": "Placement and legalization continue from the outline.",
            },
        ]
        title = "Wrap check"
    elif m["kind"] == "offline":
        items = [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Fair compares require the same outline/modules and comparable metrics.",
                "answer": True,
                "explain": "Otherwise you compare different problems.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "If a reference engine is missing you should…",
                "choices": [
                    "Invent golden deadspace",
                    "Still run your harness and document the gap",
                    "Delete your metrics",
                    "Skip legality checks",
                ],
                "answer": 1,
                "explain": "Honesty about tooling beats fake goldens.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "An educational packer that is slower than a commercial tool is automatically wrong.",
                "answer": False,
                "explain": "Speed differs; look for legal, consistent metrics.",
            },
        ]
        title = "Offline check"
    else:
        # Lab-specific quizzes
        lab_quizzes = {
            "fixed-outline": [
                {
                    "id": "q1",
                    "type": "true_false",
                    "prompt": "A packing with two overlapping modules can still be legal if both fit in the outline.",
                    "answer": False,
                    "explain": "Non-overlap is required for legality.",
                },
                {
                    "id": "q2",
                    "type": "multiple_choice",
                    "prompt": "Fixed-outline legality primarily checks…",
                    "choices": [
                        "Only total wirelength",
                        "Containment in W×H and non-overlap",
                        "Only pin order",
                        "Liberty timing arcs",
                    ],
                    "answer": 1,
                    "explain": "Geometry first.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Track A asks you to implement containment and non-overlap checks on tiny modules.",
                    "answer": True,
                    "explain": "Implement track hardens the checker.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "On a 10×8 outline, outline area is…",
                    "choices": ["18", "80", "10", "8"],
                    "answer": 1,
                    "explain": "W×H = 80.",
                },
            ],
            "area-deadspace": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": "Deadspace equals…",
                    "choices": [
                        "sum(module areas) − outlineArea",
                        "outlineArea − sum(module areas)",
                        "Only overlapping area",
                        "Pin count × outlineArea",
                    ],
                    "answer": 1,
                    "explain": "Whitespace budget formula.",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "If Σ module areas exceeds outline area, no legal packing exists.",
                    "answer": True,
                    "explain": "Area budget is a hard feasibility gate.",
                },
                {
                    "id": "q3",
                    "type": "multiple_choice",
                    "prompt": "Packing density is…",
                    "choices": [
                        "outlineArea / Σ areas",
                        "Σ areas / outlineArea",
                        "Always 1.0",
                        "Wirelength / area",
                    ],
                    "answer": 1,
                    "explain": "Occupied fraction of the outline.",
                },
                {
                    "id": "q4",
                    "type": "true_false",
                    "prompt": "Changing a soft module’s aspect at constant area changes Σ module areas.",
                    "answer": False,
                    "explain": "Area product stays fixed; geometry changes.",
                },
            ],
            "slicing-floorplan": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": "Slicing floorplans are built with…",
                    "choices": [
                        "Only diagonal cuts",
                        "Recursive through-cuts H and V",
                        "Only force-directed placement",
                        "SDF annotation",
                    ],
                    "answer": 1,
                    "explain": "H/V slicing tree / polish.",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "A polish expression is a postfix encoding with module operands and H/V operators.",
                    "answer": True,
                    "explain": "Classic slicing encoding.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Every packing is a slicing floorplan.",
                    "answer": False,
                    "explain": "Wheels / non-slicing need other reps.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "Composite size along a V cut typically…",
                    "choices": [
                        "Sums widths and takes max height (convention-dependent detail aside)",
                        "Ignores child sizes",
                        "Uses only pin counts",
                        "Forces zero deadspace",
                    ],
                    "answer": 0,
                    "explain": "Combine children geometrically.",
                },
            ],
            "bstar-tree": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": "In the usual B*-tree packing, the left child of a node is placed…",
                    "choices": [
                        "To the right of the parent",
                        "Always at the chip origin",
                        "Only on the north pin edge",
                        "With negative coordinates",
                    ],
                    "answer": 0,
                    "explain": "Left = right-of parent (common convention).",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "The right child is typically packed above (contour / above relation).",
                    "answer": True,
                    "explain": "Right = above in standard B* packing.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "A B*-tree is a netlist connectivity tree, not a packing code.",
                    "answer": False,
                    "explain": "It encodes packing adjacency.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "After packing from a B*-tree you should still check…",
                    "choices": [
                        "Only TTS quality",
                        "Outline legality and non-overlap",
                        "Only Git status",
                        "Nothing",
                    ],
                    "answer": 1,
                    "explain": "Representation ≠ automatic legality on a tight outline.",
                },
            ],
            "sequence-pair": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": "A sequence pair consists of…",
                    "choices": [
                        "One polish string only",
                        "Two permutations (Γ+ and Γ−)",
                        "Only a temperature schedule",
                        "Liberty tables",
                    ],
                    "answer": 1,
                    "explain": "Positive and negative sequences.",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "Relative order in Γ+ and Γ− encodes left-of / above-below relations.",
                    "answer": True,
                    "explain": "Classic Murata-style interpretation.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Sequence pairs can only encode slicing packings.",
                    "answer": False,
                    "explain": "They can encode general packings.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "Coordinates are often obtained via…",
                    "choices": [
                        "Longest paths on constraint graphs",
                        "Random pixel painting only",
                        "Ignoring Γ−",
                        "SPICE DC analysis",
                    ],
                    "answer": 0,
                    "explain": "H/V constraint graphs + longest path.",
                },
            ],
            "simulated-annealing-fp": [
                {
                    "id": "q1",
                    "type": "true_false",
                    "prompt": "SA perturbs a floorplan representation and may accept uphill cost early.",
                    "answer": True,
                    "explain": "Escape local minima with temperature.",
                },
                {
                    "id": "q2",
                    "type": "multiple_choice",
                    "prompt": "After each SA move you should…",
                    "choices": [
                        "Skip re-packing",
                        "Re-pack and re-score cost (incl. overflow)",
                        "Only update the README",
                        "Delete soft modules",
                    ],
                    "answer": 1,
                    "explain": "Moves change geometry; rescore.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "A cost that ignores outline overflow can reward illegal packings.",
                    "answer": True,
                    "explain": "Penalize overflow heavily.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "SA moves act on…",
                    "choices": [
                        "Only GDS layers",
                        "The chosen representation (tree / sequences / polish)",
                        "Only router tracks",
                        "Git commits",
                    ],
                    "answer": 1,
                    "explain": "Encode → move → pack → cost.",
                },
            ],
            "soft-module-sizing": [
                {
                    "id": "q1",
                    "type": "true_false",
                    "prompt": "Soft modules keep area fixed while aspect ratio may vary within bounds.",
                    "answer": True,
                    "explain": "Classic soft block model.",
                },
                {
                    "id": "q2",
                    "type": "multiple_choice",
                    "prompt": "If area is fixed and width changes, height should be…",
                    "choices": [
                        "Unchanged always",
                        "area / width (with aspect limits)",
                        "Always equal to outline H",
                        "Zero",
                    ],
                    "answer": 1,
                    "explain": "Preserve area product.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Soft sizing can make Σ areas exceed the outline even if it started feasible.",
                    "answer": False,
                    "explain": "Aspect changes don’t change areas.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "On the starter instance, which module is soft?",
                    "choices": ["B", "A", "All of them", "None"],
                    "answer": 1,
                    "explain": "Module A is marked soft.",
                },
            ],
            "macro-placement": [
                {
                    "id": "q1",
                    "type": "true_false",
                    "prompt": "Hard macros have fixed size and may also have fixed (x, y).",
                    "answer": True,
                    "explain": "Fixed blocks / preplaced macros.",
                },
                {
                    "id": "q2",
                    "type": "multiple_choice",
                    "prompt": "During SA, a fixed macro should…",
                    "choices": [
                        "Move freely like soft blocks",
                        "Keep locked size/position as constrained",
                        "Be deleted",
                        "Ignore overlap checks",
                    ],
                    "answer": 1,
                    "explain": "Respect hard constraints.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Soft sizing should not shrink hard macros.",
                    "answer": True,
                    "explain": "Hard means immutable geometry.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "Overlapping two macros at initialization means…",
                    "choices": [
                        "The instance is already illegal",
                        "Deadspace is negative by definition",
                        "Pins must all be north",
                        "SA will always fix it without checks",
                    ],
                    "answer": 0,
                    "explain": "Detect illegal init early.",
                },
            ],
            "hierarchical-floorplan": [
                {
                    "id": "q1",
                    "type": "true_false",
                    "prompt": "Hierarchical floorplanning packs subsets into regions, then composes regions into the chip outline.",
                    "answer": True,
                    "explain": "Recursive / nested packing.",
                },
                {
                    "id": "q2",
                    "type": "multiple_choice",
                    "prompt": "Child regions must…",
                    "choices": [
                        "Ignore the parent outline",
                        "Stay legal inside their parent region",
                        "Always use zero deadspace",
                        "Only contain pins",
                    ],
                    "answer": 1,
                    "explain": "Compose legality bottom-up.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Module area should be double-counted at every hierarchy level when reporting global Σ areas.",
                    "answer": False,
                    "explain": "Count each module once globally.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "Hierarchy connects naturally to…",
                    "choices": [
                        "Prior clustering / partitioning of blocks",
                        "Only SPICE noise analysis",
                        "Git rebase",
                        "UART baud rates",
                    ],
                    "answer": 0,
                    "explain": "Clusters become floorplan regions.",
                },
            ],
            "pin-assignment": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": "Boundary pins are assigned to…",
                    "choices": [
                        "Chip edges (N/E/S/W)",
                        "Only module interiors",
                        "Liberty cells only",
                        "GitHub issues",
                    ],
                    "answer": 0,
                    "explain": "I/O on the outline.",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "Pin assignment can influence which modules should abut which sides.",
                    "answer": True,
                    "explain": "Wirelength / packaging pressure.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": "Pins live inside module interiors, not on the outline.",
                    "answer": False,
                    "explain": "Boundary I/O model.",
                },
                {
                    "id": "q4",
                    "type": "multiple_choice",
                    "prompt": "A simple pin score often uses…",
                    "choices": [
                        "Manhattan distance from modules to pin locations",
                        "Only deadspace",
                        "Only temperature",
                        "FFT of the GDS",
                    ],
                    "answer": 0,
                    "explain": "Wirelength proxy to edges.",
                },
            ],
        }
        items = lab_quizzes.get(
            m["lab"],
            [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "prompt": f"This lab’s primary focus is…",
                    "choices": [
                        m["algorithm"],
                        "Vendor P&R GUI only",
                        "SPICE transient analysis",
                        "Scan-chain stitching",
                    ],
                    "answer": 0,
                    "explain": f"Focus: {m['algorithm']}.",
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "prompt": "You should report legality, deadspace, and density for packings.",
                    "answer": True,
                    "explain": "Core floorplan metrics.",
                },
                {
                    "id": "q3",
                    "type": "true_false",
                    "prompt": f"Track A asks you to implement {m['algorithm']} on tiny modules.",
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
| `01` | Foundations (fixed outline, area / deadspace) |
| `02` | Representations (slicing, B*-tree, sequence pair) |
| `03` | Search & blocks (SA, soft modules, macros) |
| `04` | Hierarchy & pins |
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

- Fixed-outline floorplanning (W×H chip) and legal packing checks
- Area, packing density, and deadspace (= outlineArea − Σ module areas)
- Slicing tree / polish expression packing
- B*-tree and sequence-pair representations
- Simulated annealing search over floorplan moves
- Soft module aspect sizing and hard macro / fixed-block constraints
- Hierarchical sub-floorplans and boundary pin / I/O assignment
- Offline compare habits on shared tiny instances

## Out of scope (v1)

- Production place-and-route engines or foundry sign-off
- Vendor GUI workflows (Innovus / ICC2 click-paths)
- Detailed standard-cell placement and row legalization (see `learn_placement`, `learn_legalization`)
- Full chip packaging / substrate codesign

## “Full implementation” means

Complete and correct for the **scoped problem size** (a handful of modules on a tiny outline): parse input, pack or search, emit coordinates + metrics—not a production-scale floorplanner.
""",
    )
    write(
        ROOT / "docs" / "TWO_TRACKS.md",
        f"""# Two learning tracks

## Track A — Implement

Practice by coding packing, representations, and metrics on tiny modules.

- Prompts live under each `moduleSS-AA-*/EXAMPLES.md`
- Shared instance: [`common/tiny_modules.json`](../common/tiny_modules.json)
- Self-check: `./scripts/module.sh SS-AA --check` (e.g. `01-03`)

Use this track when you need **fidelity**: data structures, legality, deadspace, and reproducible goldens.

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

[![GitHub](https://img.shields.io/badge/GitHub-learn__floorplanning-181717?logo=github)](https://github.com/universal-verification-methodology/learn_floorplanning)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-orange)](../../syllabus.md)
[![Parent](https://img.shields.io/badge/parent-learning%20monorepo-0A9EDC)](https://github.com/universal-verification-methodology/learning)
[![Labs](https://img.shields.io/badge/labs-GitHub%20Pages-222?logo=githubpages)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-floorplanning-purple)](docs/MODULES.md)

**{COURSE_ID}** is the open learning path for *fixed-outline floorplanning representations and search used in EDA physical design*—one full idea per lab, on tiny modules.

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
├── common/              # tiny_modules.json, shared helpers
├── docs/
│   ├── MODULES.md       # full module index
│   ├── TWO_TRACKS.md    # Track A (implement) vs Track B (browser)
│   ├── SCOPE.md
│   └── WALKTHROUGHS.md  # algorithm walkthrough map
├── scripts/
│   ├── module.sh
│   ├── scaffold_course.py
│   └── build_all_media.sh
├── module00-00-intro/
├── module01-01-fixed-outline/
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
- **Syllabus (parent):** [`syllabus.md` § {COURSE_ID}](../../syllabus.md)
- **Scope:** [docs/SCOPE.md](docs/SCOPE.md)
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
| **A — Implement** | Tiny modules + `EXAMPLES.md` / `examples/` | [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md) · `./scripts/module.sh SS-AA --check` |
| **B — Browser lab** | Platform tools | [local tools](http://127.0.0.1:8080/tools/) · [live](https://universal-verification-methodology.github.io/learning/tools/) |

Recommended path: short Track B starter (if shipped) → Track A implement + checklist → optional quiz / transcript review.

## Module landings

Full status table: **[docs/MODULES.md](docs/MODULES.md)**. Clusters: 00 intro · 01 foundations · 02 representations · 03 search/blocks · 04 hierarchy/pins · 05 offline · 99 wrap.

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


def write_common() -> None:
    write(
        ROOT / "common" / "README.md",
        f"""# common — {COURSE_ID}

Shared Track A helpers for tiny floorplan instances.

## Starter instance

[`tiny_modules.json`](tiny_modules.json) — modules **A–E** with widths/heights, outline **W×H = 10×8**. Module **A** is soft (optional aspect bounds).

Suggested layout as you flesh reference solvers:

- `pack_io.py` — load/save tiny JSON modules + outline
- `metrics.py` — legality, area, density, deadspace
- `goldens/` — expected packings for starter instances

Browser algorithms will live under `platform/tools/<lab-id>/` when published.
""",
    )
    write(ROOT / "common" / "tiny_modules.json", tiny_modules_json())


def write_license() -> None:
    write(
        ROOT / "LICENSE",
        """Creative Commons Attribution 4.0 International (CC BY 4.0)

Copyright (c) contributors to learn_floorplanning / the learning monorepo.

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
#           ./scripts/module.sh 00-00 --demo
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


def main() -> None:
    write_license()
    write_docs()
    write_modules_md()
    write_course_readme()
    write_common()
    write_module_sh()
    write_build_script()

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
            write(base / "examples" / "tiny_modules.json", tiny_modules_json())
        print(f"ok {mid}")
    print(f"Scaffolded {len(MODULES)} modules under {ROOT}")


if __name__ == "__main__":
    main()
