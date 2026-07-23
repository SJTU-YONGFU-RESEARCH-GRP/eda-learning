#!/usr/bin/env python3
"""Rewrite learn_legalization lab transcripts with algorithm-specific speech (clustering depth)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SPECS = {
    "module01-01-site-row-model": {
        "title": "Site and row model",
        "lab": "site-row-model",
        "open": (
            "Legalization snaps cells to a discrete grid. Our teaching chip is twelve sites wide "
            "and six high—three rows with bottoms at y zero, two, and four. Cell widths A through D "
            "are two sites; E and F are one. Total width ten fits inside twelve with room to pack."
        ),
        "idea": (
            "Every cell sits on exactly one row with a lower-left coordinate aligned to site pitch "
            "one. Width tells you how many consecutive sites the rectangle covers. The golden packing "
            "is legal; the overlap seed stacks A, B, and C at (4, 2) to show what illegal looks like."
        ),
    },
    "module01-03-legality-metrics": {
        "title": "Legality metrics",
        "lab": "legality-metrics",
        "open": (
            "Before you celebrate wirelength, ask whether the placement is legal. On the overlap seed "
            "the checker fails with overlap A/B—three cells share the middle row at x four. The golden "
            "reference passes with reason ok."
        ),
        "idea": (
            "Check on-row placement, site alignment, in-chip bounds, and pairwise overlap. Report "
            "displacement as L1 Manhattan distance from the origin layout—Abacus moves four total "
            "units on this instance, overlap removal moves six. Pair legality with HPWL after legalize."
        ),
    },
    "module02-01-greedy-snap": {
        "title": "Greedy snap",
        "lab": "greedy-snap",
        "open": (
            "Global placement leaves fractional coordinates—the float seed puts A near (3.7, 1.2) and "
            "B near (4.1, 1.4). Greedy snap rounds x to the nearest site and y to the nearest row. "
            "A lands at (4, 2)—the same site as B."
        ),
        "idea": (
            "Snap quantizes coordinates but does not remove overlap. After snap, A and B still fail "
            "with overlap A/B. Teaching point: snap is necessary, not sufficient—you need overlap "
            "removal or Abacus packing next."
        ),
    },
    "module02-03-overlap-removal": {
        "title": "Overlap removal",
        "lab": "overlap-removal",
        "open": (
            "Overlap removal snaps first, then left-packs each row without changing row assignment. "
            "From the triple stack at (4, 2), A stays at four, B moves to six, C to eight on the "
            "middle row—legal with displacement six and HPWL thirty-two."
        ),
        "idea": (
            "Sort movables by x within each row and place left without overlap. D, E, and F keep their "
            "seed roles on other rows. This is the same shelf pack Tetris uses—simple, deterministic, "
            "and a good global legalize baseline."
        ),
    },
    "module02-05-abacus-row-pack": {
        "title": "Abacus row packing",
        "lab": "abacus-row-pack",
        "open": (
            "Abacus-lite processes cells by increasing x and tries every row. For each trial it finds "
            "the leftmost legal site and picks the row with minimum L1 displacement from the origin. "
            "On the overlap seed: A at (4, 2), B at (4, 0), C at (4, 4)."
        ),
        "idea": (
            "Cross-row spread beats single-row shelf pack on displacement—four versus six here—with "
            "HPWL thirty-eight versus thirty-two for Tetris. Abacus is the detailed legalizer in this "
            "course: more search, less movement."
        ),
    },
    "module02-07-tetris-row-pack": {
        "title": "Tetris row packing",
        "lab": "tetris-row-pack",
        "open": (
            "Tetris-lite assigns each cell to its nearest row, then left-packs like overlap removal. "
            "On the overlap seed the result matches overlap removal: A at four, B at six, C at eight "
            "on row two—legal, displacement six, HPWL thirty-two."
        ),
        "idea": (
            "Tetris is simpler than Abacus but moves cells farther on this toy. Contrast disp six "
            "versus Abacus disp four. Trade simpler control flow against a tighter displacement budget "
            "and slightly higher HPWL when Abacus wins movement."
        ),
    },
    "module03-01-fixed-macros": {
        "title": "Fixed macros",
        "lab": "fixed-macros",
        "open": (
            "Macro D is locked at (8, 4) on the top row—width two blocks sites eight and nine. Run "
            "Abacus with fixed macros: D never moves, movables pack around the obstacle, and the run "
            "stays legal with displacement four on this instance."
        ),
        "idea": (
            "Fixed cells are placed first; occupied intervals block shelf and Abacus trials on that row. "
            "Legality adds a macro check—any drift off the lock fails. Movable cells must route around "
            "macro sites, not slide through them."
        ),
    },
    "module03-03-displacement-hpwl": {
        "title": "Displacement versus HPWL",
        "lab": "displacement-hpwl",
        "open": (
            "Legalization cost combines HPWL and displacement: cost equals HPWL plus lambda times "
            "displacement from the pre-legalize layout. Abacus on the overlap seed reports HPWL "
            "thirty-eight and displacement four."
        ),
        "idea": (
            "Lambda one gives cost forty-two; lambda five gives cost fifty-eight on the same legal "
            "Abacus result. Higher lambda favors staying near global placement even when wirelength "
            "could be slightly better under a different packer."
        ),
    },
    "module04-01-detailed-vs-global": {
        "title": "Detailed versus global legalize",
        "lab": "detailed-vs-global",
        "open": (
            "Global legalize lite maps to Tetris shelf pack—displacement six, HPWL thirty-two. "
            "Detailed legalize lite maps to Abacus—displacement four, HPWL thirty-eight. Both are "
            "legal on the overlap seed; metrics pick the winner."
        ),
        "idea": (
            "Pick global Tetris when you want a fast pass and can afford extra movement. Pick detailed "
            "Abacus when displacement budget is tight. Report both pipelines side by side in "
            "regressions—legal first, then disp and HPWL."
        ),
    },
}


def render_lab(mid: str, spec: dict) -> str:
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

In the browser lab track, open the **{lab}** lab from the tools shelf. Load the overlap or float starter, run the legalizer once, and read legality plus displacement and HPWL when the panel shows them. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 4 — Implement track

In the implement track, open this module's examples and the course `common/` solvers. Parse `tiny_legal.json`, run the algorithm with deterministic coordinates, and print legality, displacement, and HPWL. Match the browser goldens before you claim the checklist.

## Slide 5 — Pitfalls

Common traps: assuming snap alone legalizes; forgetting site width when checking overlap; ignoring fixed macro D at (8, 4); reporting HPWL without legality; and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

## Slide 6 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.
"""


INTRO = """# Welcome to legalization for EDA

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to legalization

Global placement spreads cells for wirelength and density—but coordinates float freely. Legalization snaps them to rows and sites, removes overlaps, and respects fixed macros before routing. This course teaches that transition on a tiny twelve-site grid so detailed routing has a legal canvas.

## Slide 2 — What you'll build

You'll model sites and rows, check legality, greedy-snap floats, remove overlaps, and pack rows with Abacus and Tetris-style algorithms. Then legalize around fixed macros, measure displacement versus HPWL, and contrast global versus detailed passes. Nine browser labs have step-by-step algorithm walkthroughs with verified goldens.

## Slide 3 — Prerequisite path

Finish **learn_placement** first: you need global-place floats and HPWL intuition. Floorplanning and clustering further upstream set the outline; legalization assumes cells already have rough (x, y) targets.

## Slide 4 — Two tracks

Every lab offers Track A—implement on `tiny_legal.json`—and Track B—browser labs with interactive walkthroughs. Good rhythm: browser for row/site intuition, implement to harden checkers and packers.

## Slide 5 — How to move

Read each README, pick a track, work the checklist. Keep legality, displacement, and HPWL as habits. When intro checklist is done, continue to site and row model—the geometry contract for every later algorithm.
"""

WRAP = """# Legalization path complete

**Module id:** module99-00-wrap
**Lab:** none (wrap)
**Tracks:** recap · next course

## Slide 1 — Legalization path complete

You've walked from site/row geometry through legality checks, greedy snap, overlap removal, Abacus and Tetris packing, fixed macros, displacement versus HPWL, and global vs detailed pipelines. Walkthrough goldens lock disp four for Abacus and disp six for Tetris on the shared overlap seed.

## Slide 2 — What you can do now

You can explain why legalization follows global placement. You can check row/site legality, snap floats, clear overlaps, and pack rows. You can respect fixed macros and report displacement alongside HPWL. You are building algorithm literacy—not shipping a foundry legalizer.

## Slide 3 — Close the gaps

If you mainly used browser labs, implement legality checking plus one row packer in Track A. If you mainly coded, skim browser walkthroughs for visual row intuition. Placement prereqs should feel connected: floats in, legal sites out.

## Slide 4 — Next courses

Natural next steps are detailed routing and congestion-aware flows. Keep your tiny_legal harness; routing courses consume legal coordinates. Open **`eda.md`** in the parent monorepo for the full PD spine.

## Slide 5 — Your turn

Review the wrap checklist. Name three packing strategies and when you'd pick each. When ready, take the short quiz, then continue along the PD path.
"""


def main() -> None:
    for mid, spec in SPECS.items():
        path = ROOT / mid / "transcript.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_lab(mid, spec), encoding="utf-8", newline="\n")
        print("ok", mid)

    (ROOT / "module00-00-intro" / "transcript.md").write_text(INTRO, encoding="utf-8", newline="\n")
    print("ok", "module00-00-intro")

    (ROOT / "module99-00-wrap" / "transcript.md").write_text(WRAP, encoding="utf-8", newline="\n")
    print("ok", "module99-00-wrap")


if __name__ == "__main__":
    main()
