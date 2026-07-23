#!/usr/bin/env python3
"""Scaffold learn_sta modules (hierarchical SS-AA ids) with module-slides stubs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODULES = [
    {
        "id": "module00-00-intro",
        "kind": "intro",
        "title": "Welcome to static timing analysis",
        "short": "Welcome",
        "lab": None,
        "status": "—",
        "section": "00",
        "outcomes": "Explain why STA exists in the digital flow and how this course is organized.",
        "algorithm": None,
    },
    {
        "id": "module01-01-timing-graph",
        "kind": "lab",
        "title": "Timing graph",
        "short": "Timing graph",
        "lab": "timing-graph",
        "status": "P",
        "section": "01",
        "outcomes": "Build a levelized timing graph from a tiny netlist and name pin/net delay arcs.",
        "algorithm": "timing-graph construction and levelization",
    },
    {
        "id": "module01-03-arrival-required",
        "kind": "lab",
        "title": "Arrival and required times",
        "short": "Arrival / required",
        "lab": "arrival-required",
        "status": "P",
        "section": "01",
        "outcomes": "Propagate arrival forward and required backward on a timing graph with fixed clocks.",
        "algorithm": "forward arrival and backward required propagation",
    },
    {
        "id": "module02-01-slack-setup-hold",
        "kind": "lab",
        "title": "Slack, setup, and hold",
        "short": "Slack / setup / hold",
        "lab": "slack-setup-hold",
        "status": "P",
        "section": "02",
        "outcomes": "Compute setup and hold slack at endpoints and explain the sign of each check.",
        "algorithm": "setup and hold slack at timing endpoints",
    },
    {
        "id": "module02-03-critical-path",
        "kind": "lab",
        "title": "Critical path",
        "short": "Critical path",
        "lab": "critical-path",
        "status": "P",
        "section": "02",
        "outcomes": "Trace the worst (most critical) path from an endpoint back through arrival tags.",
        "algorithm": "critical-path traceback from worst slack",
    },
    {
        "id": "module03-01-incremental-update",
        "kind": "lab",
        "title": "Incremental timing update",
        "short": "Incremental update",
        "lab": "incremental-update",
        "status": "P",
        "section": "03",
        "outcomes": "Invalidate and recompute only the cone affected by a local delay change.",
        "algorithm": "incremental invalidate / recompute on a delay edit",
    },
    {
        "id": "module03-03-false-multicycle-lite",
        "kind": "lab",
        "title": "False and multicycle paths (engine view)",
        "short": "False / multicycle",
        "lab": "false-multicycle-lite",
        "status": "P",
        "section": "03",
        "outcomes": "Apply engine-facing false-path and multicycle exceptions that change which endpoints are timed.",
        "algorithm": "false-path and multicycle exceptions as STA engine data",
    },
    {
        "id": "module05-01-offline-benchmark-compare",
        "kind": "offline",
        "title": "Offline benchmark compare",
        "short": "Offline compare",
        "lab": None,
        "status": "P",
        "section": "05",
        "outcomes": "Compare toy STA results against an open timer on shared tiny netlists when available.",
        "algorithm": "benchmark harness vs external timer",
    },
    {
        "id": "module99-00-wrap",
        "kind": "wrap",
        "title": "STA path complete",
        "short": "Wrap",
        "lab": None,
        "status": "—",
        "section": "99",
        "outcomes": "Recap graph → arrival/required → slack → critical path → incremental update, and choose learn_sdc next.",
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
        return f"**Kind:** `lab` · Primary lab: `{m['lab']}` · **Planned**"
    if m["kind"] == "offline":
        return "**Kind:** `offline` · Primary activity: local benchmark harness · **Planned**"
    return f"**Kind:** `{m['kind']}`"


def readme(m: dict, i: int) -> str:
    prev_m, next_m = prev_next(i)
    mid = m["id"]
    ss_aa = "-".join(mid.replace("module", "").split("-")[:2])
    header = (
        f"# Module {ss_aa}: {m['title']}\n\n"
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

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **{m['algorithm']}** on the tiny timing netlist.
2. Complete [CHECKLIST.md](CHECKLIST.md) with arrivals, required times, and slack (as applicable).
3. Optional self-check: `./scripts/module.sh {ss_aa} --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/{m['lab']}/index.html](http://127.0.0.1:8080/tools/{m['lab']}/index.html) *(planned)*
2. Tools shelf: open `{m['lab']}` from the platform tools index when shipped
3. Load the **starter netlist**, run the analysis, inspect path / slack metrics.
4. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach STA literacy on tiny graphs — not foundry sign-off or vendor GUI flows.
"""
    elif m["kind"] == "offline":
        body = """
## Offline track

1. Follow [EXAMPLES.md](EXAMPLES.md) to run the local compare harness.
2. Record WNS / TNS / path delay against at least one open timer when available.
3. Complete [CHECKLIST.md](CHECKLIST.md).
"""
    elif m["kind"] == "intro":
        body = """
## Setup

### Track A — Implement

No coding yet. Skim [docs/TWO_TRACKS.md](../docs/TWO_TRACKS.md) and [docs/MODULES.md](../docs/MODULES.md).

### Track B — Browser lab

When labs ship, open the tools shelf; for now, know that each later module has a primary lab id.

## How to move

1. Read this README and the short transcript.
2. Complete [CHECKLIST.md](CHECKLIST.md).
3. Continue to **timing graph** when the checklist feels honest.
"""
    else:
        body = """
## Dual-track recap

You practiced STA as **implement** (Track A) and/or **browser lab** (Track B). Prefer finishing at least one full implementation in foundations and one in slack / critical path before moving on.

## You can now

See outcomes above — and the wrap checklist.

## Next course

Natural next step: **learn_sdc** (constraints as data the engine consumes). Optional: **learn_si** for noise-on-timing literacy.
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
- [ ] Implemented **{m['algorithm']}** end-to-end on the starter netlist
- [ ] Reported arrivals, required times, and/or slack as the module requires
- [ ] Can explain the algorithm steps without the UI

## Track B — Browser lab (`{m['lab']}`)

- [ ] Opened the lab (local or live) when shipped
- [ ] Loaded the starter netlist
- [ ] Ran the analysis and inspected path / slack metrics

## Done when

- [ ] I can reproduce the result on paper/code **or** I finished the browser challenges (preferably both)
"""
    if m["kind"] == "offline":
        return f"""# Checklist — {m['title']}

## Offline harness

- [ ] Ran the compare script on at least one shared instance
- [ ] Recorded toy-engine vs external WNS/TNS (or documented tool missing)
- [ ] Named one discrepancy and a hypothesis

## Done when

- [ ] I can explain how to judge STA quality across tools on tiny netlists
"""
    if m["kind"] == "intro":
        return f"""# Checklist — {m['title']}

- [ ] I understand the course map (sections 01–03 + offline + wrap)
- [ ] I know Track A (implement) vs Track B (browser lab)
- [ ] I opened [docs/MODULES.md](../docs/MODULES.md) once
- [ ] Ready for the timing graph
"""
    return f"""# Checklist — {m['title']}

- [ ] I can name graph → arrival/required → slack → critical path → incremental update
- [ ] I know that heavy SDC authoring lives in `learn_sdc`
- [ ] I picked a next course (`learn_sdc` or optional `learn_si`)
"""


def examples(m: dict) -> str:
    if m["kind"] == "lab":
        return f"""# Examples — {m['title']}

Track A (implement). Use tiny timing netlists first (handful of cells / pins).

## Algorithm

**{m['algorithm']}**

## Starter prompts

1. Restate the algorithm in five bullets (inputs → loop → stop → output).
2. Run it on the tiny netlist in `examples/tiny_timing.json` (create if missing).
3. Report the metrics this module cares about (levels, arrival, required, slack, path, …).
4. Change one input (clock period, arc delay, exception) and report what moved.
5. Name one failure mode (wrong levelization, missed endpoint, stale incremental cone, …).

## Expected artifacts

- Timing graph or tagged pin times (as applicable)
- Slack and/or critical path for the starter clocks
- Short note: why this step belongs on the STA shelf

## Stretch

Scale to ~50 cells; keep the same API as the tiny case.
"""
    if m["kind"] == "offline":
        return """# Examples — Offline benchmark compare

1. Export the same tiny netlist used in critical-path / incremental modules.
2. Run your toy STA; record WNS, TNS, worst path delay, wall time.
3. If available, run an open timer (e.g. OpenSTA-style flow) on the same instance.
4. Fill a comparison table: WNS, TNS, path agreement, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
"""
    if m["kind"] == "intro":
        return """# Examples — Welcome

No coding yet.

1. Sketch where STA appears: after synthesis, during place/route optimization, and at sign-off.
2. Write one sentence: “Arrival and required times matter because …”
3. Name one difference between STA and dynamic simulation.
"""
    return """# Examples — Wrap

1. List five STA ideas from this course and one strength each.
2. For a local buffer insert, which module’s idea do you reach for first?
3. Write the bridge sentence you’ll need for `learn_sdc` next.
"""


def transcript_lab(m: dict) -> str:
    return f"""# {m['title']}

**Module id:** {m['id']}
**Lab:** {m['lab']}
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — {m['title']}

Static timing analysis answers a hard question without simulation waveforms: given clocks and delays, which paths meet setup and hold? In this module you’ll implement **{m['algorithm']}** end to end—not a sketch. By the end, you’ll run it on a tiny netlist, report the metrics that matter here, and know what the algorithm actually does.

## Slide 2 — The idea

Here’s the core idea in one breath: {m['algorithm']}. You’ll take a timing graph or tagged pin times, apply the update rule until a stop condition, and emit arrivals, required times, slack, or a path—depending on the lab. Watch three habits every time: levelize before you propagate, keep setup and hold separate, and never trust a path you cannot trace.

## Slide 3 — Browser lab track

In the browser lab track, open the **{m['lab']}** lab from the tools shelf when it ships. Load the starter netlist, run the analysis once, and read the metrics panel—arrivals, required times, slack, or the critical path. Orient yourself, try one parameter change, then come back to implement the same loop yourself.

## Slide 4 — Implement track

In the implement track, open this module’s examples and build the full algorithm. Parse the tiny timing JSON, run the core loop with clear stop rules, and print the tags plus metrics. Prefer a deterministic netlist so your golden answers stay stable. If something looks wrong, dump levels or pin times—debugging the graph is part of the learning.

## Slide 5 — Pitfalls

Common traps: propagating before the graph is levelized; mixing setup and hold in one number; treating false paths as free without updating endpoints; and full-chip rebuilds when only a cone changed. For incremental work, remember invalidate then recompute—not silent stale tags.

## Slide 6 — Your turn

Complete the checklist for at least one track—preferably both. Implement the algorithm until your metrics match the expected range on the starter netlist. When you’re ready, take the short quiz, then continue to the next module in this section.
"""


def transcript_intro() -> str:
    return """# Welcome to static timing analysis

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to static timing analysis

Digital chips must meet clock constraints without simulating every vector. Static timing analysis builds a timing graph, propagates arrival and required times, and reports slack—so designers know which paths fail and where to fix. This course teaches those algorithms as full implementations on tiny netlists.

## Slide 2 — What you’ll build

You’ll start with the timing graph and levelization, then propagate arrival forward and required backward. Slack, setup, and hold follow, then critical-path traceback. Later labs cover incremental updates after a local delay edit, and false-path or multicycle exceptions as data the engine consumes—not a full SDC authoring course. One idea per lab. Full implementations at course scale—not foundry throughput, but complete and correct on the scoped instances.

## Slide 3 — Stable module ids

Module folders use hierarchical ids: section, then algorithm slot—like module two dash zero one for slack. That way we can add algorithms later without renumbering everything. Odd slots leave room for inserts. Treat published ids as stable keys; display order lives in the module index.

## Slide 4 — Two tracks

Every lab module offers two practice tracks. Track A is implement: code the algorithm, run tiny netlists, report metrics. Track B is the browser lab shelf for visual intuition. A good rhythm is browser first for the idea, then implement to harden it. Intro and wrap modules have no lab. Heavy constraint authoring lives next door in learn SDC.

## Slide 5 — How to move

For each module, read the README for outcomes, pick a track—or both—then work the checklist. Keep arrival, required, and slack as your habit. When this intro checklist is done, continue to the timing graph—the shared language every later algorithm will use.
"""


def transcript_wrap() -> str:
    return """# STA path complete

**Module id:** module99-00-wrap
**Lab:** none (wrap)
**Tracks:** recap · next course

## Slide 1 — STA path complete

You’ve walked the STA path—from timing graphs and arrival/required propagation, through setup and hold slack and critical-path traceback, into incremental updates and engine-facing false or multicycle exceptions, plus an offline compare habit. This wrap names what you can do now and where to go next.

## Slide 2 — What you can do now

You can build a levelized timing graph, propagate tags, compute slack, and trace a critical path. You know when a full rebuild is wasteful and when an incremental cone update is enough. You treat false paths and multicycle checks as engine data, not magic. You are not shipping a foundry timer—you are building algorithm literacy for the digital flow.

## Slide 3 — Close the gaps

If you mainly watched browser labs, go back and finish at least one full implementation in foundations and one in slack or critical path. If you mainly coded, re-open any skipped visual labs when they ship. Either track works for self-study; both together stick best before constraints or signal integrity.

## Slide 4 — Next courses

Natural next step is learn SDC—clocks, I/O, false and multicycle constraints as data the engine consumes. Optional later: learn SI for crosstalk and noise-on-timing literacy. Keep your tiny netlist harness—you’ll reuse the I/O format.

## Slide 5 — Your turn

Review the wrap checklist. Name five ideas from this course and one strength each. Say which idea you’d use after inserting a buffer on a critical net. When you’re ready, take the short quiz, then open the learn SDC README.
"""


def transcript_offline() -> str:
    return """# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none (offline)
**Tracks:** offline harness

## Slide 1 — Offline benchmark compare

Toy engines teach mechanism. Benchmarks teach honesty. In this offline module you’ll run the same tiny netlists through your STA and, when available, an open external timer—then compare WNS, TNS, and path delay without pretending the numbers are foundry sign-off.

## Slide 2 — Fair compare rules

Use identical input. Fix clocks and library delays. Report the same metrics on both sides. If the external tool is missing, still run your harness and document the install gap—don’t invent golden numbers. A clean I/O contract matters more than a flashy chart.

## Slide 3 — What good looks like

Expect your educational engine to be slower and sometimes less complete. That’s fine. You’re looking for the same qualitative behavior: matching worst paths, consistent slack signs, and no silent illegal tags. Huge unexplained wins usually mean a metric or exception mismatch, not genius.

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
                    "Full implementations of STA algorithms on tiny netlists",
                    "Foundry PDK certification",
                    "Writing UVM agents",
                ],
                "answer": 1,
                "explain": "Algorithm / toy-engine literacy on scoped timing graphs.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "STA replaces all need for simulation vectors by proving functional correctness.",
                "answer": False,
                "explain": "STA checks timing under delay models; it does not prove function.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A good study rhythm is…",
                "choices": [
                    "Only memorize folder names",
                    "Browser intuition then implement metrics on tiny netlists",
                    "Skip checklists entirely",
                    "Start with multicycle exceptions before the timing graph",
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
                "prompt": "After a local buffer insert, the STA idea you reach for first is…",
                "choices": [
                    "Rebuild the entire chip from scratch only",
                    "Incremental invalidate / recompute of the affected cone",
                    "Delete all clocks",
                    "Ignore slack forever",
                ],
                "answer": 1,
                "explain": "Incremental update recomputes only what the edit touched.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "Setup and hold slack use the same formula with the same clock edge pair.",
                "answer": False,
                "explain": "Setup and hold use different edge relationships and inequalities.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A natural next course after STA is…",
                "choices": [
                    "Only analog layout",
                    "learn_sdc (constraints as engine data)",
                    "SPICE device models first",
                    "Ignore the digital flow",
                ],
                "answer": 1,
                "explain": "SDC teaches clocks and exceptions the timer consumes.",
            },
        ]
        title = "Wrap check"
    elif m["kind"] == "offline":
        items = [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Fair compares require the same netlist, clocks, and reported metrics.",
                "answer": True,
                "explain": "Otherwise you compare different problems.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "If an external timer is missing you should…",
                "choices": [
                    "Invent golden WNS numbers",
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
                "prompt": "An educational STA that is slower than OpenSTA is automatically wrong.",
                "answer": False,
                "explain": "Speed differs; look for consistent paths and slack signs.",
            },
        ]
        title = "Offline check"
    else:
        algo = m["algorithm"] or m["title"]
        items = [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "This lab’s primary algorithm is…",
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
                "prompt": "You can safely propagate arrivals before the timing graph is levelized.",
                "answer": False,
                "explain": "Levelization (or equivalent topo order) comes first.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "After running the algorithm you should report…",
                "choices": [
                    "Only a screenshot of the UI",
                    "Tagged times and/or slack / path metrics for the starter",
                    "Only runtime",
                    "Nothing — intuition is enough",
                ],
                "answer": 1,
                "explain": "Tags + metrics are the contract.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": f"Track A asks you to implement {algo} on a tiny netlist.",
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
footer: "learn_sta — {m['short']}"
slides:
  - type: title
    title: "{m['title']}"
    subtitle: "{m['id']} · learn_sta"
    notes: |
      Stub — replace via transcript_to_outline.py after revising transcript.md.
"""


def write_modules_md() -> None:
    rows = []
    for m in MODULES:
        lab = f"`{m['lab']}`" if m["lab"] else ("offline harness" if m["kind"] == "offline" else "—")
        status = "P" if m["kind"] in ("lab", "offline") else m["status"]
        rows.append(
            f"| `{m['id']}` | `{m['kind']}` | [{m['title']}](../{m['id']}/README.md) | {lab} | {status} |"
        )
    text = f"""# learn_sta — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.
Published ids are **stable keys**; order below is the teaching path.

Status: **P** = planned (scaffold); **ref** when browser lab + `common/` solvers ship.

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
{chr(10).join(rows)}

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (timing graph, arrival / required) |
| `02` | Slack and critical path |
| `03` | Incremental update + engine-facing exceptions |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs (PPT / transcript)

When walkthrough frames exist: [WALKTHROUGHS.md](WALKTHROUGHS.md).
Each lab module may have `assets/STEPS.md` and `assets/steps/*.png`.

**Build media in WSL** (LibreOffice + edge-tts + ffmpeg):

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_sta/scripts/build_all_media.sh
```
"""
    write(ROOT / "docs" / "MODULES.md", text)


def write_docs() -> None:
    write(
        ROOT / "docs" / "SCOPE.md",
        """# Scope — learn_sta

## In scope

- Full implementations of core STA algorithms on tiny-to-small netlists
- Timing graph construction and levelization
- Forward arrival and backward required propagation
- Setup / hold slack and critical-path traceback
- Incremental invalidate / recompute after a local delay edit
- False-path and multicycle exceptions as **engine-facing data** (lite)
- Offline compare habits against open timers when available

## Out of scope (v1)

- Drop-in replacement for commercial or production OpenSTA flows
- Foundry PDK / liberty / SPEF sign-off certification
- Full SDC authoring and constraint methodology (see `learn_sdc`)
- Crosstalk / noise-on-timing deep dive (see `learn_si`)
- Vendor GUI workflows

## “Full implementation” means

Complete and correct for the **scoped problem size** (tens of cells / pins): parse input, build the graph, propagate tags, emit slack / paths, with tests—not a production-scale timer.
""",
    )
    write(
        ROOT / "docs" / "TWO_TRACKS.md",
        """# Two tracks — learn_sta

| Track | Surface | Job |
|-------|---------|-----|
| **A — Implement** | `EXAMPLES.md`, tiny netlists under each module | Code the full algorithm; report arrivals / required / slack / path |
| **B — Browser lab** | `platform/tools/<lab-id>/` | Visual intuition; starter + challenges (when shipped) |

Intro / wrap have no lab. Offline module is harness-only.

Prefer: browser once for the idea → implement until metrics match.

Constraint-heavy authoring belongs in **learn_sdc**; this course only consumes exceptions as engine data.
""",
    )
    labs = [m for m in MODULES if m["kind"] == "lab"]
    rows = "\n".join(
        f"| `{m['lab']}` | {m['title']} | planned |" for m in labs
    )
    write(
        ROOT / "docs" / "WALKTHROUGHS.md",
        f"""# Algorithm walkthroughs — learn_sta

Step frames for PPT / transcript live under each lab’s `assets/steps/` once captured.

Interactive viewer (when ALGOS entries exist):
`http://127.0.0.1:8080/tools/algorithm-walkthrough/?algo=<lab-id>&step=1`

| Lab id | Module | Status |
|--------|--------|--------|
{rows}

Capture (WSL, after tools + walkthrough map exist):

```bash
python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \\
  courses/learn_sta/module01-01-timing-graph \\
  --inject-transcript
```
""",
    )


def write_course_readme() -> None:
    landing_rows = []
    for m in MODULES:
        parts = m["id"].replace("module", "").split("-")
        label = f"{parts[0]}-{parts[1]}"
        landing_rows.append(f"| {label} — {m['title']} | [{m['id']}]({m['id']}/README.md) |")
    table = "\n".join(landing_rows)
    lab_links = " · ".join(f"`{m['lab']}`" for m in MODULES if m["lab"])
    write(
        ROOT / "README.md",
        f"""# learn_sta

[![GitHub](https://img.shields.io/badge/GitHub-learn__sta-181717?logo=github)](https://github.com/universal-verification-methodology/learn_sta)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-orange)](../../eda.md)
[![Parent](https://img.shields.io/badge/parent-learning%20monorepo-0A9EDC)](https://github.com/universal-verification-methodology/learning)
[![Labs](https://img.shields.io/badge/labs-GitHub%20Pages-222?logo=githubpages)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-EDA%20STA%20%7C%20timing%20graph%20%7C%20slack-purple)](docs/MODULES.md)

**learn_sta** is the open learning path for *static timing analysis algorithms used in digital design*—timing graph, arrival/required, slack, critical path, and incremental update on tiny netlists.

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
learn_sta/
├── README.md
├── LICENSE              # CC BY 4.0 (add when publishing standalone)
├── common/              # netlist I/O, propagation helpers, goldens
├── docs/
│   ├── MODULES.md       # full module index
│   ├── TWO_TRACKS.md    # Track A (implement) vs Track B (browser)
│   ├── SCOPE.md
│   └── WALKTHROUGHS.md  # algorithm walkthrough map
├── scripts/
│   ├── scaffold_course.py
│   └── build_all_media.sh
├── module00-00-intro/
├── module01-01-timing-graph/
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
- **Syllabus (parent):** [`eda.md` § learn_sta](../../eda.md)
- **Scope:** [docs/SCOPE.md](docs/SCOPE.md)
- **From the monorepo:** open `courses/learn_sta/` (this tree).

Then open [module00-00-intro/README.md](module00-00-intro/README.md).

## Consume from the parent

From a clone of the **learning** monorepo:

```bash
git clone --recurse-submodules \\
  git@github.com:universal-verification-methodology/learning.git
# or, if already cloned without submodules:
git submodule update --init --recursive

ls courses/learn_sta
```

Working tree path in the parent: `courses/learn_sta/`.

## Author: publish or update

Edit inside the parent monorepo (recommended).

```bash
# from the learning monorepo checkout
cd courses/learn_sta
# … edit module README / CHECKLIST / EXAMPLES / transcript …

# rebuild media from the parent (one module at a time; Unix/WSL):
cd ../..
# revise transcript.md, then:
python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \\
  courses/learn_sta/module01-01-timing-graph
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \\
  courses/learn_sta/module01-01-timing-graph

# bulk (when asked):
# bash courses/learn_sta/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py learn_sta
```

Verify README consistency:

```bash
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \\
  courses/learn_sta --modules
```

See the skill `SKILL.md` for dual-track narration, algorithm walkthrough frames, and the full PPTX → PDF → TTS → MP4 pipeline.

## Two learning tracks

Every **lab** module documents both tracks. Intro/wrap modules have no lab. Details: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md).

| Track | Practice surface | Start here |
|-------|------------------|------------|
| **A — Implement** | Tiny netlists + `EXAMPLES.md` / `examples/` | [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md) |
| **B — Browser lab** | Platform tools (planned) | [local tools](http://127.0.0.1:8080/tools/) · [live](https://universal-verification-methodology.github.io/learning/tools/) |

Recommended path: short Track B starter (when shipped) → Track A implement + checklist → optional quiz / transcript review.

## Module landings

Full status table: **[docs/MODULES.md](docs/MODULES.md)**. Clusters: 00 intro · 01 foundations · 02 slack/critical path · 03 incremental + exceptions · 05 offline · 99 wrap.

| Module | Landing |
|--------|---------|
{table}

## Browser labs

By workflow (Track B), **planned:** {lab_links}. Offline compare remains Track A / harness only. See [all tools](https://universal-verification-methodology.github.io/learning/tools/) and each module README for its primary lab id. Algorithm step walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — add a course-root [`LICENSE`](LICENSE) when publishing this tree as a standalone repo; until then materials are intended for CC BY 4.0 alignment with the digital_learning courses.

Platform tools and the parent monorepo may carry additional notices.
""",
    )


def write_common() -> None:
    write(
        ROOT / "common" / "README.md",
        """# common — learn_sta

Shared Track A helpers (Python) for tiny timing netlists and metrics.

Suggested layout as you flesh reference solvers:

- `timing_io.py` — load/save tiny timing JSON
- `graph.py` — pins, arcs, levelization
- `propagate.py` — arrival / required / slack
- `goldens/` — expected tags for starter instances

Browser algorithms will live in `platform/assets/sta-core.js` when tools ship.
""",
    )
    tiny = {
        "name": "tiny_sta_chain",
        "clock": {"name": "clk", "period": 10.0},
        "pins": [
            {"id": "in", "kind": "port"},
            {"id": "u1/A", "kind": "cell_in", "cell": "u1"},
            {"id": "u1/Y", "kind": "cell_out", "cell": "u1"},
            {"id": "u2/A", "kind": "cell_in", "cell": "u2"},
            {"id": "u2/Y", "kind": "cell_out", "cell": "u2"},
            {"id": "out", "kind": "port"},
        ],
        "arcs": [
            {"from": "in", "to": "u1/A", "delay": 0.0, "kind": "net"},
            {"from": "u1/A", "to": "u1/Y", "delay": 1.2, "kind": "cell"},
            {"from": "u1/Y", "to": "u2/A", "delay": 0.3, "kind": "net"},
            {"from": "u2/A", "to": "u2/Y", "delay": 1.5, "kind": "cell"},
            {"from": "u2/Y", "to": "out", "delay": 0.2, "kind": "net"},
        ],
        "notes": "Toy chain for arrival/required/slack goldens; not a liberty model.",
    }
    write(ROOT / "common" / "tiny_timing.json", json.dumps(tiny, indent=2) + "\n")


def write_build_script() -> None:
    write(
        ROOT / "scripts" / "build_all_media.sh",
        """#!/usr/bin/env bash
# Build PPTX → PDF → audio → video for all learn_sta modules (Unix/WSL only).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SKILL="$ROOT/.cursor/skills/module-slides/scripts"
# shellcheck source=/dev/null
source "$SKILL/_require_unix.sh"

COURSE="$ROOT/courses/learn_sta"
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
echo "Done. Publish: python3 platform/scripts/publish_course_platform.py learn_sta"
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
            (ex / "tiny_timing.json").write_text(
                (ROOT / "common" / "tiny_timing.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        print(f"ok {mid}")
    print(f"Scaffolded {len(MODULES)} modules under {ROOT}")


if __name__ == "__main__":
    main()
