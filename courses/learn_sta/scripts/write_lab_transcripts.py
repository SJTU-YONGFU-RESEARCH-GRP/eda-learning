#!/usr/bin/env python3
"""Write algorithm-specific transcripts + quizzes for learn_sta labs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LABS = {
    "module01-01-timing-graph": {
        "title": "Timing graph",
        "lab": "timing-graph",
        "opener": "Static timing starts with a directed timing graph. On our tiny chain, six pins and five arcs carry you from in through two cells to out.",
        "promise": "You will levelize the graph, name sources and sinks, and prove that a back-edge out to in makes levelize fail.",
        "goldens": "Goldens: six pins, five arcs, levels zero through five, path delay three point two. A cycle returns no levels.",
        "quiz": [
            {"id": "q1", "type": "multiple_choice", "prompt": "Max level of out on the starter chain is…", "choices": ["3", "5", "6", "0"], "answer": 1, "explain": "out is L5."},
            {"id": "q2", "type": "true_false", "prompt": "A back-edge out→in still levelizes successfully.", "answer": False, "explain": "Cycles make Kahn stall."},
            {"id": "q3", "type": "multiple_choice", "prompt": "Path delay sum on the starter is…", "choices": ["2.7", "3.2", "10", "1.2"], "answer": 1, "explain": "0+1.2+0.3+1.5+0.2=3.2."},
        ],
    },
    "module01-03-arrival-required": {
        "title": "Arrival and required times",
        "lab": "arrival-required",
        "opener": "Once the graph is levelized, you propagate tags. Arrival moves forward from sources; required moves backward from sinks.",
        "promise": "You will compute A(out)=3.2 and R(out)=10 on the starter chain with period ten.",
        "goldens": "Forward: A(in)=0, A(u1/Y)=1.2, A(out)=3.2. Backward setup: R(out)=10, R(in)=6.8.",
        "quiz": [
            {"id": "q1", "type": "multiple_choice", "prompt": "Arrival at out on the starter is…", "choices": ["10", "3.2", "6.8", "0"], "answer": 1, "explain": "Path delay 3.2."},
            {"id": "q2", "type": "true_false", "prompt": "Required for single-cycle setup at out equals the clock period (10).", "answer": True, "explain": "R(out)=period."},
            {"id": "q3", "type": "multiple_choice", "prompt": "Required at in after backward prop is…", "choices": ["0", "3.2", "6.8", "10"], "answer": 2, "explain": "R(in)=6.8."},
        ],
    },
    "module02-01-slack-setup-hold": {
        "title": "Slack, setup, and hold",
        "lab": "slack-setup-hold",
        "opener": "Slack turns tags into a pass or fail. Setup slack is required minus arrival; hold uses a different required.",
        "promise": "You will get setup slack six point eight and hold slack three point two at out on the lite model.",
        "goldens": "Setup: R−A = 10−3.2 = 6.8. Hold lite: A−0 = 3.2. Positive means the check passes.",
        "quiz": [
            {"id": "q1", "type": "multiple_choice", "prompt": "Setup slack at out is…", "choices": ["3.2", "6.8", "10", "−3.2"], "answer": 1, "explain": "10−3.2=6.8."},
            {"id": "q2", "type": "true_false", "prompt": "Hold slack uses the same required map as setup.", "answer": False, "explain": "Hold required differs."},
            {"id": "q3", "type": "multiple_choice", "prompt": "Hold slack at out (lite) is…", "choices": ["6.8", "0", "3.2", "10"], "answer": 2, "explain": "3.2−0=3.2."},
        ],
    },
    "module02-03-critical-path": {
        "title": "Critical path",
        "lab": "critical-path",
        "opener": "When slack is bad—or even when it is good—you still need the path. Trace from the worst endpoint through matching arrival tags.",
        "promise": "You will recover the golden path in → u1/A → u1/Y → u2/A → u2/Y → out.",
        "goldens": "Critical path has six pins. Path delay equals A(out)=3.2. Always match A(u)+d to A(v).",
        "quiz": [
            {"id": "q1", "type": "true_false", "prompt": "Critical-path traceback starts at a source pin.", "answer": False, "explain": "Start at the worst sink."},
            {"id": "q2", "type": "multiple_choice", "prompt": "Golden critical path length (pins) is…", "choices": ["4", "5", "6", "7"], "answer": 2, "explain": "Six pins."},
            {"id": "q3", "type": "multiple_choice", "prompt": "Path delay equals…", "choices": ["A(out)", "R(out)", "period", "hold slack"], "answer": 0, "explain": "A(out)=3.2."},
        ],
    },
    "module03-01-incremental-update": {
        "title": "Incremental timing update",
        "lab": "incremental-update",
        "opener": "Real timers cannot rebuild the chip after every buffer insert. They invalidate a cone and recompute.",
        "promise": "You will bump u1’s cell delay from 1.2 to 2.0 and see A(out) move from 3.2 to 4.0 with setup slack 6.0.",
        "goldens": "Invalidated cone: u1/Y, u2/A, u2/Y, out. Clean: in, u1/A. ΔA(out)=+0.8.",
        "quiz": [
            {"id": "q1", "type": "multiple_choice", "prompt": "After u1 delay 1.2→2.0, A(out) is…", "choices": ["3.2", "4.0", "6.0", "2.0"], "answer": 1, "explain": "Arrival becomes 4.0."},
            {"id": "q2", "type": "true_false", "prompt": "Incremental update must invalidate the source pin in.", "answer": False, "explain": "Upstream of the edit stays clean."},
            {"id": "q3", "type": "multiple_choice", "prompt": "Setup slack after the edit is…", "choices": ["6.8", "6.0", "4.0", "3.2"], "answer": 1, "explain": "10−4.0=6.0."},
        ],
    },
    "module03-03-false-multicycle-lite": {
        "title": "False and multicycle paths (engine view)",
        "lab": "false-multicycle-lite",
        "opener": "Exceptions change which arcs propagate and how large the required window is. You consume them as engine data—not as a full SDC course.",
        "promise": "You will compare normal slack 6.8, multicycle×2 slack 16.8, and a false-path that cuts the bridge net.",
        "goldens": "Multicycle cycles=2 → R(out)=20, slack=16.8. False-path disables u1/Y→u2/A so A(u2/A) falls to 0 in the lite model.",
        "quiz": [
            {"id": "q1", "type": "multiple_choice", "prompt": "Multicycle setup×2 required at out is…", "choices": ["10", "20", "16.8", "3.2"], "answer": 1, "explain": "2×period=20."},
            {"id": "q2", "type": "true_false", "prompt": "A false-path exception removes an arc from propagation.", "answer": True, "explain": "Disabled arcs are skipped."},
            {"id": "q3", "type": "multiple_choice", "prompt": "Normal setup slack before exceptions is…", "choices": ["16.8", "6.8", "3.2", "0"], "answer": 1, "explain": "Baseline 6.8."},
        ],
    },
}


def lab_transcript(mid: str, meta: dict) -> str:
    return f"""# {meta['title']}

**Module id:** {mid}
**Lab:** {meta['lab']}
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — {meta['title']}

{meta['opener']} {meta['promise']}

## Slide 2 — Goldens to remember

{meta['goldens']} Keep these numbers handy—the browser challenges and Track A tests use the same instance.

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

In the browser lab, open **{meta['lab']}**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 9 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 10 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 11 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
"""


def write_quiz(mid: str, meta: dict) -> None:
    payload = {
        "id": mid,
        "title": f"{meta['title']} check",
        "items": meta["quiz"],
    }
    (ROOT / mid / "quiz.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    for mid, meta in LABS.items():
        path = ROOT / mid / "transcript.md"
        path.write_text(lab_transcript(mid, meta), encoding="utf-8")
        write_quiz(mid, meta)
        # mark README shipped-ish lines later via MODULES
        print("ok", mid)


if __name__ == "__main__":
    main()
