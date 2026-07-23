# False and multicycle paths (engine view)

**Module id:** module03-03-false-multicycle-lite
**Lab:** false-multicycle-lite
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — False and multicycle paths (engine view)

Exceptions change which arcs propagate and how large the required window is. You consume them as engine data—not as a full SDC course. You will compare normal slack 6.8, multicycle×2 slack 16.8, and a false-path that cuts the bridge net.

## Slide 2 — Goldens to remember

Multicycle cycles=2 → R(out)=20, slack=16.8. False-path disables u1/Y→u2/A so A(u2/A) falls to 0 in the lite model. Keep these numbers handy—the browser challenges and Track A tests use the same instance.

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

In the browser lab, open **false-multicycle-lite**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 9 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 10 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 11 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
