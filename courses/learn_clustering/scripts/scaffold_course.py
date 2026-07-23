#!/usr/bin/env python3
"""Scaffold learn_clustering modules (hierarchical SS-AA ids) with module-slides stubs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Display order; odd AA slots leave room for later algorithms.
MODULES = [
    {
        "id": "module00-00-intro",
        "kind": "intro",
        "title": "Welcome to clustering for EDA",
        "short": "Welcome",
        "lab": None,
        "status": "—",
        "section": "00",
        "outcomes": "Explain why clustering exists in physical design and how this course is organized.",
        "algorithm": None,
    },
    {
        "id": "module01-01-affinity-metrics",
        "kind": "lab",
        "title": "Affinity metrics",
        "short": "Affinity",
        "lab": "affinity-metrics",
        "status": "P",
        "section": "01",
        "outcomes": "Define and compute edge affinity / similarity scores used by later clustering algorithms.",
        "algorithm": "affinity scoring (edge weight, pin-count, connectivity)",
    },
    {
        "id": "module01-03-greedy-pair-merge",
        "kind": "lab",
        "title": "Greedy pair merge",
        "short": "Greedy merge",
        "lab": "greedy-pair-merge",
        "status": "P",
        "section": "01",
        "outcomes": "Implement heaviest-edge / greedy pair merging and evaluate cutsize after merges.",
        "algorithm": "greedy pair merge (heaviest-edge matching coarsening)",
    },
    {
        "id": "module01-05-size-constrained-agglomerative",
        "kind": "lab",
        "title": "Size-constrained agglomerative clustering",
        "short": "Constrained agglomerative",
        "lab": "size-constrained-agglomerative",
        "status": "P",
        "section": "01",
        "outcomes": "Implement agglomerative clustering with hard capacity / area constraints.",
        "algorithm": "size-constrained agglomerative clustering",
    },
    {
        "id": "module02-01-label-propagation",
        "kind": "lab",
        "title": "Label propagation clustering",
        "short": "Label propagation",
        "lab": "label-propagation",
        "status": "P",
        "section": "02",
        "outcomes": "Implement asynchronous / synchronous label propagation on a weighted graph.",
        "algorithm": "label propagation clustering",
    },
    {
        "id": "module02-03-spectral-bisection",
        "kind": "lab",
        "title": "Spectral bisection",
        "short": "Spectral bisection",
        "lab": "spectral-bisection",
        "status": "P",
        "section": "02",
        "outcomes": "Build the Laplacian, take the Fiedler vector, and bisect with balance constraints.",
        "algorithm": "spectral bisection (Laplacian / Fiedler)",
    },
    {
        "id": "module02-05-kernighan-lin",
        "kind": "lab",
        "title": "Kernighan–Lin refinement",
        "short": "Kernighan–Lin",
        "lab": "kernighan-lin",
        "status": "P",
        "section": "02",
        "outcomes": "Implement full KL pair-swap refinement with gains, locking, and rollback to best prefix.",
        "algorithm": "Kernighan–Lin (KL) refinement",
    },
    {
        "id": "module02-07-fiduccia-mattheyses",
        "kind": "lab",
        "title": "Fiduccia–Mattheyses refinement",
        "short": "Fiduccia–Mattheyses",
        "lab": "fiduccia-mattheyses",
        "status": "P",
        "section": "02",
        "outcomes": "Implement full FM single-vertex moves with bucketed gains and balance constraints.",
        "algorithm": "Fiduccia–Mattheyses (FM) refinement",
    },
    {
        "id": "module03-01-multilevel-clustering",
        "kind": "lab",
        "title": "Multilevel clustering",
        "short": "Multilevel",
        "lab": "multilevel-clustering",
        "status": "P",
        "section": "03",
        "outcomes": "Implement a full V-cycle: coarsen, initial partition, project, and refine.",
        "algorithm": "multilevel coarsen / initial / uncoarsen / refine",
    },
    {
        "id": "module03-03-hypergraph-clustering",
        "kind": "lab",
        "title": "Hypergraph clustering",
        "short": "Hypergraph",
        "lab": "hypergraph-clustering",
        "status": "P",
        "section": "03",
        "outcomes": "Model nets as hyperedges and cluster / cut with a hypergraph objective.",
        "algorithm": "hypergraph clustering / netlist cut modeling",
    },
    {
        "id": "module04-01-congestion-aware-clustering",
        "kind": "lab",
        "title": "Congestion-aware clustering",
        "short": "Congestion-aware",
        "lab": "congestion-aware-clustering",
        "status": "P",
        "section": "04",
        "outcomes": "Extend the objective with a congestion penalty and re-run clustering under that cost.",
        "algorithm": "congestion-penalized clustering objective",
    },
    {
        "id": "module04-03-timing-aware-clustering",
        "kind": "lab",
        "title": "Timing-aware clustering",
        "short": "Timing-aware",
        "lab": "timing-aware-clustering",
        "status": "P",
        "section": "04",
        "outcomes": "Weight edges by timing criticality / slack and optimize a timing-aware objective.",
        "algorithm": "timing-weighted clustering objective",
    },
    {
        "id": "module05-01-offline-benchmark-compare",
        "kind": "offline",
        "title": "Offline benchmark compare",
        "short": "Offline compare",
        "lab": None,
        "status": "P",
        "section": "05",
        "outcomes": "Compare toy engines against open hypergraph / partitioning tools on shared instances.",
        "algorithm": "benchmark harness vs external tools",
    },
    {
        "id": "module99-00-wrap",
        "kind": "wrap",
        "title": "Clustering path complete",
        "short": "Wrap",
        "lab": None,
        "status": "—",
        "section": "99",
        "outcomes": "Recap algorithm trade-offs and choose the next course (partitioning / floorplanning).",
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
    left = (
        f"[← {prev_m['short']}](../{prev_m['id']}/README.md)"
        if prev_m
        else "← Start"
    )
    right = (
        f"[{next_m['short']} →](../{next_m['id']}/README.md)"
        if next_m
        else "End"
    )
    return f"{left} · [Course README](../README.md) · {right}"


def lab_badge(m: dict) -> str:
    if m["kind"] == "lab":
        return f"**Kind:** `lab` · Primary lab: `{m['lab']}` · **Planned**"
    if m["kind"] == "offline":
        return "**Kind:** `offline` · Primary activity: local benchmark harness · **Planned**"
    return f"**Kind:** `{m['kind']}`"


def readme(m: dict, i: int) -> str:
    prev_m, next_m = prev_next(i)
    mid = m["id"]
    title = m["title"]
    lines = [
        f"# Module {mid.split('-', 1)[0].replace('module', '')}-{'-'.join(mid.split('-')[1:3]) if mid.count('-') >= 2 else ''}: {title}".replace(
            "Module 00-00: ", "Module 00-00: "
        ),
        "",
        lab_badge(m),
        "",
        nav_line(prev_m, next_m),
        "",
        "## Outcomes",
        "",
        f"After this module you can: **{m['outcomes']}**",
        "",
    ]
    # Clean title header to match digital style better
    ss_aa = "-".join(mid.split("-")[:2]).replace("module", "")
    # Actually use clearer header
    header = f"# {m['title']}\n\n**Module id:** `{mid}`  \n{lab_badge(m)}\n\n{nav_line(prev_m, next_m)}\n\n## Outcomes\n\nAfter this module you can: **{m['outcomes']}**\n"
    body = ""
    if m["kind"] == "lab":
        body = f"""
## Two tracks (pick one or both)

### Track A — Implement (hands-on)

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **{m['algorithm']}** on the tiny graphs.
2. Complete [CHECKLIST.md](CHECKLIST.md) with metrics (cutsize, balance, objective).
3. Optional self-check: `./scripts/module.sh {ss_aa} --check` (from course root).

### Track B — Browser lab (online)

1. Local: `http://127.0.0.1:8080/tools/{m['lab']}/index.html` *(planned)*
2. Live: tools shelf entry `{m['lab']}` *(planned)*
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
    media = """
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
""".format(mid=mid)
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

- [ ] Opened the lab (local or live) — or noted Coming soon and used Track A
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

- [ ] I can explain how to judge clustering quality across tools
"""
    if m["kind"] == "intro":
        return f"""# Checklist — {m['title']}

- [ ] I understand the course map (sections 01–05 + wrap)
- [ ] I know Track A (implement) vs Track B (browser lab)
- [ ] I opened [docs/MODULES.md](../docs/MODULES.md) once
- [ ] Ready for affinity metrics
"""
    return f"""# Checklist — {m['title']}

- [ ] I can name the main algorithms from sections 01–04
- [ ] I know when greedy merge vs multilevel vs hypergraph fits
- [ ] I picked a next course (`learn_partitioning` or `learn_floorplanning`)
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
3. Compute cutsize (or hyperedge cut) and balance after the run.
4. Change one parameter (capacity, seed, or stop rule) and report what moved.
5. Name one failure mode (oscillation, imbalance, local minimum, …).

## Expected artifacts

- Cluster / partition assignment per node
- Objective score before and after
- Short note: why this algorithm belongs in the EDA clustering shelf

## Stretch

Scale to ~100 nodes; keep the same API as the tiny case.
"""
    if m["kind"] == "offline":
        return """# Examples — Offline benchmark compare

1. Export the same netlist/graph used in multilevel / hypergraph modules.
2. Run your toy engine; record cutsize, balance, wall time.
3. If available, run an open tool (e.g. KaHyPar / hMETIS-style flow) on the same instance.
4. Fill a comparison table: quality, balance, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
"""
    if m["kind"] == "intro":
        return """# Examples — Welcome

No coding yet.

1. Sketch the EDA path: IR → synth → timing → place → route → verify.
2. Mark where clustering / coarsening usually appears (partition, place multilevel, CTS hierarchy).
3. Write one sentence: “Clustering reduces problem size by …”
"""
    return """# Examples — Wrap

1. List three algorithms from this course and one strength each.
2. For a netlist with huge nets, which module’s model do you reach for first?
3. Write the bridge sentence you’ll need for partitioning or floorplanning next.
"""


def transcript_lab(m: dict) -> str:
    title = m["title"]
    algo = m["algorithm"]
    lab = m["lab"]
    return f"""# {title}

**Module id:** {m['id']}
**Lab:** {lab}
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — {title}

Clustering is how EDA engines shrink a netlist or graph into groups that stay together. In this module you’ll implement **{algo}** end to end—not a sketch. By the end, you’ll run it on a tiny instance, report metrics, and know what the algorithm actually does.

## Slide 2 — The idea

Here’s the core idea in one breath: {algo}. You’ll take a graph or hypergraph, apply the update rule until a stop condition, and emit a cluster assignment. Watch three numbers every time: the objective you optimize, the cut between clusters, and balance or capacity so groups don’t grow without limit.

## Slide 3 — Browser lab track

In the browser lab track, open the **{lab}** lab from the tools shelf when it ships. Load the starter graph, run the algorithm once, and read the metrics panel—cutsize, balance, and objective. You don’t need a full UI tour. Orient yourself, try one parameter change, then come back to implement the same loop yourself.

## Slide 4 — Implement track

In the implement track, open this module’s examples and build the full algorithm. Parse the tiny graph, run the core loop with clear stop rules, and print the assignment plus metrics. Prefer a deterministic seed so your golden answers stay stable. If something looks wrong, dump intermediate gains or labels—debugging the loop is part of the learning.

## Slide 5 — Pitfalls

Common traps: forgetting balance so one cluster eats everything; using an objective that doesn’t match the cut you report; and stopping too early on a local minimum. For refinement algorithms, remember locking and rollback. For multilevel flows, remember that a bug in coarsening poisons every finer level.

## Slide 6 — Your turn

Complete the checklist for at least one track—preferably both. Implement the algorithm until your metrics match the expected range on the starter graph. When you’re ready, take the short quiz, then continue to the next module in this section.
"""


def transcript_intro() -> str:
    return """# Welcome to clustering for EDA

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to clustering for EDA

Physical design engines almost never optimize a flat million-cell problem in one shot. They cluster, coarsen, and refine. This course teaches those algorithms as full implementations on tiny graphs—so you build literacy for partitioning, placement, and multilevel flows later.

## Slide 2 — What you’ll build

You’ll move through foundations—affinity and greedy merges—then classic methods like label propagation, spectral bisection, Kernighan–Lin, and Fiduccia–Mattheyses. Then multilevel and hypergraph models, then congestion- and timing-aware objectives. One algorithm per lab. Full implementations at course scale—not production throughput, but complete and correct on the scoped instances.

## Slide 3 — Stable module ids

Module folders use hierarchical ids: section, then algorithm slot—like module two dash zero five for Kernighan–Lin. That way we can add algorithms later without renumbering everything. Odd slots are reserved so inserts stay clean. Treat published ids as stable keys; display order lives in the module index.

## Slide 4 — Two tracks

Every lab module offers two practice tracks. Track A is implement: code the algorithm, run tiny graphs, report metrics. Track B is the browser lab shelf for visual intuition when those labs ship. A good rhythm is browser first for the idea, then implement to harden it. Intro and wrap modules have no lab.

## Slide 5 — How to move

For each module, read the README for outcomes, pick a track—or both—then work the checklist. Keep cutsize, balance, and objective as your habit. When this intro checklist is done, continue to affinity metrics—the shared scoring language every later algorithm will use.
"""


def transcript_wrap() -> str:
    return """# Clustering path complete

**Module id:** module99-00-wrap
**Lab:** none (wrap)
**Tracks:** recap · next course

## Slide 1 — Clustering path complete

You’ve walked the clustering path—from affinity and greedy merges, through classic refinement and multilevel hypergraph models, into congestion- and timing-aware objectives, plus an offline compare habit. This wrap names what you can do now and where to go next.

## Slide 2 — What you can do now

You can implement and evaluate the main clustering algorithms on tiny instances. You can explain cutsize versus balance trade-offs, when a graph model is enough, and when a hyperedge model is required. You can refine a partition with KL or FM, and you know why multilevel V-cycles exist. You are not shipping a foundry tool—you are building algorithm literacy for the PD stack.

## Slide 3 — Close the gaps

If you mainly watched or used browser stubs, go back and finish at least one full implementation in foundations and one in refinement. If you mainly coded, re-open any skipped visual labs when they ship. Either track works for self-study; both together stick best before partitioning or floorplanning.

## Slide 4 — Next courses

Natural next steps are learn partitioning—for cut-focused bipartition and multiway work—and learn floorplanning, where clustered blocks become shapes and whitespace. Congestion and placement courses will reuse the same affinity and multilevel instincts. Pick one path and keep your tiny-graph harness—you’ll reuse the I/O format.

## Slide 5 — Your turn

Review the wrap checklist. Name three algorithms and one strength each. Say which model you’d use for a netlist with huge high-fanout nets. When you’re ready, take the short quiz, then open the next course README.
"""


def transcript_offline() -> str:
    return """# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none (offline)
**Tracks:** offline harness

## Slide 1 — Offline benchmark compare

Toy engines teach mechanism. Benchmarks teach honesty. In this offline module you’ll run the same instances through your clustering code and, when available, an open external tool—then compare cutsize, balance, and runtime without pretending the numbers are foundry sign-off.

## Slide 2 — Fair compare rules

Use identical input. Fix seeds when the algorithm is randomized. Report the same metrics on both sides. If the external tool is missing, still run your harness and document the install gap—don’t invent golden numbers. A clean I/O contract matters more than a flashy chart.

## Slide 3 — What good looks like

Expect your educational engine to be slower and sometimes lower quality. That’s fine. You’re looking for the same qualitative behavior: balanced clusters, improving objectives, and no silent illegal solutions. Huge unexplained wins usually mean a metric mismatch, not genius.

## Slide 4 — Your turn

Follow the examples file, fill the comparison table, and finish the checklist. Bring one discrepancy and a short hypothesis into your notes. Then continue to the wrap module to close the course.
"""


def quiz(m: dict) -> dict:
    mid = m["id"]
    if m["kind"] == "intro":
        items = [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "This course focuses primarily on…",
                "choices": [
                    "Vendor GUI click-paths",
                    "Full implementations of clustering algorithms on tiny instances",
                    "Foundry PDK certification",
                    "Writing UVM agents",
                ],
                "answer": 1,
                "explain": "Algorithm / toy-engine literacy on scoped graphs.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "Hierarchical module ids (section + algorithm slot) are meant to stay stable when new algorithms are added later.",
                "answer": True,
                "explain": "Ids are stable keys; display order is in MODULES.md.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A good study rhythm is…",
                "choices": [
                    "Only memorize folder names",
                    "Browser intuition then implement metrics on tiny graphs",
                    "Skip checklists entirely",
                    "Start with timing-aware before affinity",
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
                "prompt": "Huge high-fanout nets are modeled most naturally by…",
                "choices": [
                    "Only pairwise graph edges",
                    "Hyperedges / hypergraph clustering",
                    "Ignoring connectivity",
                    "Always one cell per cluster",
                ],
                "answer": 1,
                "explain": "Nets span many pins; hypergraphs capture that.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "KL and FM are refinement methods that improve an existing partition.",
                "answer": True,
                "explain": "They move or swap nodes to reduce cut under balance.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A natural next course after clustering is…",
                "choices": [
                    "learn_partitioning or learn_floorplanning",
                    "learn_uart only",
                    "Vendor Innovus certification only",
                    "Skipping metrics forever",
                ],
                "answer": 0,
                "explain": "Partitioning and floorplanning reuse clustering instincts.",
            },
        ]
        title = "Wrap check"
    elif m["kind"] == "offline":
        items = [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Fair compares require the same input instance and comparable metrics on both engines.",
                "answer": True,
                "explain": "Otherwise you compare different problems.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "If the external tool is missing, you should…",
                "choices": [
                    "Invent golden numbers",
                    "Still validate harness I/O and document the gap",
                    "Delete your toy engine",
                    "Skip metrics",
                ],
                "answer": 1,
                "explain": "Honesty beats fake goldens.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A huge unexplained quality win usually suggests…",
                "choices": [
                    "Always a better algorithm",
                    "Possible metric or input mismatch",
                    "That balance does not matter",
                    "That runtime is irrelevant to report",
                ],
                "answer": 1,
                "explain": "Check definitions before celebrating.",
            },
        ]
        title = "Offline compare check"
    else:
        items = [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": f"This module’s primary algorithm is…",
                "choices": [
                    m["algorithm"],
                    "Gate-level SDF annotation",
                    "UVM phase jumping",
                    "Liberty CCSP parsing",
                ],
                "answer": 0,
                "explain": "One algorithm per lab.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "You should report cutsize (or hyperedge cut) and balance/capacity along with the objective.",
                "answer": True,
                "explain": "Quality without balance is often illegal or useless.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "Course-scale “full implementation” means…",
                "choices": [
                    "Drop-in replacement for commercial P&R",
                    "Complete correct algorithm on scoped tiny/medium instances",
                    "Only pseudocode comments",
                    "GUI macros only",
                ],
                "answer": 1,
                "explain": "Complete and correct at learning scale.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": f"Track A asks you to implement {m['algorithm']} end-to-end, not only click a demo.",
                "answer": True,
                "explain": "Implement track is the fidelity path.",
            },
        ]
        title = f"{m['short']} check"
    return {
        "module": mid,
        "title": title,
        "passing_score": 0.67,
        "items": items,
    }


def modules_md() -> str:
    rows = [
        "# learn_clustering — module index",
        "",
        "Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).",
        "Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.",
        "Published ids are **stable keys**; order below is the teaching path.",
        "",
        "| Id | Kind | Module | Lab / activity | Status |",
        "|----|------|--------|----------------|--------|",
    ]
    for m in MODULES:
        lab = f"`{m['lab']}`" if m["lab"] else ("offline harness" if m["kind"] == "offline" else "—")
        rows.append(
            f"| `{m['id']}` | `{m['kind']}` | [{m['title']}](../{m['id']}/README.md) | {lab} | {m['status']} |"
        )
    rows += [
        "",
        "## Sections",
        "",
        "| Section | Focus |",
        "|---------|--------|",
        "| `00` | Intro |",
        "| `01` | Foundations (affinity, greedy, constrained agglomerative) |",
        "| `02` | Classic methods (LP, spectral, KL, FM) |",
        "| `03` | Multilevel + hypergraph |",
        "| `04` | EDA-aware objectives (congestion, timing) |",
        "| `05` | Offline evidence |",
        "| `99` | Wrap |",
        "",
        "## Dual tracks",
        "",
        "See [TWO_TRACKS.md](TWO_TRACKS.md).",
        "",
    ]
    return "\n".join(rows)


def two_tracks() -> str:
    return """# Two learning tracks

## Track A — Implement

Practice by coding the full algorithm on tiny graphs.

- Prompts live under each `moduleSS-AA-*/EXAMPLES.md`
- Self-check: `./scripts/module.sh SS-AA --check` (e.g. `01-03`)

Use this track when you need **fidelity**: data structures, loops, stop rules, and metrics you can reproduce.

## Track B — Browser lab

Practice in the learning platform concept labs (when shipped).

- Local tools: http://127.0.0.1:8080/tools/
- Each lab module README names its primary lab id
- Planned labs show **P** in [MODULES.md](MODULES.md); use Track A until they ship

Use this track for **intuition** and quick visual feedback.

## Recommended path

1. **Track B** starter (if shipped) — 5–10 min
2. **Track A** implement + metrics — 20–45 min
3. Optional quiz / transcript review

Doing only Track A is OK for self-study while browser labs are planned.
"""


def scope_md() -> str:
    return """# Scope — learn_clustering

## In scope

- Full implementations of clustering / coarsening / refinement algorithms on tiny-to-medium instances
- Graph and hypergraph models used in EDA multilevel flows
- Metrics: cutsize (or hyperedge cut), balance/capacity, objective, runtime
- Offline compare habits against open tools when available

## Out of scope (v1)

- Drop-in replacement for commercial physical design tools
- Foundry PDK certification or production sign-off
- Research ML-EDA as the spine of this course
- Vendor GUI workflows

## “Full implementation” means

Complete and correct for the **scoped problem size** (tens to low hundreds of nodes/nets): parse input, run the algorithm, emit assignment + metrics, with tests—not a production-scale engine.
"""


def course_readme() -> str:
    landings = "\n".join(
        f"| {m['id']} — {m['title']} | [{m['id']}]({m['id']}/README.md) |"
        for m in MODULES
    )
    return f"""# learn_clustering

[![Role](https://img.shields.io/badge/role-course%20scaffold-orange)](../../eda.md)
[![Domain](https://img.shields.io/badge/domain-EDA%20clustering%20%7C%20multilevel%20%7C%20cutsize-purple)](docs/MODULES.md)

**learn_clustering** is the open learning path for *clustering / coarsening algorithms used in EDA physical design*—one full algorithm per lab, on tiny instances.

- Scope: [docs/SCOPE.md](docs/SCOPE.md)
- Modules: [docs/MODULES.md](docs/MODULES.md)
- Tracks: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md)

## Contents

```text
learn_clustering/
├── README.md
├── docs/           # MODULES, TWO_TRACKS, SCOPE
├── scripts/        # module.sh, scaffold_course.py
├── module00-00-intro/
├── module01-01-affinity-metrics/
├── …
└── module99-00-wrap/
```

Module folders use **hierarchical ids** `moduleSS-AA-slug` so algorithms can be added later without renumbering.

## Two learning tracks

| Track | Practice surface |
|-------|------------------|
| **A** | Implement full algorithms on tiny graphs (`EXAMPLES.md`) |
| **B** | Browser labs on the tools shelf *(planned)* |

## Module landings

Full table: **[docs/MODULES.md](docs/MODULES.md)**.

| Module | Landing |
|--------|---------|
{landings}

## Author: module-slides

From the monorepo root:

```bash
python .cursor/skills/module-slides/scripts/transcript_to_outline.py \\
  courses/learn_clustering/module01-01-affinity-metrics
python .cursor/skills/module-slides/scripts/build_pptx.py \\
  courses/learn_clustering/module01-01-affinity-metrics
```

## License

Course materials intended for CC BY 4.0 alignment with the digital_learning courses (add `LICENSE` when publishing).
"""


def module_sh() -> str:
    return r"""#!/usr/bin/env bash
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
    ;;
  --demo)
    echo "Demo: open $MOD_DIR/EXAMPLES.md and README.md"
    ;;
  *)
    echo "Unknown option: $ACTION"
    exit 1
    ;;
esac
"""


def tiny_graph() -> str:
    return """{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"u": "A", "v": "B", "w": 5},
    {"u": "A", "v": "C", "w": 1},
    {"u": "B", "v": "C", "w": 4},
    {"u": "C", "v": "D", "w": 2},
    {"u": "D", "v": "E", "w": 5},
    {"u": "C", "v": "E", "w": 1}
  ],
  "node_sizes": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1},
  "notes": "Natural clusters often emerge as {A,B,C} and {D,E}."
}
"""


def main() -> None:
    write(ROOT / "README.md", course_readme())
    write(ROOT / "docs" / "MODULES.md", modules_md())
    write(ROOT / "docs" / "TWO_TRACKS.md", two_tracks())
    write(ROOT / "docs" / "SCOPE.md", scope_md())
    write(ROOT / "scripts" / "module.sh", module_sh())

    for i, m in enumerate(MODULES):
        d = ROOT / m["id"]
        write(d / "README.md", readme(m, i))
        write(d / "CHECKLIST.md", checklist(m))
        write(d / "EXAMPLES.md", examples(m))
        if m["kind"] == "intro":
            write(d / "transcript.md", transcript_intro())
        elif m["kind"] == "wrap":
            write(d / "transcript.md", transcript_wrap())
        elif m["kind"] == "offline":
            write(d / "transcript.md", transcript_offline())
        else:
            write(d / "transcript.md", transcript_lab(m))
            write(d / "examples" / "tiny_graph.json", tiny_graph())
        write(d / "quiz.json", json.dumps(quiz(m), indent=2))

    print(f"Scaffolded {len(MODULES)} modules under {ROOT}")


if __name__ == "__main__":
    main()
