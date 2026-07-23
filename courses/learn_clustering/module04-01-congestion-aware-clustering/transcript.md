# Congestion-aware clustering

**Module id:** module04-01-congestion-aware-clustering
**Lab:** congestion-aware-clustering
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Congestion-aware clustering

When bridge edges are congested, cutting them becomes expensive. You’ll watch FM under a congestion penalty and see how lambda reshapes the partition.

<!-- algorithm-walkthrough -->

## Slide 2 — Start from BAD_SEED

![Start from BAD_SEED](assets/steps/01-bad-seed.png)

Same cutsize-12 seed AE|BCD. Congestion map marks C–D=5 and C–E=4 — cheap wire cuts may be expensive for routing.

## Slide 3 — λ=0 → ordinary FM

![λ=0 → ordinary FM](assets/steps/02-lam0.png)

With λ=0, boosted weights equal original weights. FM recovers ABC|DE: plain=3 but penalty=9 because both congested bridges are cut.

## Slide 4 — Boost weights by λ·cong

![Boost weights by λ·cong](assets/steps/03-boost.png)

For λ=5, C–D and C–E become very expensive to cut. FM optimizes the boosted graph, then we report plain cut and congestion penalty separately.

## Slide 5 — λ=5 → pen 0, plain 5

![λ=5 → pen 0, plain 5](assets/steps/04-lam5.png)

Result AB|CDE: plain cut rises to 5, but congestion penalty drops to 0 — congested bridges stay internal.

## Slide 6 — Objective tradeoffs

![Objective tradeoffs](assets/steps/05-takeaway.png)

EDA flows rarely optimize cut alone. λ makes the congestion tax explicit so students see the Pareto move between wire and routing.

<!-- /algorithm-walkthrough -->

## Slide 7 — Browser lab track

In the browser lab, compare lambda zero with lambda five from the same bad seed. Watch the penalty drop to zero when the congested bridge is avoided.

## Slide 8 — Implement track

Run congestion-aware partition at lambda zero and five. Confirm plain cut three with penalty nine at lambda zero, and plain five with penalty zero at lambda five.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode congestion --seed ../module02-05-kernighan-lin/examples/seed_partition.json --congestion examples/congestion.json --lambda 5
```

## Slide 9 — Pitfalls to watch

Applying congestion only after FM misses the point—weights must change before moves. Huge lambda can ignore connectivity entirely.

## Slide 10 — Your turn

Match both lambda goldens, finish the checklist and quiz, then continue to timing-aware clustering.
