# Track usage and capacity

**Module id:** module02-05-track-usage
**Lab:** track-usage
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — When usage exceeds capacity

Each directed M1 or M2 track has capacity one on tiny_dr. Every routed net deposits plus one on each track its segments traverse. Overflow is how far usage exceeds capacity—summed, maxed, and counted per track.

## Slide 2 — The idea

path_track_usage walks consecutive segment pairs, maps horizontal moves to h_edge and vertical to v_edge, increments usage. track_overflow computes max of zero and usage minus capacity per track. Sequential L-HV on all six nets should yield positive total overflow at cap one.

<!-- algorithm-walkthrough -->

## Slide 3 — Usage heat

![Usage heat](assets/steps/01-def.png)

Each M1/M2 track accumulates routed net count.

## Slide 4 — Total overflow

![Total overflow](assets/steps/02-total.png)

Sum over tracks—primary scalar.

## Slide 5 — Max overflow

![Max overflow](assets/steps/03-max.png)

Worst track catches hotspot corridors.

## Slide 6 — Overflow count

![Overflow count](assets/steps/04-count.png)

How many tracks exceed Cap.

## Slide 7 — Hit targets

![Hit targets](assets/steps/05-target.png)

Move pins or switch Lee/A* to clear thresholds.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Open **track-usage**. Run sequential L routes and read the triple total max count. Heat-map the worst track.

## Slide 9 — Implement track

Implement `path_track_usage` and `track_overflow`. Call sequential_detailed with mode l_hv on tiny_dr and assert total overflow is greater than zero.

## Slide 10 — Pitfalls

Computing overflow before summing all nets. Using GCell edge usage from global routing instead of directed tracks. Reporting negative overflow values.

## Slide 11 — Your turn

Hit overflow targets. Next: assign vias on two-layer L paths.
