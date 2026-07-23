#!/usr/bin/env python3
"""Scaffold learn_placement modules (hierarchical SS-AA ids) with module-slides stubs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "learn_placement"

MODULES = [
    {
        "id": "module00-00-intro",
        "kind": "intro",
        "title": "Welcome to placement for EDA",
        "short": "Welcome",
        "lab": None,
        "status": "—",
        "section": "00",
        "outcomes": "Explain why global placement sits between floorplanning and legalization, and how this course is organized.",
        "algorithm": None,
    },
    {
        "id": "module01-01-hpwl-metrics",
        "kind": "lab",
        "title": "Half-perimeter wirelength",
        "short": "HPWL metrics",
        "lab": "hpwl-metrics",
        "status": "P",
        "section": "01",
        "outcomes": "Compute half-perimeter wirelength (HPWL) per net and total HPWL for a placement.",
        "algorithm": "bbox half-perimeter wirelength (HPWL) metrics",
    },
    {
        "id": "module01-03-net-models",
        "kind": "lab",
        "title": "Net models for wirelength",
        "short": "Net models",
        "lab": "net-models",
        "status": "P",
        "section": "01",
        "outcomes": "Compare bbox, clique, and star wirelength models on the same multi-pin net.",
        "algorithm": "bbox / clique / star net wirelength models",
    },
    {
        "id": "module02-01-force-directed-place",
        "kind": "lab",
        "title": "Force-directed placement",
        "short": "Force-directed",
        "lab": "force-directed-place",
        "status": "P",
        "section": "02",
        "outcomes": "Run a force-directed (spring) placement pass and report HPWL before and after.",
        "algorithm": "force-directed (spring) placement",
    },
    {
        "id": "module02-03-quadratic-place",
        "kind": "lab",
        "title": "Quadratic placement",
        "short": "Quadratic",
        "lab": "quadratic-place",
        "status": "P",
        "section": "02",
        "outcomes": "Solve a quadratic-lite placement with fixed pads and compare HPWL to free force place.",
        "algorithm": "quadratic placement with fixed pads",
    },
    {
        "id": "module02-05-analytical-place",
        "kind": "lab",
        "title": "Analytical / density-aware place",
        "short": "Analytical",
        "lab": "analytical-place",
        "status": "P",
        "section": "02",
        "outcomes": "Combine a wirelength stage with density spreading and report HPWL versus overflow trade-offs.",
        "algorithm": "analytical lite (wirelength + density spread)",
    },
    {
        "id": "module02-07-sa-placement",
        "kind": "lab",
        "title": "Simulated annealing placement",
        "short": "Simulated annealing",
        "lab": "sa-placement",
        "status": "P",
        "section": "02",
        "outcomes": "Run simulated-annealing cell jogs under an HPWL cost and keep the best placement.",
        "algorithm": "simulated annealing placement (HPWL cost)",
    },
    {
        "id": "module03-01-density-bins",
        "kind": "lab",
        "title": "Density bins and overflow",
        "short": "Density bins",
        "lab": "density-bins",
        "status": "P",
        "section": "03",
        "outcomes": "Bin cells on a grid, compute per-bin counts, and report density overflow vs capacity.",
        "algorithm": "density bins and overflow",
    },
    {
        "id": "module03-03-spread-legalize-lite",
        "kind": "lab",
        "title": "Spreading / overlap relief",
        "short": "Spread / legalize",
        "lab": "spread-legalize-lite",
        "status": "P",
        "section": "03",
        "outcomes": "Push overlapping cells apart until a minimum pairwise distance is met without exploding HPWL.",
        "algorithm": "pairwise spread / overlap relief",
    },
    {
        "id": "module04-01-timing-driven-place",
        "kind": "lab",
        "title": "Timing-driven placement",
        "short": "Timing-driven",
        "lab": "timing-driven-place",
        "status": "P",
        "section": "04",
        "outcomes": "Weight critical nets in the HPWL objective and compare plain vs timing-weighted wirelength.",
        "algorithm": "timing-weighted HPWL placement objective",
    },
    {
        "id": "module05-01-offline-benchmark-compare",
        "kind": "offline",
        "title": "Offline benchmark compare",
        "short": "Offline compare",
        "lab": None,
        "status": "P",
        "section": "05",
        "outcomes": "Compare toy placers against open placement tools on shared instances.",
        "algorithm": "benchmark harness vs external tools",
    },
    {
        "id": "module99-00-wrap",
        "kind": "wrap",
        "title": "Placement path complete",
        "short": "Wrap",
        "lab": None,
        "status": "—",
        "section": "99",
        "outcomes": "Recap HPWL, global place, density, and timing objectives; choose legalization or congestion next.",
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

1. Open [EXAMPLES.md](EXAMPLES.md) and implement **{m['algorithm']}** on the tiny placement.
2. Complete [CHECKLIST.md](CHECKLIST.md) with metrics (HPWL, density / overflow when relevant).
3. Optional self-check: `./scripts/module.sh {ss_aa} --check` (from course root).

### Track B — Browser lab (online)

1. Local: [http://127.0.0.1:8080/tools/{m['lab']}/index.html](http://127.0.0.1:8080/tools/{m['lab']}/index.html)
2. Tools shelf: open `{m['lab']}` from the platform tools index
3. Load the **starter placement**, run the algorithm, inspect metrics.
4. Check off Track B items in [CHECKLIST.md](CHECKLIST.md).

> Concept labs teach algorithm literacy on tiny instances — not production PDK flows.
"""
    elif m["kind"] == "offline":
        body = """
## Offline track

1. Follow [EXAMPLES.md](EXAMPLES.md) to run the local compare harness.
2. Record HPWL / density / runtime against at least one external tool when available.
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
- [ ] Implemented **{m['algorithm']}** end-to-end on the starter placement
- [ ] Reported HPWL (and density / overflow when the lab uses them)
- [ ] Can explain the algorithm steps without the UI

## Track B — Browser lab (`{m['lab']}`)

- [ ] Opened the lab (local or live)
- [ ] Loaded the starter placement
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

- [ ] I can explain how to judge placement quality across tools
"""
    if m["kind"] == "intro":
        return f"""# Checklist — {m['title']}

- [ ] I understand the course map (sections 01–05 + wrap)
- [ ] I know Track A (implement) vs Track B (browser lab)
- [ ] I opened [docs/MODULES.md](../docs/MODULES.md) once
- [ ] Ready for HPWL metrics
"""
    return f"""# Checklist — {m['title']}

- [ ] I can name the main algorithms from sections 01–04
- [ ] I know when force / quadratic / SA / density fits
- [ ] I picked a next course (`learn_legalization`, `learn_congestion`, or `learn_floorplanning`)
"""


def examples(m: dict) -> str:
    if m["kind"] == "lab":
        return f"""# Examples — {m['title']}

Track A (implement). Use the tiny 6-cell placement first.

## Algorithm

**{m['algorithm']}**

## Starter prompts

1. Restate the algorithm in five bullets (inputs → loop → stop → output).
2. Run it on `examples/tiny_place.json` (same instance as the browser starter).
3. Compute total HPWL after the run (and density overflow when relevant).
4. Change one parameter (seed, iters, pad fix, capacity) and report what moved.
5. Name one failure mode (overlap collapse, ignored pads, metric mismatch, …).

## Expected artifacts

- Cell coordinates (or assignment) after the run
- HPWL before and after (plus density / overflow when used)
- Short note: why this algorithm belongs on the placement shelf

## Stretch

Scale to ~100 cells; keep the same API as the tiny case.
"""
    if m["kind"] == "offline":
        return """# Examples — Offline benchmark compare

1. Export the same tiny placement used in force / quadratic / SA modules.
2. Run your toy placer; record HPWL, density overflow, wall time.
3. If available, run an open tool (e.g. OpenROAD place-lite / academic placer) on the same instance.
4. Fill a comparison table: quality, legality proxy, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
"""
    if m["kind"] == "intro":
        return """# Examples — Welcome

No coding yet.

1. Sketch where global placement sits: after floorplan, before detailed legalization / routing.
2. Write one sentence: “A good placement reduces wirelength while keeping density legal because …”
3. Name one difference between placement and floorplanning in EDA.
"""
    return """# Examples — Wrap

1. List three algorithms from this course and one strength each.
2. For a timing-critical net, which module’s idea do you reach for first?
3. Write the bridge sentence you’ll need for legalization or congestion next.
"""


def transcript_lab(m: dict) -> str:
    return f"""# {m['title']}

**Module id:** {m['id']}
**Lab:** {m['lab']}
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — {m['title']}

Placement assigns cell coordinates to cut wirelength while keeping density under control. In this module you’ll implement **{m['algorithm']}** end to end—not a sketch. By the end, you’ll run it on a tiny instance, report HPWL, and know what the algorithm actually does.

## Slide 2 — The idea

{m['algorithm']}. You’ll take a placement instance, apply the update rule until a stop condition, and emit coordinates. Watch HPWL every time—and density overflow when the lab uses bins.

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 3 — Browser lab track

In the browser lab track, open the **{m['lab']}** lab from the tools shelf. Load the starter placement, run the algorithm once, and read the metrics panel. Orient yourself, try one parameter change, then come back to implement the same loop yourself.

## Slide 4 — Implement track

In the implement track, open this module’s examples and build the full algorithm. Parse the tiny placement, run the core loop with clear stop rules, and print coordinates plus metrics. Prefer a deterministic seed so your golden answers stay stable.

## Slide 5 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads; mixing bbox and clique models in one report; and stopping before the best SA iterate is kept.

## Slide 6 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the expected range on the starter placement. When you’re ready, take the short quiz, then continue to the next module.
"""


def transcript_intro() -> str:
    return """# Welcome to placement for EDA

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to placement for EDA

Physical design asks: where does each cell go so wires stay short and density stays legal? That is placement. This course teaches global placement algorithms as full implementations on a tiny six-cell instance—so you build literacy for legalization, congestion, and routing later.

## Slide 2 — What you’ll build

You’ll start with half-perimeter wirelength and net models, then force-directed, quadratic, analytical, and simulated-annealing place. Density bins and spreading teach legality proxies. Timing-driven place weights critical nets. One algorithm per lab. Full implementations at course scale—not production throughput, but complete and correct on the scoped instance.

## Slide 3 — Stable module ids

Module folders use hierarchical ids: section, then algorithm slot—like module two dash zero one for force-directed place. That way we can add algorithms later without renumbering everything. Odd slots leave room for inserts. Treat published ids as stable keys; display order lives in the module index.

## Slide 4 — Two tracks

Every lab module offers two practice tracks. Track A is implement: code the algorithm, run the tiny placement, report metrics. Track B is the browser lab shelf for visual intuition. A good rhythm is browser first for the idea, then implement to harden it. Intro and wrap modules have no lab.

## Slide 5 — How to move

For each module, read the README for outcomes, pick a track—or both—then work the checklist. Keep HPWL as your habit. When this intro checklist is done, continue to half-perimeter wirelength—the shared language every later algorithm will use.
"""


def transcript_wrap() -> str:
    return """# Placement path complete

**Module id:** module99-00-wrap
**Lab:** none (wrap)
**Tracks:** recap · next course

## Slide 1 — Placement path complete

You’ve walked the placement path—from HPWL and net models, through force, quadratic, analytical, and SA search, into density bins, spreading, and timing-weighted objectives, plus an offline compare habit. This wrap names what you can do now and where to go next.

## Slide 2 — What you can do now

You can compute HPWL, compare net models, and run global-place loops that improve wirelength. You know why density bins matter and how spreading relieves overlap. You can weight critical nets. You are not shipping a foundry placer—you are building algorithm literacy for the PD stack.

## Slide 3 — Close the gaps

If you mainly watched browser labs, go back and finish at least one full implementation in foundations and one in global place. If you mainly coded, re-open any skipped visual labs. Either track works for self-study; both together stick best before legalization or congestion.

## Slide 4 — Next courses

Natural next steps are learn legalization—for snapping and overlap removal—and learn congestion, where density maps feed routing capacity. Keep your tiny-placement harness—you’ll reuse the I/O format.

## Slide 5 — Your turn

Review the wrap checklist. Name three algorithms and one strength each. Say which idea you’d use when a net is timing-critical. When you’re ready, take the short quiz, then open the next course README.
"""


def transcript_offline() -> str:
    return """# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none (offline)
**Tracks:** offline harness

## Slide 1 — Offline benchmark compare

Toy engines teach mechanism. Benchmarks teach honesty. In this offline module you’ll run the same instances through your placer and, when available, an open external tool—then compare HPWL, density, and runtime without pretending the numbers are foundry sign-off.

## Slide 2 — Fair compare rules

Use identical input. Fix seeds when the algorithm is randomized. Report the same metrics on both sides. If the external tool is missing, still run your harness and document the install gap—don’t invent golden numbers. A clean I/O contract matters more than a flashy chart.

## Slide 3 — What good looks like

Expect your educational engine to be slower and sometimes lower quality. That’s fine. You’re looking for the same qualitative behavior: improving HPWL, controlled density, and no silent illegal piles. Huge unexplained wins usually mean a metric mismatch, not genius.

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
                    "Full implementations of placement algorithms on tiny instances",
                    "Foundry PDK certification",
                    "Writing UVM agents",
                ],
                "answer": 1,
                "explain": "Algorithm / toy-engine literacy on scoped placements.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "A good placement usually ignores density as long as HPWL is zero.",
                "answer": False,
                "explain": "Density keeps cells legal for legalization and routing; piled cells with tiny HPWL are not usable.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A good study rhythm is…",
                "choices": [
                    "Only memorize folder names",
                    "Browser intuition then implement metrics on the tiny placement",
                    "Skip checklists entirely",
                    "Start with SA before HPWL",
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
                "prompt": "Timing-critical nets are handled most directly by…",
                "choices": [
                    "Ignoring weights until routing",
                    "Timing-weighted HPWL / criticality weights",
                    "Always SA with seed 1 only",
                    "Increasing HPWL on purpose",
                ],
                "answer": 1,
                "explain": "Weights pull critical nets shorter in the objective.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "Force-directed and quadratic place improve an existing seed under an HPWL-related pull.",
                "answer": True,
                "explain": "They move free cells toward wirelength-friendly positions.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A natural next course after placement is…",
                "choices": [
                    "Only analog layout",
                    "Legalization or congestion",
                    "SPICE device models first",
                    "Ignore the PD stack",
                ],
                "answer": 1,
                "explain": "Those courses reuse HPWL, density, and legality instincts.",
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
                "prompt": "An educational placer that is slower than OpenROAD is automatically wrong.",
                "answer": False,
                "explain": "Speed differs; look for improving HPWL and controlled density.",
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
                "prompt": "HPWL alone is enough; density can always be ignored in this course.",
                "answer": False,
                "explain": "Density labs report overflow; global place must not silently pile cells.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "After running the algorithm you should report…",
                "choices": [
                    "Only a screenshot of the UI",
                    "Coordinates plus HPWL (and density when relevant)",
                    "Only runtime",
                    "Nothing — intuition is enough",
                ],
                "answer": 1,
                "explain": "Coordinates + metrics are the contract.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": f"Track A asks you to implement {algo} on the tiny placement.",
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
        lab = f"`{m['lab']}`" if m["lab"] else ("offline harness" if m["kind"] == "offline" else "—")
        status = "**ref**" if m["kind"] == "lab" else m["status"]
        rows.append(
            f"| `{m['id']}` | `{m['kind']}` | [{m['title']}](../{m['id']}/README.md) | {lab} | {status} |"
        )
    text = f"""# {COURSE_ID} — module index

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
| `01` | Foundations (HPWL, net models) |
| `02` | Global place (force, quadratic, analytical, SA) |
| `03` | Density and spreading |
| `04` | Timing-driven place |
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

- Full implementations of global placement algorithms on a tiny-to-medium instance
- Metrics: HPWL (bbox), clique/star net models, density bins / overflow
- Fixed pads, analytical density spreading, timing-weighted objectives
- Offline compare habits against open tools when available

## Out of scope (v1)

- Drop-in replacement for commercial or OpenROAD production placers
- Foundry PDK certification or production sign-off
- Detailed legalization / row-site snapping as the spine (see `learn_legalization`)
- Vendor GUI workflows

## “Full implementation” means

Complete and correct for the **scoped problem size** (handful of cells/nets → low hundreds): parse input, run the algorithm, emit coordinates + metrics, with tests—not a production-scale engine.
""",
    )
    write(
        ROOT / "docs" / "TWO_TRACKS.md",
        f"""# Two tracks — {COURSE_ID}

| Track | Surface | Job |
|-------|---------|-----|
| **A — Implement** | `EXAMPLES.md`, tiny placement under each module | Code the full algorithm; report HPWL (+ density) |
| **B — Browser lab** | `platform/tools/<lab-id>/` | Visual intuition; starter + challenges |

Intro / wrap have no lab. Offline module is harness-only.

Prefer: browser once for the idea → implement until metrics match.
""",
    )
    lab_rows = []
    for m in MODULES:
        if m["kind"] != "lab":
            continue
        lab_rows.append(
            f"| `{m['lab']}` | [`{m['id']}`](../{m['id']}/assets/STEPS.md) | (capture later) |"
        )
    write(
        ROOT / "docs" / "WALKTHROUGHS.md",
        f"""# Algorithm walkthroughs (for PPT / transcript)

Step frames live under each lab module’s `assets/steps/` with captions in `assets/STEPS.md`.
Transcripts embed them between `<!-- algorithm-walkthrough -->` markers; PPTX rebuilds as full-slide images.

## Interactive viewer

`platform/tools/algorithm-walkthrough/?algo=<lab-id>&step=N`

Serve: `python3 -m http.server 8080 --directory platform`

## Capture + rebuild (WSL)

```bash
cd /mnt/d/proj/designs/eda_learning

# Walkthrough PNGs + inject transcripts (serve platform/ on :8080 first)
python3 -m http.server 8080 --directory platform &
for m in \\
  module01-01-hpwl-metrics \\
  module01-03-net-models \\
  module02-01-force-directed-place \\
  module02-03-quadratic-place \\
  module02-05-analytical-place \\
  module02-07-sa-placement \\
  module03-01-density-bins \\
  module03-03-spread-legalize-lite \\
  module04-01-timing-driven-place
do
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \\
    courses/{COURSE_ID}/$m --inject-transcript
done

bash courses/{COURSE_ID}/scripts/build_all_media.sh
```

| Algorithm | Module | Steps |
|-----------|--------|-------|
{chr(10).join(lab_rows)}

Intro / offline / wrap modules have PPTX from transcript only (no algorithm step frames).
""",
    )


def write_course_readme() -> None:
    table = "\n".join(
        f"| {m['id']} — {m['title']} | [{m['id']}]({m['id']}/README.md) |" for m in MODULES
    )
    write(
        ROOT / "README.md",
        f"""# {COURSE_ID}

[![Role](https://img.shields.io/badge/role-course%20scaffold-orange)](../../eda.md)
[![Domain](https://img.shields.io/badge/domain-EDA%20placement%20%7C%20HPWL%20%7C%20density-purple)](docs/MODULES.md)

**{COURSE_ID}** is the open learning path for *global placement algorithms used in EDA physical design*—one full algorithm per lab, on a tiny instance.

- Scope: [docs/SCOPE.md](docs/SCOPE.md)
- Modules: [docs/MODULES.md](docs/MODULES.md)
- Tracks: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md)
- Walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md)

## Contents

```text
{COURSE_ID}/
├── README.md
├── common/         # placement I/O, HPWL, reference solvers
├── docs/           # MODULES, TWO_TRACKS, SCOPE, WALKTHROUGHS
├── scripts/        # scaffold_course.py, enrich_transcripts.py, build_all_media.sh
├── module00-00-intro/
├── …
└── module99-00-wrap/
```

Module folders use **hierarchical ids** `moduleSS-AA-slug` so algorithms can be added later without renumbering.

## Two learning tracks

| Track | Practice surface |
|-------|------------------|
| **A** | Implement full algorithms on the tiny placement (`EXAMPLES.md`) |
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
  courses/{COURSE_ID}/module01-01-hpwl-metrics
python3 .cursor/skills/module-slides/scripts/build_pptx.py \\
  courses/{COURSE_ID}/module01-01-hpwl-metrics
bash courses/{COURSE_ID}/scripts/build_all_media.sh
```

## License

Course materials intended for CC BY 4.0 alignment with the digital_learning courses (add `LICENSE` when publishing).
""",
    )


def tiny_place_dict() -> dict:
    return {
        "cells": ["A", "B", "C", "D", "E", "F"],
        "nets": [
            ["A", "B"],
            ["C", "D"],
            ["A", "C"],
            ["B", "D"],
            ["A", "B", "C", "D"],
            ["E", "F"],
        ],
        "net_weights": [1, 1, 1, 1, 5, 1],
        "fixed_pads": ["A", "D"],
        "starter": {
            "A": {"x": 0, "y": 0},
            "B": {"x": 8, "y": 0},
            "C": {"x": 0, "y": 8},
            "D": {"x": 8, "y": 8},
            "E": {"x": 4, "y": 4},
            "F": {"x": 0, "y": 4},
        },
        "golden": {
            "A": {"x": 2, "y": 2},
            "B": {"x": 4, "y": 2},
            "C": {"x": 2, "y": 4},
            "D": {"x": 4, "y": 4},
            "E": {"x": 3, "y": 3},
            "F": {"x": 1, "y": 3},
        },
        "overlap": {
            "A": {"x": 4, "y": 4},
            "B": {"x": 4, "y": 4},
            "C": {"x": 4, "y": 4},
            "D": {"x": 7, "y": 1},
            "E": {"x": 1, "y": 7},
            "F": {"x": 7, "y": 7},
        },
        "notes": "Matches platform/assets/placement-core.js starter/golden (HPWL 52 → 14).",
    }


def write_common_stub() -> None:
    """Ensure tiny_place.json exists for lab example copies; full common/ filled separately."""
    write(ROOT / "common" / "tiny_place.json", json.dumps(tiny_place_dict(), indent=2))


def write_build_script() -> None:
    mods = "\n".join(f"  {m['id']}" for m in MODULES)
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
{mods}
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
    write_docs()
    write_modules_md()
    write_course_readme()
    write_common_stub()
    write_build_script()
    tiny = (ROOT / "common" / "tiny_place.json").read_text(encoding="utf-8")
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
        write(base / "quiz.json", json.dumps(quiz(m), indent=2))
        if m["kind"] == "lab":
            ex = base / "examples"
            ex.mkdir(parents=True, exist_ok=True)
            (ex / "tiny_place.json").write_text(tiny, encoding="utf-8", newline="\n")
        print(f"ok {mid}")
    print(f"Scaffolded {len(MODULES)} modules under {ROOT}")


if __name__ == "__main__":
    main()
