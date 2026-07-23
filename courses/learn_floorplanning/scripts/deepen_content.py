#!/usr/bin/env python3
"""Rewrite learn_floorplanning lab transcripts + quizzes to clustering depth."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# module id → (lab, title, opener, browser, implement, pitfall, your_turn, quiz)
LABS = [
    (
        "module01-01-fixed-outline",
        "fixed-outline",
        "Fixed-outline constraints",
        "Floorplanning on this course uses a fixed outline ten by eight. Modules A through E must pack inside—no growing the chip. In this lab you’ll reject illegal packings before you ever talk about density.",
        "Open the fixed-outline lab. Show the bad seed: E overflows past the right edge. Then show overlap, then golden. Watch legality flip from false to true when the golden packing loads.",
        "Parse tiny_modules.json, assign (x, y), and implement containment plus pairwise non-overlap. On the golden packing, legality must pass; on the bad seed with E at nine, it must fail with E outside the outline.",
        "Off-by-one edges, treating centers as rectangles, and celebrating density on illegal layouts. Edge-touching is allowed; interior overlap is not.",
        "Get a legal packing of A through E inside ten by eight. Quiz checks the overflow failure and the golden pass. Next: deadspace fifty-seven on this same instance.",
        [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "On the bad seed, legality fails because…",
                "choices": [
                    "Density is too low",
                    "E overflows the right edge (x+w = 11 > 10)",
                    "A is soft",
                    "Deadspace is 57",
                ],
                "answer": 1,
                "explain": "E at x=9 with w=2 exceeds outline width 10.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "The golden packing of A–E inside 10×8 is legal.",
                "answer": True,
                "explain": "Containment and non-overlap both hold.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "Edge-touching rectangles count as illegal overlap in this course.",
                "answer": False,
                "explain": "Only positive-area interior overlap is illegal.",
            },
            {
                "id": "q4",
                "type": "multiple_choice",
                "prompt": "Outline size for the teaching instance is…",
                "choices": ["8×8", "10×8", "12×10", "9×3"],
                "answer": 1,
                "explain": "Fixed outline W×H = 10×8.",
            },
        ],
    ),
    (
        "module01-03-area-deadspace",
        "area-deadspace",
        "Area, packing density, whitespace/deadspace",
        "With a legal packing in hand, score the whitespace. Module areas sum to twenty-three; the outline is eighty; deadspace is fifty-seven; density is zero point two eight seven five.",
        "Open area-deadspace, load the golden packing, and read the metrics panel: module area twenty-three, outline eighty, deadspace fifty-seven, density zero point two eight seven five.",
        "Implement moduleAreaSum, outlineArea, deadspace, and density. Assert deadspace equals eighty minus twenty-three on the starter modules—independent of placement when sizes are fixed.",
        "Reporting density on an illegal pack; mixing outline area with bounding-box area; forgetting soft A still contributes area six at three by two.",
        "Print the area trio on every run. Next lab builds a slicing polish whose bounding box is nine by three inside this outline.",
        [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "Module area sum on the starter is…",
                "choices": ["18", "23", "57", "80"],
                "answer": 1,
                "explain": "6+6+4+3+4 = 23.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "Deadspace for outline 10×8 is…",
                "choices": ["23", "57", "80", "9"],
                "answer": 1,
                "explain": "80 − 23 = 57.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "Density equals 23/80 = 0.2875 on the starter.",
                "answer": True,
                "explain": "moduleArea / outlineArea.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": "Whitespace fraction 57/80 equals 0.7125.",
                "answer": True,
                "explain": "Complement of density.",
            },
        ],
    ),
    (
        "module02-01-slicing-floorplan",
        "slicing-floorplan",
        "Slicing tree / polish expression packing",
        "Slicing floorplans use through-cuts. The golden polish A D H B V C V E V stacks A under D, then attaches B, C, and E with vertical cuts—bounding box nine by three.",
        "Open slicing-floorplan and Evaluate polish. Confirm bounding width nine, height three, and a legal packing inside ten by eight.",
        "Implement postfix evaluation for H and V. On the golden token list, assert width nine, height three, and is_legal_packing true.",
        "Swapping H/V meanings; leaving polish operands on the stack; assuming every packing is slicing—wheels need other reps.",
        "Ship a legal polish pack with BB nine by three. Next: B-star trees for non-slicing adjacency.",
        [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "Golden polish bounding box is…",
                "choices": ["10×8", "9×3", "5×5", "3×9"],
                "answer": 1,
                "explain": "evalPolish(A D H B V C V E V) → 9×3.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "The golden polish packing is legal inside the 10×8 outline.",
                "answer": True,
                "explain": "9≤10 and 3≤8 with no overlaps.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "In this course, operator H means…",
                "choices": [
                    "Horizontal through-cut stacking children vertically",
                    "Always place on the left",
                    "Hyperedge cut",
                    "Ignore heights",
                ],
                "answer": 0,
                "explain": "H stacks; V places side by side.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": "Every packing is a slicing floorplan.",
                "answer": False,
                "explain": "Non-slicing wheels need B* / SP.",
            },
        ],
    ),
    (
        "module02-03-bstar-tree",
        "bstar-tree",
        "B*-tree floorplan representation",
        "B-star stores packing adjacency: left child sits right-of the parent; right child sits above on a contour. Root A at the origin; left chain B then C then E; right child D above A.",
        "Open bstar-tree and Pack B*-tree. Confirm A at zero comma zero, B at x equals three, D above A, and a legal five-module packing.",
        "Build the golden tree and contour-pack it. Assert A at (0,0), B.x equals A.x plus A.w, D.y at least A.h, and legality true.",
        "Reversing left/right geometry; stale contour segments; treating the tree as a netlist.",
        "Produce the legal B-star packing. Next: sequence-pair permutations as another encoding.",
        [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "In the golden B*, A is placed at (0,0).",
                "answer": True,
                "explain": "Root packs at the origin.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "Left child means right-of parent in this packing convention.",
                "answer": True,
                "explain": "Left → +x; right → above via contour.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "Golden B* left chain order is…",
                "choices": ["E→C→B", "B→C→E", "D→A→B", "C→A→E"],
                "answer": 1,
                "explain": "A.left = B→C→E.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": "The golden B* packing is legal inside 10×8.",
                "answer": True,
                "explain": "Contour pack of A–E fits.",
            },
        ],
    ),
    (
        "module02-05-sequence-pair",
        "sequence-pair",
        "Sequence-pair representation",
        "Sequence pair uses positive permutation A B C E D and negative D A B C E. Longest-path packing from left-of and below constraints places all five modules legally.",
        "Open sequence-pair and Pack sequence pair. Confirm five modules, non-negative coordinates, and legality true on the golden permutations.",
        "Implement longest-path SP packing. Assert pos and neg are the same five ids, and the golden pair packs legally.",
        "Mismatched id sets between pos and neg; swapping the horizontal/vertical rules; negative coordinates from a buggy DP.",
        "Pack the golden sequences legally. Next: simulated annealing that prefers legal low-cost neighbors.",
        [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "Golden positive sequence starts with…",
                "choices": ["D", "A", "E", "C"],
                "answer": 1,
                "explain": "pos = A B C E D.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "Golden negative sequence starts with…",
                "choices": ["A", "D", "B", "E"],
                "answer": 1,
                "explain": "neg = D A B C E.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "Pos and neg are permutations of the same five module ids.",
                "answer": True,
                "explain": "Required for a valid sequence pair.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": "The golden SP packing is legal.",
                "answer": True,
                "explain": "Longest-path pack of the teaching pair is legal.",
            },
        ],
    ),
    (
        "module03-01-simulated-annealing-fp",
        "simulated-annealing-fp",
        "Simulated annealing floorplan search",
        "Toy cost adds one thousand when a packing is illegal. The bad overflow seed sits near one thousand forty-four; the golden legal packing scores about thirty-six. Annealing should move toward legal, lower cost.",
        "Open simulated-annealing-fp. Show bad, note cost at least one thousand. Show golden or Improve—cost drops below one thousand and legality becomes true.",
        "Implement cost with an illegality penalty, plus deadspace and HPWL terms. Assert cost(golden) is less than cost(bad), and saSwap only exchanges coordinates.",
        "Accepting illegal states without penalty; forgetting to rescore after a swap; cooling so fast you never escape the bad seed.",
        "Demonstrate one improve step from bad to golden. Next: soft module A reshaped from three by two to two by three.",
        [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Illegal packings add a +1000 term in the toy cost.",
                "answer": True,
                "explain": "Penalty dominates bad-seed cost.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "cost(golden) is less than cost(bad) on the starter.",
                "answer": True,
                "explain": "Golden is legal; bad pays the penalty.",
            },
            {
                "id": "q3",
                "type": "multiple_choice",
                "prompt": "A simple SA neighbor in this lab…",
                "choices": [
                    "Deletes modules",
                    "Swaps two modules’ coordinates (keeps sizes)",
                    "Changes the outline to 20×20",
                    "Ignores legality forever",
                ],
                "answer": 1,
                "explain": "saSwap exchanges lower-left corners.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": "After Improve, the packing should be legal.",
                "answer": True,
                "explain": "Improve loads the golden legal pack.",
            },
        ],
    ),
    (
        "module03-03-soft-module-sizing",
        "soft-module-sizing",
        "Soft module aspect sizing",
        "Soft module A keeps area six but may reshape between aspect one half and two. Reshape three by two into two by three, then pack legally—still area six.",
        "Open soft-module-sizing. Show hard three-by-two, then Reshape A to two by three. Confirm area six and legality true on the soft packing.",
        "Implement resize_soft that preserves area, then pack. Assert soft A ends at two by three with area six and a legal outline fit.",
        "Changing area when reshaping; ignoring aspect bounds; leaving hard modules soft by mistake.",
        "Accept a legal soft packing with A at two by three. Next: fix macro D at the origin.",
        [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "Module A is soft on the starter instance.",
                "answer": True,
                "explain": "Only A has soft: true.",
            },
            {
                "id": "q2",
                "type": "multiple_choice",
                "prompt": "After reshape, soft A size is…",
                "choices": ["3×2", "2×3", "4×2", "1×6"],
                "answer": 1,
                "explain": "Teaching reshape keeps area 6 as 2×3.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "Reshaped A still has area 6.",
                "answer": True,
                "explain": "2×3 = 6.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": "The soft packing remains legal inside 10×8.",
                "answer": True,
                "explain": "SOFT_A_PACK is a legal golden.",
            },
        ],
    ),
    (
        "module03-05-macro-placement",
        "macro-placement",
        "Hard macro / fixed-block placement",
        "Macros are hard fixed rectangles. In macro mode, D is pinned at zero comma zero with macro true, size three by one. A stacks above; B, C, and E pack to the right—still legal.",
        "Open macro-placement. Compare free golden D at zero comma two with Place macros: D at zero comma zero. Confirm legality and the macro flag.",
        "Fix D, pack the rest, assert D at (0,0), D.macro true, and is_legal_packing true. Note the free golden differs.",
        "Moving macros after fixing them; shrinking macro size; allowing overlaps against the fixed block.",
        "Ship the legal macro packing. Next: hierarchical AB left and CDE right at offset five.",
        [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "In macro mode, D is fixed at…",
                "choices": ["(0,2)", "(0,0)", "(3,0)", "(5,0)"],
                "answer": 1,
                "explain": "MACRO_PACK pins D at the origin.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "D.macro is true in the macro packing.",
                "answer": True,
                "explain": "Hard macro flag.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "Macro packing stays legal inside 10×8.",
                "answer": True,
                "explain": "Fixed D plus packed neighbors fit.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": "Free golden D sits at the same coordinates as macro D.",
                "answer": False,
                "explain": "Free D is at (0,2); macro D at (0,0).",
            },
        ],
    ),
    (
        "module04-01-hierarchical-floorplan",
        "hierarchical-floorplan",
        "Hierarchical floorplanning",
        "Hierarchy packs cluster AB on the left and cluster CDE on the right with x offset five. Local pack, then place clusters—legal overall with clusters separated in x.",
        "Open hierarchical-floorplan and Pack hierarchy. Confirm A and B have x less than five, C D E have x at least five, and legality true.",
        "Implement pack_hierarchical. Assert leftMax x+w is at most rightMin x, five modules present, and legality true.",
        "Overlapping cluster bounding boxes; forgetting the offset; applying different legality rules at each level.",
        "Accept the AB | CDE packing. Next: assign pins P0 through P3 on all four outline sides.",
        [
            {
                "id": "q1",
                "type": "true_false",
                "prompt": "In the golden hierarchy, A is on the left cluster (x < 5).",
                "answer": True,
                "explain": "AB packs left of the cut.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "C, D, and E are offset so x ≥ 5.",
                "answer": True,
                "explain": "Right cluster origin at x=5.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "The hierarchical packing is legal.",
                "answer": True,
                "explain": "Clusters do not overlap; outline fits.",
            },
            {
                "id": "q4",
                "type": "multiple_choice",
                "prompt": "Teaching hierarchy uses how many top-level clusters?",
                "choices": ["1", "2", "5", "10"],
                "answer": 1,
                "explain": "AB and CDE.",
            },
        ],
    ),
    (
        "module04-03-pin-assignment",
        "pin-assignment",
        "Boundary pin / I/O assignment",
        "Pins sit on outline edges. Golden assignment places P0 left, P1 bottom, P2 right, P3 top—four sides covered so pinsValid is true. An empty list is invalid.",
        "Open pin-assignment. Assign golden pins, confirm four sides and valid true. Clear pins and watch validity fail.",
        "Implement pinsValid requiring all four sides and in-range offsets. Assert golden pins pass and the empty list fails.",
        "Putting pins inside modules; offsets past edge length; claiming validity with only two sides covered.",
        "Ship a valid four-side assignment. Offline compare is next; then the wrap points to learn_placement.",
        [
            {
                "id": "q1",
                "type": "multiple_choice",
                "prompt": "Golden pin P0 is on which side?",
                "choices": ["top", "left", "right", "bottom"],
                "answer": 1,
                "explain": "P0 side=left.",
            },
            {
                "id": "q2",
                "type": "true_false",
                "prompt": "Golden pins cover all four outline sides.",
                "answer": True,
                "explain": "left, bottom, right, top.",
            },
            {
                "id": "q3",
                "type": "true_false",
                "prompt": "An empty pin list is valid.",
                "answer": False,
                "explain": "Need four distinct sides.",
            },
            {
                "id": "q4",
                "type": "true_false",
                "prompt": "pinsValid is true for the golden four-pin set.",
                "answer": True,
                "explain": "Offsets in range and four sides present.",
            },
        ],
    ),
]


def transcript(mid: str, lab: str, title: str, opener: str, browser: str, implement: str, pitfall: str, your_turn: str) -> str:
    return f"""# {title}

**Module id:** {mid}
**Lab:** {lab}
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — {title}

{opener}

<!-- algorithm-walkthrough -->
## Slide 2 — (walkthrough pending)
<!-- /algorithm-walkthrough -->

## Slide 3 — Browser lab track

{browser}

## Slide 4 — Implement track

{implement}

## Slide 5 — Pitfalls

{pitfall}

## Slide 6 — Your turn

{your_turn}
"""


def main() -> None:
    for mid, lab, title, opener, browser, implement, pitfall, your_turn, quiz_items in LABS:
        base = ROOT / mid
        (base / "transcript.md").write_text(
            transcript(mid, lab, title, opener, browser, implement, pitfall, your_turn),
            encoding="utf-8",
        )
        quiz = {
            "module": mid,
            "title": f"{title.split('/')[0].strip()} check",
            "passing_score": 0.67,
            "items": quiz_items,
        }
        (base / "quiz.json").write_text(json.dumps(quiz, indent=2) + "\n", encoding="utf-8")
        print("deepened", mid)
    print("done", len(LABS))


if __name__ == "__main__":
    main()
