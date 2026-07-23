# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none
**Tracks:** offline harness

## Slide 1 — Why compare

Toy estimators need a harness: same JSON in, overflow and runtime out. Comparing engines teaches you what “better congestion” means beyond a pretty heat map.

## Slide 2 — The idea

Fix the instance. Run RUDY and probabilistic. Record total overflow, max overflow, wall time. Optionally compare to a reference map. Write one discrepancy hypothesis.

## Slide 3 — Harness shape

A small Python driver loading tiny_cong.json is enough. Print a markdown table. Missing external tools are OK—document blockers and still validate I/O.

## Slide 4 — Pitfalls

Changing Cap between rows of the table. Comparing incompatible demand units. Optimizing runtime before correctness.

## Slide 5 — Your turn

Fill one comparison table for spread versus congested seeds. Then open the wrap.
