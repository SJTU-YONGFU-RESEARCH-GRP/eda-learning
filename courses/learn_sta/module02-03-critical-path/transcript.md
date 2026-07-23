# Critical path

**Module id:** module02-03-critical-path
**Lab:** critical-path
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Critical path

When slack is bad—or even when it is good—you still need the path. Trace from the worst endpoint through matching arrival tags. You will recover the golden path in → u1/A → u1/Y → u2/A → u2/Y → out.

## Slide 2 — Goldens to remember

Critical path has six pins. Path delay equals A(out)=3.2. Always match A(u)+d to A(v). Keep these numbers handy—the browser challenges and Track A tests use the same instance.

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

In the browser lab, open **critical-path**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 9 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 10 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 11 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
