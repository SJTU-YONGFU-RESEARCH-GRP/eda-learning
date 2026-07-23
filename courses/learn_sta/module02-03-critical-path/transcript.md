# Critical path

**Module id:** module02-03-critical-path
**Lab:** critical-path
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Critical path

When slack is bad—or even when it is good—you still need the path. Trace from the worst endpoint through matching arrival tags. You will recover the golden path in → u1/A → u1/Y → u2/A → u2/Y → out.

## Slide 2 — Goldens to remember

Critical path has six pins. Path delay equals A(out)=3.2. Always match A(u)+d to A(v). Keep these numbers handy—the browser challenges and Track A tests use the same instance.


## Slide 3 — Pseudocode

Critical path pseudocode walks backward from the sink. At each pin pick a predecessor arc whose arrival plus delay exactly rebuilds the pin’s arrival, breaking ties toward larger arrival.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

The golden path is six pins from in through both cells to out. Path delay must equal arrival at out—three point two on this instance.

```text
INPUT: G, A[], sink
OUTPUT: pin path (source→…→sink)
path←[sink]; cur←sink
while cur has preds:
  pick u→cur with A[u]+delay == A[cur]
  (tie-break: largest A[u])
  prepend u; cur←u
return path
GOLDEN: in→u1/A→u1/Y→u2/A→u2/Y→out
```


<!-- algorithm-walkthrough -->

## Slide 5 — Start from the worst endpoint

![Start from the worst endpoint](assets/steps/01-worst-sink.png)

Critical-path traceback begins at the endpoint with the worst setup slack. Here that is out with slack 6.8—still the only sink.

## Slide 6 — Step to the matching predecessor

![Step to the matching predecessor](assets/steps/02-match-pred.png)

At each pin, choose a predecessor u where A(u) + delay equals A(v). That arc is on the critical path.

## Slide 7 — The full golden path

![The full golden path](assets/steps/03-full-path.png)

The complete critical path is in → u1/A → u1/Y → u2/A → u2/Y → out. Arrival at out equals the sum of arc delays along this path: 3.2.

## Slide 8 — Fix the path, not a random gate

![Fix the path, not a random gate](assets/steps/04-why-it-matters.png)

Optimization and ECO work chase critical paths. Tag matching keeps you honest when reconvergence exists—on this chain there is only one route.

## Slide 9 — Slack and path travel together

![Slack and path travel together](assets/steps/05-slack-path.png)

Reports pair worst slack with its path. Next labs edit delays and exceptions—always re-trace after the tags change.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab, open **critical-path**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 11 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 12 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 13 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
