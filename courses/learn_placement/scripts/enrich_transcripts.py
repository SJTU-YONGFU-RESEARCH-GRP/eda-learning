#!/usr/bin/env python3
"""Rewrite learn_placement lab transcripts with algorithm-specific speech (clustering depth)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SPECS = {
    "module01-01-hpwl-metrics": {
        "title": "Half-perimeter wirelength",
        "lab": "hpwl-metrics",
        "open": (
            "Half-perimeter wirelength is the teaching yardstick for placement. For each net, take the "
            "bounding box of its pins and add width plus height. On the starter six-cell instance the "
            "spread-out seed scores total HPWL fifty-two. The compact golden placement drops that to "
            "fourteen. You will compute both numbers every time you look at a placement."
        ),
        "idea": (
            "For every net, find min and max x and y among its pins, then add (maxX minus minX) plus "
            "(maxY minus minY). Sum over nets for total HPWL. Never celebrate a tiny total that piles "
            "every cell on one point—that is not a usable placement, only a collapsed metric."
        ),
    },
    "module01-03-net-models": {
        "title": "Net models for wirelength",
        "lab": "net-models",
        "open": (
            "Multi-pin nets need a model before you optimize. Bounding-box HPWL is the usual report. "
            "Clique sums every pairwise HPWL; star sums spokes from a hub. On the golden four-pin net "
            "ABCD, bbox HPWL is four, clique is sixteen, and star-from-A is eight—same pins, different "
            "numbers."
        ),
        "idea": (
            "Bbox is cheap and standard. Clique overestimates affinity on multi-pin nets. Star depends "
            "on the hub choice. Use one model for the reported objective and say which—mixing them in "
            "one table is how goldens quietly disagree."
        ),
    },
    "module02-01-force-directed-place": {
        "title": "Force-directed placement",
        "lab": "force-directed-place",
        "open": (
            "Force-directed place pulls each free cell toward the average of its net neighbors, plus a "
            "weak center pull. From the starter HPWL of fifty-two, a few lite iterations land near "
            "eighteen point seven—better wirelength, still above the golden fourteen."
        ),
        "idea": (
            "Each iteration: for free cells, blend current position toward the neighbor average with a "
            "small alpha. Fixed pads stay put. Too much alpha collapses the design; too little barely "
            "moves. Report HPWL before and after with the same net model."
        ),
    },
    "module02-03-quadratic-place": {
        "title": "Quadratic placement",
        "lab": "quadratic-place",
        "open": (
            "Quadratic-lite placement averages neighbors under fixed pads—here A and D stay pinned. "
            "From starter HPWL fifty-two the solve reaches forty-eight. Pads constrain the free cells, "
            "so you will not match free force’s eighteen point seven on this instance."
        ),
        "idea": (
            "Gauss–Seidel style: replace each free cell with a blend of neighbor average and prior "
            "coordinate so the solve does not collapse. Fixed pads anchor the system. Teaching point: "
            "pad constraints raise HPWL versus unconstrained force on the same seed."
        ),
    },
    "module02-05-analytical-place": {
        "title": "Analytical / density-aware place",
        "lab": "analytical-place",
        "open": (
            "Analytical lite first pulls for wirelength, then spreads for density with pads A and D "
            "fixed. From starter fifty-two you should land near forty-eight point one—close to "
            "quadratic, deliberately above free force, because spreading fights pure collapse."
        ),
        "idea": (
            "Wirelength stage clusters; density stage pushes cells out of overloaded bins; a light "
            "reconnect keeps HPWL from exploding. Watch both HPWL and overflow—winning wirelength "
            "while overflowing every bin is not analytical success."
        ),
    },
    "module02-07-sa-placement": {
        "title": "Simulated annealing placement",
        "lab": "sa-placement",
        "open": (
            "Simulated annealing jogs one cell at a time under an HPWL cost. With seed forty-two and "
            "sixty moves on the starter, best HPWL lands near forty-nine point six—modest improvement "
            "over fifty-two, not a force-style collapse."
        ),
        "idea": (
            "Propose a small axis move, accept improvements always, and accept worsenings with "
            "temperature probability. Keep the best iterate, not only the final temperature. Fix the "
            "seed so your golden stays stable across runs."
        ),
    },
    "module03-01-density-bins": {
        "title": "Density bins and overflow",
        "lab": "density-bins",
        "open": (
            "Density bins count cells on a grid and sum overflow above capacity. On a two-by-two grid "
            "with capacity one, both starter and golden still overflow by two—compact HPWL does not "
            "automatically mean legal density. Raise capacity to two on golden and overflow drops to one."
        ),
        "idea": (
            "Assign each cell to a bin by coordinates, count occupants, then overflow equals sum of "
            "max(zero, count minus capacity). Report HPWL and overflow together. A pretty wirelength "
            "with piled bins fails the density half of placement."
        ),
    },
    "module03-03-spread-legalize-lite": {
        "title": "Spreading / overlap relief",
        "lab": "spread-legalize-lite",
        "open": (
            "Spreading pushes overlapping or near pairs apart until a minimum pairwise distance holds. "
            "Start from the triple-overlap demo at one point, run the lite spreader, and confirm every "
            "pair clears the threshold without sending HPWL to infinity."
        ),
        "idea": (
            "While any pair sits closer than minDist, push them along their separation vector. Finish "
            "with a deterministic repair pass so the result is stable. Spreading is a legality proxy—"
            "not full row-site legalization."
        ),
    },
    "module04-01-timing-driven-place": {
        "title": "Timing-driven placement",
        "lab": "timing-driven-place",
        "open": (
            "Timing-driven place weights critical nets in the wirelength objective. On the starter, "
            "plain HPWL is fifty-two but timing-weighted HPWL is one hundred sixteen because the "
            "four-pin net carries weight five. The compact golden drops timing-weighted cost to thirty."
        ),
        "idea": (
            "Multiply each net’s HPWL by its criticality weight and sum. Heavy weights pull critical "
            "nets shorter even when plain HPWL looks fine. Always report both plain and weighted "
            "totals so you can see what the objective actually optimized."
        ),
    },
}


def render(mid: str, spec: dict) -> str:
    title = spec["title"]
    lab = spec["lab"]
    return f"""# {title}

**Module id:** {mid}
**Lab:** {lab}
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — {title}

{spec["open"]}

## Slide 2 — The idea

{spec["idea"]}

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 3 — Browser lab track

In the browser lab track, open the **{lab}** lab from the tools shelf. Load the starter placement, run the algorithm once, and read HPWL—and density when the panel shows it. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 4 — Implement track

In the implement track, open this module’s examples and the course `common/` solvers. Parse `tiny_place.json`, run the algorithm with a deterministic seed, and print coordinates plus HPWL. Match the browser goldens before you claim the checklist.

## Slide 5 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads A and D; mixing bbox and clique models in one report; keeping only the final SA iterate instead of the best; and forgetting that timing weights change the objective, not just the label.

## Slide 6 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
"""


def main() -> None:
    for mid, spec in SPECS.items():
        path = ROOT / mid / "transcript.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(mid, spec), encoding="utf-8", newline="\n")
        print("ok", mid)


if __name__ == "__main__":
    main()
