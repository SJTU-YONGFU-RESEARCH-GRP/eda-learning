#!/usr/bin/env python3
"""Refresh legalization EXAMPLES + transcript pseudocode (≤12 lines per fence for slides)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Compact slide fences (≤ CODE_SLIDE_MAX_LINES=12). EXAMPLES may mirror these.
LABS: list[tuple[str, str, str, str, str, str]] = [
    (
        "module01-01-site-row-model",
        "Site and row model",
        "site/row grid model and cell widths",
        """\
INPUT: chip W×H, siteW, rowH, rows Y[], widths w[c]
OUTPUT: legal coordinate rules
for each cell c:
  x multiple of siteW; y in Y[]
  occupies [x, x+w[c]) × [y, y+rowH)
GOLDEN: W=12 H=6 siteW=1 rowH=2 Y={0,2,4}
widths A–D=2 E–F=1 (total 10 ≤ 12)""",
        "Pseudocode is the written sketch of the algorithm before you code it. For this module the sketch is the site and row model itself: inputs are chip size, site pitch, row bottoms, and cell widths. Outputs are the rules every legal packing must obey.",
        "Read the sketch as a contract. Every cell lower-left sits on a site and a row bottom. Width tells how many consecutive sites the rectangle covers. Our teaching chip is twelve by six with three rows—that is the instance every later lab shares.",
    ),
    (
        "module01-03-legality-metrics",
        "Legality metrics",
        "legality checker + displacement + HPWL",
        """\
INPUT: positions, widths, chip, optional fixed
OUTPUT: legal?, reason, disp, HPWL
for each cell c:
  fail if off-site, off-row, outside, or macro moved
for each same-row pair (a,b):
  fail if [x,x+w) intervals overlap
disp = Σ|Δx|+|Δy|; HPWL = Σ net bbox (centers)
GOLDEN: overlap → "overlap A/B"; golden → "ok\"""",
        "Before you trust wirelength, write a legality checker in pseudocode. Inputs are coordinates and widths. The loop walks cells and pairs. The stop condition is the first failure reason—or ok when every check passes.",
        "The sketch also defines the metrics you report after a legalize pass: L1 displacement from the origin layout, and HPWL from cell centers. On the overlap seed the checker fails with overlap A/B; the golden packing returns ok.",
    ),
    (
        "module02-01-greedy-snap",
        "Greedy snap",
        "greedy site/row snap from float coordinates",
        """\
INPUT: float positions, widths, rows Y[], chip W
OUTPUT: snapped positions (may still overlap)
for each movable cell c:
  x ← round(x) clamped to [0, W−w[c]]
  y ← nearest row in Y[]
fixed macros: keep locked (x,y)
NOTE: snap ≠ legal — A,B may share a site
GOLDEN float: A→(4,2), B→(4,2) still overlap""",
        "Greedy snap is the first written loop after global place. Pseudocode here has one pass: for each movable cell, round x to a site and y to the nearest row. Fixed macros stay put.",
        "The important line in the sketch is the note after the loop: snap does not remove overlap. On the float starter, A and B both land at four comma two—so legality still fails until a packer runs.",
    ),
    (
        "module02-03-overlap-removal",
        "Overlap removal",
        "per-row left pack after snap",
        """\
INPUT: positions, widths, rows, fixed macros
OUTPUT: legal packing (if capacity allows)
snap all movables to sites/rows
for each row y:
  sort movables by x; left-pack (skip macros)
report legal?, disp, HPWL
GOLDEN: A@4 B@6 C@8 on y=2; disp=6; HPWL=32""",
        "Overlap removal is a two-phase sketch: snap first, then pack each row. Pseudocode makes the phases explicit so you do not merge them into one vague “fix overlaps” bullet.",
        "Inside each row, sort by x and place left without interval overlap, skipping fixed macro blocks. On the teaching seed that yields A at four, B at six, C at eight on the middle row—displacement six, HPWL thirty-two.",
    ),
    (
        "module02-05-abacus-row-pack",
        "Abacus row packing",
        "Abacus-lite: try each row, min L1 displacement",
        """\
INPUT: origin, widths, rows Y[], fixed macros
OUTPUT: legal pack minimizing Σ L1 move
place fixed macros first
order ← movables by origin.x
for each cell c in order:
  for each row y: trial leftmost legal x
  keep (x,y) with min |Δx|+|Δy| to origin
  place c at best
GOLDEN: A(4,2) B(4,0) C(4,4); disp=4; HPWL=38""",
        "Abacus needs a nested loop in pseudocode: outer cells in x order, inner trial of every row. For each trial you compute leftmost legal x and an L1 cost back to the origin, then keep the cheapest row.",
        "Fixed macros sit first so their intervals block later trials. On the overlap seed the sketch lands A at four two, B at four zero, C at four four—displacement four and HPWL thirty-eight, tighter movement than Tetris.",
    ),
    (
        "module02-07-tetris-row-pack",
        "Tetris row packing",
        "nearest-row assign then left pack",
        """\
INPUT: positions, widths, rows Y[], fixed macros
OUTPUT: legal packing (shelf / Tetris-lite)
for each movable c: y ← nearest row (freeze)
then per-row left pack (see overlap removal)
GOLDEN: A@4 B@6 C@8 on y=2; disp=6; HPWL=32
COMPARE: Abacus disp=4 (more search)""",
        "Tetris pseudocode is shorter than Abacus on purpose. First assign each cell to its nearest row and freeze that choice. Then reuse the per-row left pack from overlap removal.",
        "Same teaching seed, same numbers as overlap removal: displacement six, HPWL thirty-two. Write the compare line in the sketch so you remember Abacus spends search to cut displacement to four.",
    ),
    (
        "module03-01-fixed-macros",
        "Fixed macros",
        "Abacus with locked macro obstacles",
        """\
INPUT: positions, widths, fixed F (e.g. D@(8,4))
OUTPUT: legal pack; macros never move
place every f in F at locked (x,y)
run Abacus/Tetris on movables only
F intervals block try-place / left-pack
fail legality if any macro drifted
GOLDEN: D stays (8,4); Abacus disp=4; legal""",
        "Macro legalization adds one precondition to the Abacus sketch: place locked cells first. Their site intervals become obstacles for every later try-place on that row.",
        "The legality line in the sketch is new too—if D drifts off eight comma four, the packing fails even when overlaps are gone. On this instance Abacus still finishes legal with displacement four.",
    ),
    (
        "module03-03-displacement-hpwl",
        "Displacement versus HPWL",
        "cost = HPWL + λ · displacement",
        """\
INPUT: legal positions, origin, nets, λ≥0
OUTPUT: cost, HPWL, disp
disp ← Σ|Δx|+|Δy| vs origin
HPWL ← Σ net bbox (cell centers)
cost ← HPWL + λ · disp
GOLDEN Abacus: HPWL=38 disp=4
  λ=1 → 42;  λ=5 → 58""",
        "This module’s pseudocode is a cost function, not a packer. After you have a legal layout, compute displacement and HPWL, then combine them with lambda.",
        "Plug in the Abacus goldens: thirty-eight plus lambda times four. Lambda one costs forty-two; lambda five costs fifty-eight. Higher lambda means the sketch favors staying near the global place.",
    ),
    (
        "module04-01-detailed-vs-global",
        "Detailed versus global legalize",
        "global=Tetris, detailed=Abacus",
        """\
INPUT: illegal / global positions
global:   TetrisLite → disp=6 HPWL=32
detailed: AbacusLite → disp=4 HPWL=38
both must report legal=true
CHOOSE detailed when disp budget is tight
CHOOSE global when a fast shelf pack is enough""",
        "Here the sketch is two named pipelines on the same seed. Global legalize lite means Tetris. Detailed legalize lite means Abacus. Pseudocode names both so regressions do not mix the labels.",
        "Both pipelines must end legal. Then compare displacement six versus four and HPWL thirty-two versus thirty-eight. Pick detailed when movement budget is tight; pick global when speed matters more.",
    ),
]

EXAMPLES_TMPL = """# Examples — {title}

Track A (implement). Use `examples/tiny_legal.json` and `../../common/` solvers.

## Algorithm

**{algo}**

## API

```text
# Python (courses/learn_legalization/common/)
load_legal / greedy_snap / overlap_remove / abacus_lite / tetris_lite
check_legality · total_displacement · total_hpwl
```

## Pseudocode

```text
{pseudo}
```

## Starter prompts

1. Implement the pseudocode above (or call the matching `common/` solver).
2. Print legality, displacement, and HPWL; match the GOLDEN line.
3. Change one knob (macro lock, λ, or packer) and report the delta.

## Expected artifacts

- Legal (x, y) per cell (or intentional illegal before-state)
- Legality + displacement / HPWL (and cost when relevant)
- Note tying the run to the pseudocode phases

## Stretch

Lock macro D at (8,4) or sweep λ; keep the same metrics API.
"""

SLIDE_CONCEPT = """## Slide {n} — Pseudocode

{spoken}

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.
"""

SLIDE_SKETCH = """## Slide {n} — Algorithm sketch

{spoken}

```text
{pseudo}
```
"""


def write_examples() -> None:
    for mid, title, algo, pseudo, _c, _s in LABS:
        (ROOT / mid / "EXAMPLES.md").write_text(
            EXAMPLES_TMPL.format(title=title, algo=algo, pseudo=pseudo.rstrip()),
            encoding="utf-8",
            newline="\n",
        )


def renumber_slides(text: str) -> str:
    pattern = re.compile(r"^## Slide \d+ — (.+)$", re.M)
    idx = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal idx
        idx += 1
        return f"## Slide {idx} — {m.group(1)}"

    return pattern.sub(repl, text)


def inject_transcript(mid: str, title: str, pseudo: str, concept: str, sketch: str) -> None:
    path = ROOT / mid / "transcript.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\n## Slide \d+ — Pseudocode\n.*?(?=\n## Slide |\n<!-- )",
        "\n",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r"\n## Slide \d+ — Algorithm sketch\n.*?(?=\n## Slide |\n<!-- )",
        "\n",
        text,
        count=1,
        flags=re.S,
    )
    block = (
        "\n"
        + SLIDE_CONCEPT.format(n=99, spoken=concept).rstrip()
        + "\n\n"
        + SLIDE_SKETCH.format(n=99, spoken=sketch, pseudo=pseudo.rstrip()).rstrip()
        + "\n\n"
    )
    m = re.search(
        r"(## Slide 2 — The idea\n\n.*?)(\n(?=<!-- algorithm-walkthrough -->|## Slide ))",
        text,
        re.S,
    )
    if not m:
        raise SystemExit(f"cannot find Slide 2 in {mid}")
    text = text[: m.end(1)] + "\n" + block + text[m.start(2) :]
    text = renumber_slides(text)
    text = text.replace(
        "Load the overlap or float starter, run the legalizer once, and read legality plus displacement and HPWL when the panel shows them.",
        "Open the interactive lab, place or snap cells on the site and row grid—or use an Apply helper—then Check. Reveal golden is study-only.",
    )
    text = text.replace(
        "In the implement track, open this module's examples and the course `common/` solvers.",
        "In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers.",
    )
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    nlines = len(pseudo.strip().splitlines())
    print(f"OK  {mid} fence_lines={nlines} ({title})")


def main() -> None:
    write_examples()
    for mid, title, _a, pseudo, concept, sketch in LABS:
        assert len(pseudo.strip().splitlines()) <= 12, mid
        inject_transcript(mid, title, pseudo, concept, sketch)
    print("DONE")


if __name__ == "__main__":
    main()
