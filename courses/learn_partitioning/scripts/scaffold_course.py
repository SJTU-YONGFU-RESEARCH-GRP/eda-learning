#!/usr/bin/env python3
"""Scaffold learn_partitioning modules (hierarchical SS-AA ids) with module-slides stubs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODULES = [
    {
        "id": "module00-00-intro",
        "kind": "intro",
        "title": "Welcome to partitioning for EDA",
        "short": "Welcome",
        "lab": None,
        "status": "—",
        "section": "00",
        "outcomes": "Explain why bipartition and multiway partitioning matter in physical design and how this course is organized.",
        "algorithm": None,
    },
    {
        "id": "module01-01-cutsize-balance",
        "kind": "lab",
        "title": "Cutsize and balance",
        "short": "Cutsize & balance",
        "lab": "cutsize-balance",
        "status": "P",
        "section": "01",
        "outcomes": "Compute edge cutsize and part balance for a bipartition and explain the cut–balance trade-off.",
        "algorithm": "cutsize + balance metrics on a labeled bipartition",
    },
    {
        "id": "module01-03-initial-bipartition",
        "kind": "lab",
        "title": "Initial bipartition",
        "short": "Initial bipartition",
        "lab": "initial-bipartition",
        "status": "P",
        "section": "01",
        "outcomes": "Build a legal initial bipartition (random, greedy, or grow) that respects balance before refinement.",
        "algorithm": "random / greedy / grow initial bipartition",
    },
    {
        "id": "module02-01-kl-partition",
        "kind": "lab",
        "title": "Kernighan–Lin bipartition",
        "short": "Kernighan–Lin",
        "lab": "kl-partition",
        "status": "P",
        "section": "02",
        "outcomes": "Run full KL pair-swap bipartition from a seed cut with gains, locking, and rollback to the best prefix.",
        "algorithm": "Kernighan–Lin (KL) bipartition",
    },
    {
        "id": "module02-03-fm-partition",
        "kind": "lab",
        "title": "Fiduccia–Mattheyses bipartition",
        "short": "Fiduccia–Mattheyses",
        "lab": "fm-partition",
        "status": "P",
        "section": "02",
        "outcomes": "Run full FM single-vertex moves with bucketed gains and balance constraints to improve a bipartition.",
        "algorithm": "Fiduccia–Mattheyses (FM) bipartition",
    },
    {
        "id": "module02-05-spectral-partition",
        "kind": "lab",
        "title": "Spectral bipartition",
        "short": "Spectral",
        "lab": "spectral-partition",
        "status": "P",
        "section": "02",
        "outcomes": "Build the Laplacian, take the Fiedler vector, and bipartition under balance constraints.",
        "algorithm": "spectral bipartition (Laplacian / Fiedler)",
    },
    {
        "id": "module02-07-recursive-bisection",
        "kind": "lab",
        "title": "Recursive bisection",
        "short": "Recursive bisection",
        "lab": "recursive-bisection",
        "status": "P",
        "section": "02",
        "outcomes": "Obtain a multiway partition by recursively bipartitioning parts until k parts are reached.",
        "algorithm": "recursive bisection to k parts",
    },
    {
        "id": "module03-01-multiway-partition",
        "kind": "lab",
        "title": "Multiway partitioning",
        "short": "Multiway",
        "lab": "multiway-partition",
        "status": "P",
        "section": "03",
        "outcomes": "Form and evaluate a direct k-way partition and compare it to recursive bisection on the same graph.",
        "algorithm": "direct multiway partitioning",
    },
    {
        "id": "module03-03-terminal-propagation",
        "kind": "lab",
        "title": "Terminal propagation",
        "short": "Terminals",
        "lab": "terminal-propagation",
        "status": "P",
        "section": "03",
        "outcomes": "Propagate fixed terminals / pads into the partition objective so I/O constraints shape the cut.",
        "algorithm": "terminal propagation with fixed nodes",
    },
    {
        "id": "module03-05-hypergraph-partition",
        "kind": "lab",
        "title": "Hypergraph partitioning",
        "short": "Hypergraph",
        "lab": "hypergraph-partition",
        "status": "P",
        "section": "03",
        "outcomes": "Model nets as hyperedges and optimize a hyperedge-cut objective for bipartition.",
        "algorithm": "hypergraph / netlist cut bipartition",
    },
    {
        "id": "module04-01-multilevel-partition",
        "kind": "lab",
        "title": "Multilevel partitioning",
        "short": "Multilevel",
        "lab": "multilevel-partition",
        "status": "P",
        "section": "04",
        "outcomes": "Run a partitioning V-cycle: coarsen, initial partition, project, and refine at each level.",
        "algorithm": "multilevel coarsen / initial / uncoarsen / refine",
    },
    {
        "id": "module05-01-offline-benchmark-compare",
        "kind": "offline",
        "title": "Offline benchmark compare",
        "short": "Offline compare",
        "lab": None,
        "status": "P",
        "section": "05",
        "outcomes": "Compare toy partitioners against open partitioning tools on shared instances.",
        "algorithm": "benchmark harness vs external tools",
    },
    {
        "id": "module99-00-wrap",
        "kind": "wrap",
        "title": "Partitioning path complete",
        "short": "Wrap",
        "lab": None,
        "status": "—",
        "section": "99",
        "outcomes": "Recap cut–balance trade-offs and choose the next course (clustering / floorplanning / placement).",
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


def nav_line(prev_m, next_m) -> str:
    left = f"[← {prev_m['short']}](../{prev_m['id']}/README.md)" if prev_m else "← Start"
    right = f"[{next_m['short']} →](../{next_m['id']}/README.md)" if next_m else "End"
    return f"{left} · [Course README](../README.md) · {right}"


def lab_badge(m: dict) -> str:
    if m["kind"] == "lab":
        return f"**Kind:** `lab` · Primary lab: `{m['lab']}` · **Shipped**"
    if m["kind"] == "offline":
        return "**Kind:** `offline` · Primary activity: local benchmark harness · **Planned**"
    return f"**Kind:** `{m['kind']}`"


def readme(m: dict, i: int) -> str:
    prev_m, next_m = prev_next(i)
    mid = m["id"]
    ss_aa = "-".join(mid.replace("module", "").split("-")[:2])
    header = (
        f"# {m['title']}\n\n"
        f"**Module id:** `{mid}`  \n"
        f"{lab_badge(m)}\n\n"
        f"{nav_line(prev_m, next_m)}\n\n"
        f"## Outcomes\n\n"
        f"After this module you can: **{m['outcomes']}**\n"
    )
    if m["kind"] == "lab":
        body = f"""
## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **{m['algorithm']}** on the tiny graphs.
2. Complete [CHECKLIST.md](CHECKLIST.md) with metrics (cutsize, balance, objective).
3. Optional self-check: `./scripts/module.sh {ss_aa} --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/{m['lab']}/index.html](http://127.0.0.1:8080/tools/{m['lab']}/index.html)
2. Tools shelf: open `{m['lab']}` from the platform tools index
3. Load the **starter graph**, run the algorithm, inspect metrics.
4. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach algorithm literacy on tiny instances — not production PDK flows.
"""
    elif m["kind"] == "offline":
        body = """
## Offline track

1. Follow [EXAMPLES.md](EXAMPLES.md) to run the local compare harness.
2. Record cutsize / balance / runtime against at least one external tool when available.
3. Complete [CHECKLIST.md](CHECKLIST.md).
"""
    else:
        body = """
## How to use this module

1. Read this README and the short transcript.
2. Complete [CHECKLIST.md](CHECKLIST.md).
3. Continue to the next module when the checklist feels honest.
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
    return header + body + media


def checklist(m: dict) -> str:
    if m["kind"] == "lab":
        return f"""# Checklist — {m['title']}

## Track A — Implement

- [ ] Worked through the prompts in [EXAMPLES.md](EXAMPLES.md)
- [ ] Implemented **{m['algorithm']}** end-to-end on the starter graph
- [ ] Reported cutsize, balance (or capacity), and objective score
- [ ] Can explain the algorithm steps without the UI

## Track B — Browser lab (`{m['lab']}`)

- [ ] Opened the lab (local or live)
- [ ] Loaded the starter graph
- [ ] Ran the algorithm and inspected metrics

## Done when

- [ ] I can reproduce the result on paper/code **or** I finished the browser challenges (preferably both)
"""
    if m["kind"] == "offline":
        return f"""# Checklist — {m['title']}

## Offline harness

- [ ] Ran the compare script on at least one shared instance
- [ ] Recorded toy-engine vs external metrics (or documented tool missing)
- [ ] Named one discrepancy and a hypothesis

## Done when

- [ ] I can explain how to judge partition quality across tools
"""
    if m["kind"] == "intro":
        return f"""# Checklist — {m['title']}

- [ ] I understand the course map (sections 01–05 + wrap)
- [ ] I know Track A (implement) vs Track B (browser lab)
- [ ] I opened [docs/MODULES.md](../docs/MODULES.md) once
- [ ] Ready for cutsize and balance
"""
    return f"""# Checklist — {m['title']}

- [ ] I can name the main algorithms from sections 01–04
- [ ] I know when KL/FM vs spectral vs multilevel fits
- [ ] I picked a next course (`learn_clustering`, `learn_floorplanning`, or `learn_placement`)
"""


def examples(m: dict) -> str:
    if m["kind"] == "lab":
        return f"""# Examples — {m['title']}

Track A (implement). Use tiny graphs first (8–30 nodes).

## Algorithm

**{m['algorithm']}**

## Starter prompts

1. Restate the algorithm in five bullets (inputs → loop → stop → output).
2. Run it on the 5-node weighted graph in `examples/tiny_graph.json` (create if missing).
3. Compute cutsize and balance after the run.
4. Change one parameter (seed, k, balance tolerance) and report what moved.
5. Name one failure mode (imbalance, local minimum, ignored terminals, …).

## Expected artifacts

- Partition assignment per node
- Cutsize and balance before and after
- Short note: why this algorithm belongs on the partitioning shelf

## Stretch

Scale to ~100 nodes; keep the same API as the tiny case.
"""
    if m["kind"] == "offline":
        return """# Examples — Offline benchmark compare

1. Export the same graph/netlist used in multilevel / hypergraph modules.
2. Run your toy partitioner; record cutsize, balance, wall time.
3. If available, run an open tool (e.g. KaHyPar / Metis-style flow) on the same instance.
4. Fill a comparison table: quality, balance, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
"""
    if m["kind"] == "intro":
        return """# Examples — Welcome

No coding yet.

1. Sketch where bipartition appears: floorplan chips, place multilevel, FPGA packing.
2. Write one sentence: “A good partition reduces cut while keeping parts balanced because …”
3. Name one difference between partitioning and clustering in EDA.
"""
    return """# Examples — Wrap

1. List three algorithms from this course and one strength each.
2. For fixed I/O pads, which module’s idea do you reach for first?
3. Write the bridge sentence you’ll need for clustering or floorplanning next.
"""


def transcript_lab(m: dict) -> str:
    return f"""# {m['title']}

**Module id:** {m['id']}
**Lab:** {m['lab']}
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — {m['title']}

Partitioning cuts a netlist or graph into parts that stay balanced while the edges or nets between parts stay as light as possible. In this module you’ll implement **{m['algorithm']}** end to end—not a sketch. By the end, you’ll run it on a tiny instance, report cutsize and balance, and know what the algorithm actually does.

## Slide 2 — The idea

Here’s the core idea in one breath: {m['algorithm']}. You’ll take a graph or hypergraph, apply the update rule until a stop condition, and emit a part assignment. Watch three numbers every time: the cut you minimize, the balance between parts, and any fixed terminals that constrain legal moves.

## Slide 3 — Browser lab track

In the browser lab track, open the **{m['lab']}** lab from the tools shelf. Load the starter graph, run the algorithm once, and read the metrics panel—cutsize, balance, and objective. Orient yourself, try one parameter change, then come back to implement the same loop yourself.

## Slide 4 — Implement track

In the implement track, open this module’s examples and build the full algorithm. Parse the tiny graph, run the core loop with clear stop rules, and print the assignment plus metrics. Prefer a deterministic seed so your golden answers stay stable. If something looks wrong, dump intermediate gains or part sizes—debugging the loop is part of the learning.

## Slide 5 — Pitfalls

Common traps: optimizing cut while ignoring balance; reporting pairwise cut when the instance is a hypergraph; forgetting locked terminals; and stopping too early on a local minimum. For KL and FM, remember locking and rollback. For multilevel flows, a bug in coarsening poisons every finer level.

## Slide 6 — Your turn

Complete the checklist for at least one track—preferably both. Implement the algorithm until your metrics match the expected range on the starter graph. When you’re ready, take the short quiz, then continue to the next module in this section.
"""


def transcript_intro() -> str:
    return """# Welcome to partitioning for EDA

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to partitioning for EDA

Physical design repeatedly asks: how do we cut a design into balanced pieces with few wires between them? That is partitioning. This course teaches bipartition and multiway algorithms as full implementations on tiny graphs—so you build literacy for floorplanning, placement multilevel, and FPGA packing later.

## Slide 2 — What you’ll build

You’ll start with cutsize and balance, then form an initial legal bipartition. Classic methods follow: Kernighan–Lin, Fiduccia–Mattheyses, spectral bipartition, and recursive bisection. Then multiway, terminal propagation, hypergraph cuts, and a multilevel V-cycle. One algorithm per lab. Full implementations at course scale—not production throughput, but complete and correct on the scoped instances.

## Slide 3 — Stable module ids

Module folders use hierarchical ids: section, then algorithm slot—like module two dash zero one for Kernighan–Lin. That way we can add algorithms later without renumbering everything. Odd slots leave room for inserts. Treat published ids as stable keys; display order lives in the module index.

## Slide 4 — Two tracks

Every lab module offers two practice tracks. Track A is implement: code the algorithm, run tiny graphs, report metrics. Track B is the browser lab shelf for visual intuition. A good rhythm is browser first for the idea, then implement to harden it. Intro and wrap modules have no lab.

## Slide 5 — How to move

For each module, read the README for outcomes, pick a track—or both—then work the checklist. Keep cutsize and balance as your habit. When this intro checklist is done, continue to cutsize and balance—the shared language every later algorithm will use.
"""


def transcript_wrap() -> str:
    return """# Partitioning path complete

**Module id:** module99-00-wrap
**Lab:** none (wrap)
**Tracks:** recap · next course

## Slide 1 — Partitioning path complete

You’ve walked the partitioning path—from metrics and initial cuts, through KL, FM, spectral, and recursive multiway work, into terminals, hypergraphs, and multilevel V-cycles, plus an offline compare habit. This wrap names what you can do now and where to go next.

## Slide 2 — What you can do now

You can form legal bipartitions, refine them with KL or FM, and explain cut versus balance trade-offs. You know when a graph model is enough and when a hyperedge model is required. You can respect fixed terminals and sketch a multilevel V-cycle. You are not shipping a foundry tool—you are building algorithm literacy for the PD stack.

## Slide 3 — Close the gaps

If you mainly watched browser labs, go back and finish at least one full implementation in foundations and one in classic bipartition. If you mainly coded, re-open any skipped visual labs. Either track works for self-study; both together stick best before floorplanning or placement.

## Slide 4 — Next courses

Natural next steps are learn clustering—for coarsening affinities that feed multilevel flows—and learn floorplanning or placement, where partitioned blocks become shapes and density. Keep your tiny-graph harness—you’ll reuse the I/O format.

## Slide 5 — Your turn

Review the wrap checklist. Name three algorithms and one strength each. Say which idea you’d use when pads are fixed on the chip boundary. When you’re ready, take the short quiz, then open the next course README.
"""


def transcript_offline() -> str:
    return """# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none (offline)
**Tracks:** offline harness

## Slide 1 — Offline benchmark compare

Toy engines teach mechanism. Benchmarks teach honesty. In this offline module you’ll run the same instances through your partitioner and, when available, an open external tool—then compare cutsize, balance, and runtime without pretending the numbers are foundry sign-off.

## Slide 2 — Fair compare rules

Use identical input. Fix seeds when the algorithm is randomized. Report the same metrics on both sides. If the external tool is missing, still run your harness and document the install gap—don’t invent golden numbers. A clean I/O contract matters more than a flashy chart.

## Slide 3 — What good looks like

Expect your educational engine to be slower and sometimes lower quality. That’s fine. You’re looking for the same qualitative behavior: balanced parts, improving cuts, and no silent illegal solutions. Huge unexplained wins usually mean a metric mismatch, not genius.

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
                    "Vendor GUI click-paths",
                    "Full implementations of partitioning algorithms on tiny instances",
                    "Foundry PDK certification",
                    "Writing UVM agents",
                ],
                "answer": 1,
                "explain": "Algorithm / toy-engine literacy on scoped graphs.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "A good partition usually ignores balance as long as cutsize is zero.",
                "answer": False,
                "explain": "Balance keeps parts usable for floorplan and place; empty cuts with one empty part are useless.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A good study rhythm is…",
                "choices": [
                    "Only memorize folder names",
                    "Browser intuition then implement metrics on tiny graphs",
                    "Skip checklists entirely",
                    "Start with multilevel before cutsize",
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
                "prompt": "Fixed I/O pads are handled most directly by…",
                "choices": [
                    "Ignoring them until routing",
                    "Terminal propagation / fixed-node constraints",
                    "Always spectral bipartition only",
                    "Increasing cutsize on purpose",
                ],
                "answer": 1,
                "explain": "Terminals pin nodes to parts and shape legal cuts.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "KL and FM improve an existing bipartition under a balance rule.",
                "answer": True,
                "explain": "They move or swap nodes to reduce cut while staying legal.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A natural next course after partitioning is…",
                "choices": [
                    "Only analog layout",
                    "Clustering, floorplanning, or placement",
                    "SPICE device models first",
                    "Ignore the PD stack",
                ],
                "answer": 1,
                "explain": "Those courses reuse cut, balance, and multilevel instincts.",
            },
        ]
        title = "Wrap check"
    elif m["kind"] == "offline":
        items = [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Fair compares require the same input instance and the same reported metrics.",
                "answer": True,
                "explain": "Otherwise you compare different problems.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "If an external tool is missing you should…",
                "choices": [
                    "Invent golden numbers",
                    "Still run your harness and document the gap",
                    "Delete your metrics",
                    "Skip the module forever",
                ],
                "answer": 1,
                "explain": "Honesty about tooling beats fake goldens.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "An educational partitioner that is slower than Metis is automatically wrong.",
                "answer": False,
                "explain": "Speed differs; look for legal, balanced, improving cuts.",
            },
        ]
        title = "Offline check"
    else:
        algo = m["algorithm"] or m["title"]
        items = [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": f"This lab’s primary algorithm is…",
                "choices": [
                    algo,
                    "Vendor place-and-route GUI only",
                    "SPICE transient analysis",
                    "Scan-chain stitching",
                ],
                "answer": 0,
                "explain": f"Focus: {algo}.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "Cutsize alone is enough; balance can be ignored in this course.",
                "answer": False,
                "explain": "Every partition lab reports cut and balance together.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "After running the algorithm you should report…",
                "choices": [
                    "Only a screenshot of the UI",
                    "Part assignment plus cutsize and balance",
                    "Only runtime",
                    "Nothing — intuition is enough",
                ],
                "answer": 1,
                "explain": "Assignment + metrics are the contract.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": f"Track A asks you to implement {algo} on a tiny graph.",
                "answer": True,
                "explain": "Implement track hardens the idea.",
            },
        ]
        title = f"{m['short']} check"
    return {
        "id": m["id"],
        "title": title,
        "items": items,
    }


def outline_stub(m: dict) -> str:
    return f"""title: "{m['title']}"
footer: "learn_partitioning — {m['short']}"
slides:
  - type: title
    title: "{m['title']}"
    subtitle: "{m['id']} · learn_partitioning"
    notes: |
      Stub — replace via transcript_to_outline.py after revising transcript.md.
"""


def write_modules_md() -> None:
    rows = []
    for m in MODULES:
        lab = f"`{m['lab']}`" if m["lab"] else ("offline harness" if m["kind"] == "offline" else "—")
        status = "**ref**" if m["kind"] == "lab" else m["status"]
        rows.append(
            f"| `{m['id']}` | `{m['kind']}` | [{m['title']}](../{m['id']}/README.md) | {lab} | {status} |"
        )
    text = f"""# learn_partitioning — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.
Published ids are **stable keys**; order below is the teaching path.

Status: **ref** = browser lab shipped under `platform/tools/` (algorithm modules).

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
{chr(10).join(rows)}

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (cutsize/balance, initial bipartition) |
| `02` | Classic bipartition (KL, FM, spectral, recursive) |
| `03` | Multiway, terminals, hypergraph |
| `04` | Multilevel V-cycle |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs (PPT / transcript)

When walkthrough frames exist: each lab module may have `assets/STEPS.md` and `assets/steps/*.png`.

**Build media in WSL** (LibreOffice + edge-tts + ffmpeg):

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_partitioning/scripts/build_all_media.sh
```
"""
    write(ROOT / "docs" / "MODULES.md", text)


def write_docs() -> None:
    write(
        ROOT / "docs" / "SCOPE.md",
        """# Scope — learn_partitioning

## In scope

- Full implementations of bipartition and multiway partitioning algorithms on tiny-to-medium instances
- Metrics: edge cutsize, hyperedge cut, balance / part sizes
- Terminal / fixed-node constraints and multilevel V-cycles
- Offline compare habits against open tools when available

## Out of scope (v1)

- Drop-in replacement for commercial partitioners (hMETIS / KaHyPar production)
- Foundry PDK certification or production sign-off
- Clustering affinities as the spine (see `learn_clustering`)
- Vendor GUI workflows

## “Full implementation” means

Complete and correct for the **scoped problem size** (tens to low hundreds of nodes/nets): parse input, run the algorithm, emit assignment + metrics, with tests—not a production-scale engine.
""",
    )
    write(
        ROOT / "docs" / "TWO_TRACKS.md",
        """# Two tracks — learn_partitioning

| Track | Surface | Job |
|-------|---------|-----|
| **A — Implement** | `EXAMPLES.md`, tiny graphs under each module | Code the full algorithm; report cutsize + balance |
| **B — Browser lab** | `platform/tools/<lab-id>/` | Visual intuition; starter + challenges |

Intro / wrap have no lab. Offline module is harness-only.

Prefer: browser once for the idea → implement until metrics match.
""",
    )


def write_course_readme() -> None:
    table = "\n".join(
        f"| {m['id']} — {m['title']} | [{m['id']}]({m['id']}/README.md) |" for m in MODULES
    )
    write(
        ROOT / "README.md",
        f"""# learn_partitioning

[![Role](https://img.shields.io/badge/role-course%20scaffold-orange)](../../eda.md)
[![Domain](https://img.shields.io/badge/domain-EDA%20partitioning%20%7C%20cutsize%20%7C%20KL%2FFM-purple)](docs/MODULES.md)

**learn_partitioning** is the open learning path for *bipartition and multiway partitioning algorithms used in EDA physical design*—one full algorithm per lab, on tiny instances.

- Scope: [docs/SCOPE.md](docs/SCOPE.md)
- Modules: [docs/MODULES.md](docs/MODULES.md)
- Tracks: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md)

## Contents

```text
learn_partitioning/
├── README.md
├── common/         # graph I/O, metrics, reference helpers
├── docs/           # MODULES, TWO_TRACKS, SCOPE
├── scripts/        # scaffold_course.py, build_all_media.sh
├── module00-00-intro/
├── …
└── module99-00-wrap/
```

Module folders use **hierarchical ids** `moduleSS-AA-slug` so algorithms can be added later without renumbering.

## Two learning tracks

| Track | Practice surface |
|-------|------------------|
| **A** | Implement full algorithms on tiny graphs (`EXAMPLES.md`) |
| **B** | Browser labs under `platform/tools/` |

## Module landings

Full table: **[docs/MODULES.md](docs/MODULES.md)**.

| Module | Landing |
|--------|---------|
{table}

## Author: module-slides

From the monorepo root (WSL):

```bash
python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \\
  courses/learn_partitioning/module01-01-cutsize-balance
python3 .cursor/skills/module-slides/scripts/build_pptx.py \\
  courses/learn_partitioning/module01-01-cutsize-balance
bash courses/learn_partitioning/scripts/build_all_media.sh
```

## License

Course materials intended for CC BY 4.0 alignment with the digital_learning courses (add `LICENSE` when publishing).
""",
    )


def write_common() -> None:
    write(
        ROOT / "common" / "README.md",
        """# common — learn_partitioning

Shared Track A helpers (Python) for tiny graphs and metrics.

Suggested layout as you flesh reference solvers:

- `graph_io.py` — load/save tiny JSON graphs
- `metrics.py` — cutsize, balance
- `goldens/` — expected assignments for starter instances

Browser algorithms live in `platform/assets/partitioning-core.js` (and clustering-core for KL/FM/spectral).
""",
    )
    write(
        ROOT / "common" / "tiny_graph.json",
        json.dumps(
            {
                "nodes": ["A", "B", "C", "D", "E"],
                "edges": [
                    {"u": "A", "v": "B", "w": 5},
                    {"u": "B", "v": "C", "w": 1},
                    {"u": "C", "v": "D", "w": 1},
                    {"u": "D", "v": "E", "w": 5},
                    {"u": "A", "v": "E", "w": 1},
                    {"u": "B", "v": "D", "w": 2},
                ],
            },
            indent=2,
        )
        + "\n",
    )


def write_build_script() -> None:
    write(
        ROOT / "scripts" / "build_all_media.sh",
        """#!/usr/bin/env bash
# Build PPTX → PDF → audio → video for all learn_partitioning modules (Unix/WSL only).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SKILL="$ROOT/.cursor/skills/module-slides/scripts"
# shellcheck source=/dev/null
source "$SKILL/_require_unix.sh"

COURSE="$ROOT/courses/learn_partitioning"
NO_VIDEO=0
if [[ "${1:-}" == "--no-video" ]]; then NO_VIDEO=1; fi

mapfile -t MODS < <(find "$COURSE" -maxdepth 1 -type d -name 'module*' | sort)
echo "Modules: ${#MODS[@]}"
for d in "${MODS[@]}"; do
  echo "=== $(basename "$d") ==="
  python3 "$SKILL/transcript_to_outline.py" "$d"
  python3 "$SKILL/build_pptx.py" "$d"
  bash "$SKILL/pptx_to_pdf.sh" "$d/slides.pptx" || true
  if [[ "$NO_VIDEO" -eq 1 ]]; then
    bash "$SKILL/synthesize_audio.sh" "$d" || true
  else
    bash "$SKILL/narrate_clips.sh" "$d" || true
  fi
done
echo "Done. Publish: python3 platform/scripts/publish_course_platform.py learn_partitioning"
""",
    )


def main() -> None:
    write_docs()
    write_modules_md()
    write_course_readme()
    write_common()
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
            ex = base / "examples"
            ex.mkdir(parents=True, exist_ok=True)
            (ex / "tiny_graph.json").write_text(
                (ROOT / "common" / "tiny_graph.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        print(f"ok {mid}")
    print(f"Scaffolded {len(MODULES)} modules under {ROOT}")


if __name__ == "__main__":
    main()
