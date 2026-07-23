# Arrival and required times

**Module id:** module01-03-arrival-required
**Lab:** arrival-required
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Arrival and required times

Once the graph is levelized, you propagate tags. Arrival moves forward from sources; required moves backward from sinks. You will compute A(out)=3.2 and R(out)=10 on the starter chain with period ten.

## Slide 2 — Goldens to remember

Forward: A(in)=0, A(u1/Y)=1.2, A(out)=3.2. Backward setup: R(out)=10, R(in)=6.8. Keep these numbers handy—the browser challenges and Track A tests use the same instance.


## Slide 3 — Pseudocode

Arrival and required need two written passes. Forward topo takes a max over predecessors for arrival. Reverse topo takes a min over successors for setup required from the period at sinks.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Goldens on the chain: arrival at out is three point two, required at out is ten, and required at in is six point eight. Arrival is latest; required is earliest.

```text
INPUT: DAG G, period, arrival seeds
OUTPUT: A[], R_setup[]
for p in topo(G):
  A[p]← max over u→p of A[u]+delay   (sources: seed/0)
for sinks: R[p]←period×cycles
for p in reverse_topo:
  R[p]← min over p→v of R[v]−delay
GOLDEN: A[out]=3.2; R[out]=10; R[in]=6.8
```


<!-- algorithm-walkthrough -->

## Slide 5 — Seed arrival at the source

![Seed arrival at the source](assets/steps/01-seed-arrival.png)

Set arrival at in to zero for the launch edge. Every other pin waits for its predecessors.

## Slide 6 — Propagate arrival forward

![Propagate arrival forward](assets/steps/02-forward-wave.png)

For each pin in topo order, arrival is the max over predecessors of A(pred) + delay. At out the wavefront reaches 3.2.

## Slide 7 — Seed required at the sink

![Seed required at the sink](assets/steps/03-seed-required.png)

For a single-cycle setup check, required at out equals the clock period—here 10.

## Slide 8 — Propagate required backward

![Propagate required backward](assets/steps/04-backward-wave.png)

Walk reverse topo order. Required at a pin is the min over successors of R(succ) − delay. At in, required becomes 6.8.

## Slide 9 — Keep both tags on every pin

![Keep both tags on every pin](assets/steps/05-both-tags.png)

Arrival and required live together. Slack at a pin is R − A for setup. Next labs turn those tags into slack and a critical path.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab, open **arrival-required**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 11 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 12 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 13 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
