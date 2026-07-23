# Slack, setup, and hold

**Module id:** module02-01-slack-setup-hold
**Lab:** slack-setup-hold
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Slack, setup, and hold

Slack turns tags into a pass or fail. Setup slack is required minus arrival; hold uses a different required. You will get setup slack six point eight and hold slack three point two at out on the lite model.

## Slide 2 — Goldens to remember

Setup: R−A = 10−3.2 = 6.8. Hold lite: A−0 = 3.2. Positive means the check passes. Keep these numbers handy—the browser challenges and Track A tests use the same instance.

<!-- algorithm-walkthrough -->
<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

In the browser lab, open **slack-setup-hold**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 9 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 10 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 11 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
