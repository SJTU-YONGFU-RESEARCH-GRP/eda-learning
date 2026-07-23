# Timing-aware clustering

**Module id:** module04-03-timing-aware-clustering
**Lab:** timing-aware-clustering
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Timing-aware clustering

Critical nets should stay uncut. You’ll watch FM on criticality-weighted edges and land on cutsize three with weighted cut seven—protecting the A–B–C path.

<!-- algorithm-walkthrough -->

## Slide 2 — Mark critical edges

![Mark critical edges](assets/steps/01-criticality.png)

Criticality map emphasizes path A–B–C–D: A–B=5, B–C=4, C–D=3. Cutting critical edges hurts timing more than raw wire weight suggests.

## Slide 3 — Reweight then refine

![Reweight then refine](assets/steps/02-weight.png)

Multiply each edge by its criticality (default 1 if missing). FM now strongly prefers keeping A–B and B–C internal.

## Slide 4 — Land on ABC|DE

![Land on ABC|DE](assets/steps/03-result.png)

Timing-aware FM reaches ABC|DE. Plain cutsize is 3; weighted cut (criticality-scaled) is 7.

## Slide 5 — Critical edges uncut

![Critical edges uncut](assets/steps/04-protect.png)

A–B and B–C stay inside ABC. The cut uses less critical bridges C–D and C–E — acceptable plain cut, better timing story.

## Slide 6 — Timing as an objective

![Timing as an objective](assets/steps/05-takeaway.png)

Reweighting turns the same FM kernel into a timing-aware partitioner. Students compare plain vs weighted metrics on one seed.

<!-- /algorithm-walkthrough -->

## Slide 7 — Browser lab track

In the browser lab, run timing-aware refinement from the bad seed. Confirm plain cut three and weighted cut seven.

## Slide 8 — Implement track

Run timing-aware mode and confirm ABC versus DE, plain three, weighted seven.

```bash
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode timing --seed ../module02-05-kernighan-lin/examples/seed_partition.json --criticality examples/criticality.json
```

## Slide 9 — Pitfalls to watch

Criticality of one means no boost—document defaults. Mixing plain and weighted metrics in the same table confuses compares.

## Slide 10 — Your turn

Match the golden, finish the checklist and quiz, then continue to offline benchmark compare.
