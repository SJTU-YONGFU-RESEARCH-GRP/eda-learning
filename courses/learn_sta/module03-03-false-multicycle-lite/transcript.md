# False and multicycle paths (engine view)

**Module id:** module03-03-false-multicycle-lite
**Lab:** false-multicycle-lite
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — False and multicycle paths (engine view)

Exceptions change which arcs propagate and how large the required window is. You consume them as engine data—not as a full SDC course. You will compare normal slack 6.8, multicycle×2 slack 16.8, and a false-path that cuts the bridge net.

## Slide 2 — Goldens to remember

Multicycle cycles=2 → R(out)=20, slack=16.8. False-path disables u1/Y→u2/A so A(u2/A) falls to 0 in the lite model. Keep these numbers handy—the browser challenges and Track A tests use the same instance.


## Slide 3 — Pseudocode

Exceptions enter the same propagate sketch. False paths omit disabled arcs. Multicycle setup multiplies the sink required by setup cycles times the period.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Default slack at out is six point eight. Two cycles raises required to twenty and slack to sixteen point eight. Disabling u1/Y to u2/A removes that timing path.

```text
INPUT: G, disable set S, setup_cycles
OUTPUT: setup slack at sink
A ← prop_arrival using arcs ∉ S
R ← prop_required; R[sink]←period×cycles
slack ← R[sink] − A[sink]
GOLDEN default: slack(out)=6.8
cycles=2 → R[out]=20, slack=16.8
disable u1/Y→u2/A breaks that path
```


<!-- algorithm-walkthrough -->

## Slide 5 — Normal single-cycle setup

![Normal single-cycle setup](assets/steps/01-normal-check.png)

Without exceptions, required at out is one period (10) and setup slack is 6.8. That is the baseline the exceptions will change.

## Slide 6 — Multicycle widens the required window

![Multicycle widens the required window](assets/steps/02-multicycle.png)

A setup multicycle of 2 means required = 2 × period = 20. Slack becomes 16.8. The graph did not change—only the endpoint budget did.

## Slide 7 — False path disables an arc

![False path disables an arc](assets/steps/03-false-path.png)

Marking the bridge net u1/Y→u2/A as false removes it from propagation. Downstream pins no longer see the real wavefront—u2/A falls back to 0 in this lite engine.

## Slide 8 — Exceptions are engine data

![Exceptions are engine data](assets/steps/04-engine-data.png)

SDC authoring lives in learn_sdc. Here you only consume false-path and multicycle as flags the timer reads—same idea as production engines.

## Slide 9 — Always recheck after exceptions

![Always recheck after exceptions](assets/steps/05-recheck.png)

Apply exceptions, then recompute tags and slack. Never keep a stale 6.8 after a multicycle or false-path change.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab, open **false-multicycle-lite**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 11 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 12 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 13 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
