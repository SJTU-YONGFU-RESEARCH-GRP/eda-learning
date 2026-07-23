# Incremental timing update

**Module id:** module03-01-incremental-update
**Lab:** incremental-update
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Incremental timing update

Real timers cannot rebuild the chip after every buffer insert. They invalidate a cone and recompute. You will bump u1’s cell delay from 1.2 to 2.0 and see A(out) move from 3.2 to 4.0 with setup slack 6.0.

## Slide 2 — Goldens to remember

Invalidated cone: u1/Y, u2/A, u2/Y, out. Clean: in, u1/A. ΔA(out)=+0.8. Keep these numbers handy—the browser challenges and Track A tests use the same instance.


## Slide 3 — Pseudocode

Incremental STA is cone invalidation plus selective recompute. After an arc delay edit, BFS the fanout from the arc’s sink, clear those arrivals, then refill in topo order.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Bump the u1 cell delay from one point two to two. The golden cone is u1/Y, u2/A, u2/Y, and out. Arrival at out becomes four and setup slack six.

```text
INPUT: G, edit u→v delay:=d', A_old
OUTPUT: A_new, invalidated cone
set delay(u,v)←d'
inv ← BFS successors from v (incl. v)
delete A[p] for p in inv
recompute A in topo order for missing pins
GOLDEN edit 1.2→2.0 on u1 cell:
  inv={u1/Y,u2/A,u2/Y,out}; A[out]=4.0
```


<!-- algorithm-walkthrough -->

## Slide 5 — Start from a full analysis

![Start from a full analysis](assets/steps/01-base-tags.png)

Base arrival at out is 3.2 with setup slack 6.8. Incremental update never starts from an empty graph—it starts from valid tags.

## Slide 6 — Edit one cell delay

![Edit one cell delay](assets/steps/02-local-edit.png)

Bump the u1 cell arc from 1.2 to 2.0. Only the fanout cone of u1/Y can change—everything upstream of the edit stays put.

## Slide 7 — Invalidate the fanout cone

![Invalidate the fanout cone](assets/steps/03-invalidate-cone.png)

Mark u1/Y, u2/A, u2/Y, and out dirty. Do not touch in or u1/A—their arrivals are still valid.

## Slide 8 — Recompute only the dirty pins

![Recompute only the dirty pins](assets/steps/04-recompute.png)

Replay topo order on dirty pins. Arrival at out becomes 4.0; setup slack drops to 6.0. Same answer as a full rebuild, less work.

## Slide 9 — Why timers insist on incremental

![Why timers insist on incremental](assets/steps/05-why-incremental.png)

Place, CTS, and ECO change tiny regions millions of times. Full-chip rebuilds every edit would not finish. Cone invalidate-and-repair is the habit.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab, open **incremental-update**. Load the starter, run the analysis once, and read the metrics panel. Orient yourself—challenge panel, canvas, Check—then mirror the same goldens in code.

## Slide 11 — Implement track

In the implement track, use `common/tiny_timing.json` with the helpers in `common/graph.py` and `common/propagate.py`. Run `python3 common/test_propagate.py` (and the timing-graph test) until the goldens print ok.

## Slide 12 — Pitfall

Do not mix setup and hold required maps. Do not propagate before the graph is levelized. After an edit or exception, recompute—stale tags lie.

## Slide 13 — Your turn

Finish the checklist on at least one track—preferably both. When your numbers match the goldens, take the quiz, then continue.
