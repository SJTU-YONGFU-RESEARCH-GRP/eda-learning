# Fiduccia–Mattheyses refinement

**Module id:** module02-07-fiduccia-mattheyses
**Lab:** fiduccia-mattheyses
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Fiduccia–Mattheyses refinement

FM refines a bipartition with single-vertex moves, locking, and rollback—cousin to Kernighan–Lin, but one cell at a time. On the same bad seed that starts at cutsize twelve, FM reaches cutsize three.

<!-- algorithm-walkthrough -->

## Slide 2 — Same bad seed, different move set

![Same bad seed, different move set](assets/steps/01-bad-seed.png)

FM starts from the same cutsize-twelve seed, but moves one vertex at a time instead of swapping a pair. That suits hypergraph and cell-move implementations.

## Slide 3 — Move 1: flip D (gain 3)

![Move 1: flip D (gain 3)](assets/steps/02-move-d.png)

Highest legal move sends D to the other side with gain three. Partial progress: D joins E’s side early. Lock D and update neighbor gains.

## Slide 4 — Move 2: flip A (gain 6)

![Move 2: flip A (gain 6)](assets/steps/03-move-a.png)

Next, A flips with gain six. Cumulative gain is three plus six—nine—the same total improvement KL found with one swap. Best k equals two keeps both moves.

## Slide 5 — Final ABC|DE, cutsize 3

![Final ABC|DE, cutsize 3](assets/steps/04-final.png)

FM lands on the same refined bipartition as KL. Move style differs; destination quality matches on this instance. Cutsize is three.

## Slide 6 — Pass 1 confirms local optimum

![Pass 1 confirms local optimum](assets/steps/05-pass1-stop.png)

A second FM pass finds no improving move prefix. Stop. In real tools, FM often runs inside multilevel V-cycles with tighter balance and hyperedges.

<!-- /algorithm-walkthrough -->

## Slide 7 — Browser lab track

In the browser lab, show the seed, run FM, and compare the move list with KL’s single swap. Clear the challenges for twelve-to-three and the D-then-A prefix.

## Slide 8 — Implement track

Run FM on the shared bad seed. Confirm moves D then A in the accepted prefix, and cut twelve to three. Re-implement selection and rollback until tests pass.

```bash
# FM refinement on the shared bad seed
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode fm --seed ../module02-05-kernighan-lin/examples/seed_partition.json
```

## Slide 9 — Pitfalls to watch

Skipping rollback keeps a worse locked state. Ignoring balance lets one side empty. Stale gains after a move pick the wrong cell next.

## Slide 10 — Your turn

Reproduce twelve to three, finish the checklist and quiz, then continue to multilevel clustering.
