# Size-constrained agglomerative clustering

**Module id:** module01-05-size-constrained-agglomerative
**Lab:** size-constrained-agglomerative
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Size-constrained agglomerative clustering

Size caps change which merges are legal. You’ll watch greedy agglomeration with capacity two on the tiny graph—and see why A–B–C can no longer form.

<!-- algorithm-walkthrough -->

## Slide 2 — Capacity blocks illegal merges

![Capacity blocks illegal merges](assets/steps/01-capacity-rule.png)

Same greedy heaviest-edge merge, but refuse any pair whose sizes sum above capacity. With capacity=2 on unit nodes, size-3 clusters are illegal.

## Slide 3 — Merge A–B (still legal)

![Merge A–B (still legal)](assets/steps/02-merge-ab.png)

Heaviest edge A–B at weight 5 merges first. Combined size is 2 — exactly at capacity. C cannot join next.

## Slide 4 — Merge D–E; C stays alone

![Merge D–E; C stays alone](assets/steps/03-merge-de.png)

D–E merges at weight 5. Absorbing C into AB would create size 3 and is rejected, so we stop with three clusters even though target K=2.

## Slide 5 — Result: cutsize 8

![Result: cutsize 8](assets/steps/04-cut-8.png)

Cut edges include A–C, B–C, C–D, C–E. Capacity cost is +5 versus the unconstrained cut of 3.

## Slide 6 — Why capacity matters in EDA

![Why capacity matters in EDA](assets/steps/05-takeaway.png)

Floorplanning and clustering often cap cluster area. Teaching point: constraints change the greedy path — you may never reach the unconstrained communities.

<!-- /algorithm-walkthrough -->

## Slide 7 — Browser lab track

In the browser lab, load the starter with capacity two, then compare presets against unconstrained K equals two. Clear the challenges for blocked size-three clusters and the AB|C|DE parts.

## Slide 8 — Implement track

Run greedy merge with capacity two and confirm cutsize eight with parts AB|C|DE. Then lift capacity to three and recover the unconstrained ABC|DE cutsize three.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --k 2 --capacity 2
```

## Slide 9 — Pitfalls to watch

Forgetting to check capacity before contracting is the classic bug. Also watch stale affinities after a blocked merge candidate is skipped.

## Slide 10 — Your turn

Match the capacity-two golden, finish the checklist and quiz, then continue to label propagation.
