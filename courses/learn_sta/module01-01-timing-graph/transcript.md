# Timing graph

**Module id:** module01-01-timing-graph
**Lab:** timing-graph
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Timing graph

Static timing starts with a directed timing graph. On our tiny chain, six pins and five arcs carry you from in through two cells to out. You will levelize the graph, name sources and sinks, and prove that a back-edge out to in makes levelize fail.

## Slide 2 — Goldens to remember

Goldens: six pins, five arcs, levels zero through five, path delay three point two. A cycle returns no levels. Keep these numbers handy—the browser challenges and Track A tests use the same instance.

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

In the browser lab, open **timing-graph**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 9 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 10 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 11 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
