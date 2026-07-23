#!/usr/bin/env python3
"""Write polished transcript.md from assets/STEPS.md for algorithm labs.

Skips modules that already contain <!-- algorithm-walkthrough --> unless --force.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

COURSE = Path(__file__).resolve().parents[1]

# Closing slides per lab (browser / implement / pitfalls / your turn)
CLOSING: dict[str, dict[str, str]] = {
    "module01-05-size-constrained-agglomerative": {
        "title": "Size-constrained agglomerative clustering",
        "lab": "size-constrained-agglomerative",
        "opener": (
            "Size caps change which merges are legal. You’ll watch greedy agglomeration "
            "with capacity two on the tiny graph—and see why A–B–C can no longer form."
        ),
        "browser": (
            "In the browser lab, load the starter with capacity two, then compare presets "
            "against unconstrained K equals two. Clear the challenges for blocked size-three "
            "clusters and the AB|C|DE parts."
        ),
        "implement": (
            "Run greedy merge with capacity two and confirm cutsize eight with parts AB|C|DE. "
            "Then lift capacity to three and recover the unconstrained ABC|DE cutsize three."
        ),
        "code": (
            "export PYTHONPATH=../common\n"
            "python ../common/solvers.py examples/tiny_graph.json --k 2 --capacity 2"
        ),
        "pitfalls": (
            "Forgetting to check capacity before contracting is the classic bug. "
            "Also watch stale affinities after a blocked merge candidate is skipped."
        ),
        "your_turn": (
            "Match the capacity-two golden, finish the checklist and quiz, then continue "
            "to label propagation."
        ),
    },
    "module02-03-spectral-bisection": {
        "title": "Spectral bisection",
        "lab": "spectral-bisection",
        "opener": (
            "Spectral bisection uses the graph Laplacian and its Fiedler vector to propose "
            "a balanced cut. You’ll watch the order and the chosen split land on cutsize three."
        ),
        "browser": (
            "In the browser lab, run spectral bisection and inspect the Fiedler order. "
            "Clear challenges for cutsize three and the ABC versus DE parts."
        ),
        "implement": (
            "Run the spectral mode on the tiny graph. Confirm cutsize three and the natural "
            "clusters. Re-implement the sweep yourself; a dense tiny eigensolve is fine at course scale."
        ),
        "code": (
            "export PYTHONPATH=../common\n"
            "python ../common/solvers.py examples/tiny_graph.json --mode spectral"
        ),
        "pitfalls": (
            "Ignoring balance can isolate one node. Numerical noise can scramble near-ties—"
            "use a stable sort. Disconnected graphs need explicit component handling."
        ),
        "your_turn": (
            "Match cutsize three, finish the checklist and quiz, then continue to Kernighan–Lin."
        ),
    },
    "module03-01-multilevel-clustering": {
        "title": "Multilevel clustering",
        "lab": "multilevel-clustering",
        "opener": (
            "Multilevel clustering coarsens, partitions, then refines. You’ll watch greedy "
            "coarsening to two clusters followed by FM polish—landing on cutsize three."
        ),
        "browser": (
            "In the browser lab, run multilevel and compare with a plain greedy seed. "
            "Clear challenges for the refined ABC|DE result."
        ),
        "implement": (
            "Run multilevel on the tiny graph and confirm cutsize three. Re-implement "
            "project-and-refine until the unit test passes."
        ),
        "code": (
            "export PYTHONPATH=../common\n"
            "python ../common/solvers.py examples/tiny_graph.json --mode multilevel"
        ),
        "pitfalls": (
            "Skipping refinement leaves coarsening artifacts. Projecting labels incorrectly "
            "scrambles the fine-level seed. Too aggressive coarsening can erase structure."
        ),
        "your_turn": (
            "Match the golden, finish the checklist and quiz, then continue to hypergraph clustering."
        ),
    },
    "module03-03-hypergraph-clustering": {
        "title": "Hypergraph clustering",
        "lab": "hypergraph-clustering",
        "opener": (
            "Netlists are hypergraphs—one net can touch many pins. You’ll watch greedy "
            "clustering on a tiny hypergraph where multi-pin net n1 pulls A–B–C together."
        ),
        "browser": (
            "In the browser lab, load the starter hypergraph and run greedy clustering to K equals two. "
            "Confirm hyperedge cut one for ABC versus DE."
        ),
        "implement": (
            "Run hypergraph greedy to K equals two. Confirm hyperedge cut one and the natural clusters."
        ),
        "code": (
            "export PYTHONPATH=../common\n"
            "python ../common/solvers.py examples/tiny_hypergraph.json --mode hypergraph --k 2"
        ),
        "pitfalls": (
            "Clique-expanding hyperedges changes the objective. Counting a cut once per "
            "hyperedge—not per pair—is required. Empty or singleton nets must be filtered."
        ),
        "your_turn": (
            "Match hyperedge cut one, finish the checklist and quiz, then continue to congestion-aware clustering."
        ),
    },
    "module04-01-congestion-aware-clustering": {
        "title": "Congestion-aware clustering",
        "lab": "congestion-aware-clustering",
        "opener": (
            "When bridge edges are congested, cutting them becomes expensive. You’ll watch "
            "FM under a congestion penalty and see how lambda reshapes the partition."
        ),
        "browser": (
            "In the browser lab, compare lambda zero with lambda five from the same bad seed. "
            "Watch the penalty drop to zero when the congested bridge is avoided."
        ),
        "implement": (
            "Run congestion-aware partition at lambda zero and five. Confirm plain cut three "
            "with penalty nine at lambda zero, and plain five with penalty zero at lambda five."
        ),
        "code": (
            "export PYTHONPATH=../common\n"
            "python ../common/solvers.py examples/tiny_graph.json --mode congestion "
            "--seed ../module02-05-kernighan-lin/examples/seed_partition.json "
            "--congestion examples/congestion.json --lambda 5"
        ),
        "pitfalls": (
            "Applying congestion only after FM misses the point—weights must change before moves. "
            "Huge lambda can ignore connectivity entirely."
        ),
        "your_turn": (
            "Match both lambda goldens, finish the checklist and quiz, then continue to timing-aware clustering."
        ),
    },
    "module04-03-timing-aware-clustering": {
        "title": "Timing-aware clustering",
        "lab": "timing-aware-clustering",
        "opener": (
            "Critical nets should stay uncut. You’ll watch FM on criticality-weighted edges "
            "and land on cutsize three with weighted cut seven—protecting the A–B–C path."
        ),
        "browser": (
            "In the browser lab, run timing-aware refinement from the bad seed. "
            "Confirm plain cut three and weighted cut seven."
        ),
        "implement": (
            "Run timing-aware mode and confirm ABC versus DE, plain three, weighted seven."
        ),
        "code": (
            "export PYTHONPATH=../common\n"
            "python ../common/solvers.py examples/tiny_graph.json --mode timing "
            "--seed ../module02-05-kernighan-lin/examples/seed_partition.json "
            "--criticality examples/criticality.json"
        ),
        "pitfalls": (
            "Criticality of one means no boost—document defaults. Mixing plain and weighted "
            "metrics in the same table confuses compares."
        ),
        "your_turn": (
            "Match the golden, finish the checklist and quiz, then continue to offline benchmark compare."
        ),
    },
}


def parse_steps(steps_md: Path) -> list[dict[str, str]]:
    text = steps_md.read_text(encoding="utf-8")
    parts = re.split(r"^## Step (\d+) — (.+)$", text, flags=re.M)
    out = []
    i = 1
    while i + 2 < len(parts):
        _n, title, body = parts[i], parts[i + 1], parts[i + 2]
        img = re.search(r"!\[[^\]]*\]\((steps/[^)]+)\)", body)
        cap = re.search(r"\*\*Caption \(transcript\):\*\*\s*(.+)", body)
        if img and cap:
            out.append(
                {
                    "title": title.strip(),
                    "image": f"assets/{img.group(1)}",
                    "caption": cap.group(1).strip(),
                }
            )
        i += 3
    return out


def write_transcript(mod: Path, meta: dict[str, str], steps: list[dict[str, str]]) -> None:
    lines = [
        f"# {meta['title']}",
        "",
        f"**Module id:** {mod.name}",
        f"**Lab:** {meta['lab']}",
        "**Tracks:** A (implement) · B (browser lab)",
        "",
        f"## Slide 1 — {meta['title']}",
        "",
        meta["opener"],
        "",
        "<!-- algorithm-walkthrough -->",
        "",
    ]
    n = 2
    for s in steps:
        lines += [
            f"## Slide {n} — {s['title']}",
            "",
            f"![{s['title']}]({s['image']})",
            "",
            s["caption"],
            "",
        ]
        n += 1
    lines += [
        "<!-- /algorithm-walkthrough -->",
        "",
        f"## Slide {n} — Browser lab track",
        "",
        meta["browser"],
        "",
    ]
    n += 1
    lines += [
        f"## Slide {n} — Implement track",
        "",
        meta["implement"],
        "",
        "```bash",
        meta["code"],
        "```",
        "",
    ]
    n += 1
    lines += [
        f"## Slide {n} — Pitfalls to watch",
        "",
        meta["pitfalls"],
        "",
    ]
    n += 1
    lines += [
        f"## Slide {n} — Your turn",
        "",
        meta["your_turn"],
        "",
    ]
    (mod / "transcript.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {mod / 'transcript.md'}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for name, meta in CLOSING.items():
        mod = COURSE / name
        steps_md = mod / "assets" / "STEPS.md"
        if not steps_md.is_file():
            print(f"skip {name}: no STEPS.md")
            continue
        tr = mod / "transcript.md"
        if tr.is_file() and "algorithm-walkthrough" in tr.read_text(encoding="utf-8") and not args.force:
            print(f"skip {name}: already has walkthrough")
            continue
        steps = parse_steps(steps_md)
        if len(steps) < 3:
            print(f"skip {name}: only {len(steps)} steps")
            continue
        write_transcript(mod, meta, steps)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
