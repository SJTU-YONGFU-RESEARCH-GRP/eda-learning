# Slack, setup, and hold

**Module id:** module02-01-slack-setup-hold
**Lab:** slack-setup-hold
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Slack, setup, and hold

Slack turns tags into a pass or fail. Setup slack is required minus arrival; hold uses a different required. You will get setup slack six point eight and hold slack three point two at out on the lite model.

## Slide 2 — Goldens to remember

Setup: R−A = 10−3.2 = 6.8. Hold lite: A−0 = 3.2. Positive means the check passes. Keep these numbers handy—the browser challenges and Track A tests use the same instance.


## Slide 3 — Pseudocode

Slack pseudocode is arithmetic on tags you already have. Setup slack is required minus arrival. Hold lite uses required hold zero at the sink and arrival minus that required.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

On the tiny chain with period ten, setup slack at out is six point eight and hold slack is three point two. Shrink the period to three and setup fails first.

```text
INPUT: A[], R_setup[], R_hold[] (lite)
OUTPUT: setup_slack, hold_slack, meet?
setup_slack(p) ← R_setup[p] − A[p]
hold_slack(p)  ← A[p] − R_hold[p]
R_hold[sink] ← 0 in this lite model
meet_setup if setup_slack(sink)≥0
meet_hold  if hold_slack(sink)≥0
GOLDEN: setup(out)=6.8; hold(out)=3.2
```


<!-- algorithm-walkthrough -->

## Slide 5 — Setup slack is required minus arrival

![Setup slack is required minus arrival](assets/steps/01-setup-formula.png)

At the endpoint out, setup slack equals R − A. With R=10 and A=3.2, slack is 6.8—positive means the path meets the single-cycle check.

## Slide 6 — Hold slack uses a different required

![Hold slack uses a different required](assets/steps/02-hold-formula.png)

For this lite hold model, required at out is 0 on the same edge. Hold slack is A − R_hold = 3.2 − 0 = 3.2.

## Slide 7 — The sign tells you pass or fail

![The sign tells you pass or fail](assets/steps/03-sign-matters.png)

Negative setup slack means the path is too slow for the period. Negative hold means data changes too soon. Read the sign before you chase the path.

## Slide 8 — Report slack at endpoints first

![Report slack at endpoints first](assets/steps/04-endpoint-habit.png)

Engineers scan worst negative slack at endpoints, then open the path. On this toy netlist there is one sink—out—so both checks live there.

## Slide 9 — Period changes setup, not hold lite

![Period changes setup, not hold lite](assets/steps/05-period-knob.png)

If the period were tighter, setup required would drop and setup slack would shrink. Hold in this lite model stays tied to arrival versus zero.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab, open **slack-setup-hold**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 11 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 12 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 13 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
