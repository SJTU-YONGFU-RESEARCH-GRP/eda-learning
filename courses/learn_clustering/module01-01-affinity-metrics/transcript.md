# Affinity metrics

**Module id:** module01-01-affinity-metrics
**Lab:** affinity-metrics
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Affinity metrics

Before you merge cells or coarsen a netlist, you need a score that says these two should stay together. That score is affinity. In this module you’ll compare plain edge weight with shared-neighbor scoring on the same tiny graph—and watch who wants to merge first.

<!-- algorithm-walkthrough -->

## Slide 2 — Start with a tiny weighted graph

![Start with a tiny weighted graph](assets/steps/01-raw-graph.png)

Five cells A through E with edge weights. Heavy edges A–B and D–E both weigh five; the bridge through C is weaker. Affinity will decide which pairs want to cluster first.

## Slide 3 — Edge-weight affinity ranks pairs

![Edge-weight affinity ranks pairs](assets/steps/02-edge-rank.png)

Pure edge-weight affinity just sorts existing edges. A–B and D–E tie at five; tie-break puts A–B first. That ranking is the simplest merge priority.

## Slide 4 — Shared neighbors boost A–B

![Shared neighbors boost A–B](assets/steps/03-shared-idea.png)

A and B already share edge weight five. They also share neighbor C. Shared-neighbor affinity adds the minimum of those spokes—one—so A–B rises to six.

## Slide 5 — Shared ranking reshuffles the list

![Shared ranking reshuffles the list](assets/steps/04-shared-rank.png)

Under shared-neighbor scoring, A–B and D–E lead at six. Weak edge A–C jumps to five because of B. Non-edges like B–D can appear from shared support alone.

## Slide 6 — Why affinity matters in EDA

![Why affinity matters in EDA](assets/steps/05-takeaway.png)

Affinity is the objective’s local preference: which cells belong together before global constraints. Bad affinity means bad merges, and harder refinement later.

<!-- /algorithm-walkthrough -->

## Slide 7 — Browser lab track

In the browser lab track, open the affinity metrics lab, load the starter example, and switch between the two ranking buttons. Clear the ten challenges when you’re ready—start with the top edge-weight pair, then the shared-neighbor climb for A–C.

## Slide 8 — Implement track

In the implement track, load the tiny weighted graph and print both rankings. Match the goldens: edge weight tops at five for A–B; shared-neighbor lifts A–B to six. Run the unit tests from the course common folder so your scores stay honest.

```bash
# pwd — print working directory (where am I?)
pwd

# ls examples — confirm the starter graph is here
ls examples

# print both affinity rankings
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode affinity
```

## Slide 9 — Pitfalls to watch

Watch for mixing directed and undirected assumptions, or double-counting a neighbor. Don’t invent pairs with zero connection unless your API says so. And don’t let a later merge engine silently use a different affinity than the one you documented.

## Slide 10 — Your turn

Finish the checklist for at least one track. Match both golden tables, then explain why A–C climbs under shared-neighbor scoring. Take the short quiz, then continue to greedy pair merge—where these scores become the merge policy.
