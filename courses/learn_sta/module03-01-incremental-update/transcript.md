# Incremental timing update

**Module id:** module03-01-incremental-update
**Lab:** incremental-update
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Incremental timing update

Real timers cannot rebuild the chip after every buffer insert. They invalidate a cone and recompute. You will bump u1’s cell delay from 1.2 to 2.0 and see A(out) move from 3.2 to 4.0 with setup slack 6.0.

## Slide 2 — Goldens to remember

Invalidated cone: u1/Y, u2/A, u2/Y, out. Clean: in, u1/A. ΔA(out)=+0.8. Keep these numbers handy—the browser challenges and Track A tests use the same instance.

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

In the browser lab, open **incremental-update**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 9 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 10 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 11 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
