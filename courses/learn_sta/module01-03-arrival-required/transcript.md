# Arrival and required times

**Module id:** module01-03-arrival-required
**Lab:** arrival-required
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Arrival and required times

Once the graph is levelized, you propagate tags. Arrival moves forward from sources; required moves backward from sinks. You will compute A(out)=3.2 and R(out)=10 on the starter chain with period ten.

## Slide 2 — Goldens to remember

Forward: A(in)=0, A(u1/Y)=1.2, A(out)=3.2. Backward setup: R(out)=10, R(in)=6.8. Keep these numbers handy—the browser challenges and Track A tests use the same instance.

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

In the browser lab, open **arrival-required**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 9 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 10 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 11 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
